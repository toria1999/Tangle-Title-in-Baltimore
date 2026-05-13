from html import escape
from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from shared_style import apply_theme


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
QUANT_DIR = DATA_DIR / "quant"

TRACT_METRICS = QUANT_DIR / "quant_merged_data.csv"
BALTIMORE_TRACTS_GEOJSON = QUANT_DIR / "baltimore_tracts.geojson"

# Coerce after read_csv so currency/counts survive Excel/CSV quirks (commas, stray spaces).
# Dollar / equity columns may arrive as strings with commas or $ from hand-edited CSVs.
_TRACT_EQUITY_LIKE_COLUMNS: frozenset[str] = frozenset(
    {
        "tangled_net_equity",
        "at_risk_net_equity",
        "tangled_gross_positive_equity",
        "at_risk_gross_positive_equity",
        "tangled_gross_negative_equity",
        "at_risk_gross_negative_equity",
    }
)

_TRACT_METRICS_NUMERIC_COLUMNS: tuple[str, ...] = (
    "intersectionality_group_id",
    "tangled_properties",
    "at_risk_properties",
    "ratio",
    "tangled_net_equity",
    "at_risk_net_equity",
    "tangled_gross_positive_equity",
    "at_risk_gross_positive_equity",
    "tangled_gross_negative_equity",
    "at_risk_gross_negative_equity",
    "black_population_percentage",
    "median_property_value_total",
    "median_property_value_black",
    "total_properties",
    "total_population",
)
INTRO_IMAGE = QUANT_DIR / "andra-c-taylor-jr-mM52YKqAER8-unsplash.jpg"
HOLC_MAP_IMAGE = QUANT_DIR / "holc-map.png"
PLACES_CASTHMA_TANGLED_LOESS_SVG = (
    QUANT_DIR / "places_casthma_x_tangled_titles_numbers_per_10000_population_loess.svg"
)
CSA_LEVEL_LE_LOESS_SVG = QUANT_DIR / "20260509_CSA_level_LE_loess.svg"

# Match `render_interactive_map` Plotly height + selectbox/caption slack; left column stretches to this min.
_INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX = 560
_CITYWIDE_MAP_ROW_LEFT_MIN_HEIGHT_PX = _INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX + 220
# Quadrant diagram + tract group map (same Streamlit row): shared Plotly height for visual alignment.
_QUADRANT_GROUP_MAP_ROW_FIG_HEIGHT_PX = 480
# Black population scatter + intersectionality boxplots (same Streamlit row): matched Plotly height.
_IMPACT_SCATTER_BOXPLOT_ROW_FIG_HEIGHT_PX = 520

GROUP_LABELS = {
    "Sustained advantage": "Historically advantaged + currently advantaged",
    "Contemporary advantage": "Historically disadvantaged + currently advantaged",
    "Previous advantage": "Historically advantaged + currently disadvantaged",
    "Sustained disadvantage": "Historically disadvantaged + currently disadvantaged",
    "Excluded from analysis": "Excluded / insufficient data",
}
GROUP_ORDER = list(GROUP_LABELS.keys())
DISPLAY_GROUP_ORDER = [GROUP_LABELS[group] for group in GROUP_ORDER]
GROUP_SHORT_LABELS = {
    "Historically advantaged + currently advantaged": "Hist. adv.<br>Current adv.",
    "Historically disadvantaged + currently advantaged": "Hist. disadv.<br>Current adv.",
    "Historically advantaged + currently disadvantaged": "Hist. adv.<br>Current disadv.",
    "Historically disadvantaged + currently disadvantaged": "Hist. disadv.<br>Current disadv.",
    "Excluded / insufficient data": "Excluded<br>/ insufficient data",
}
GROUP_COLORS = {
    "Historically advantaged + currently advantaged": "#a9c77b",
    "Historically disadvantaged + currently advantaged": "#f0c56a",
    "Historically advantaged + currently disadvantaged": "#e58b60",
    "Historically disadvantaged + currently disadvantaged": "#8f3d46",
    "Excluded / insufficient data": "#b9b9b9",
}

# Column specs for `render_group_boxplots` (label -> column name, axis unit, value tick format).
# Dict order is the selectbox order; Black population is first by default.
GROUP_BOXPLOT_METRIC_SPECS: dict[str, tuple[str, str, str]] = {
    "Black population (%)": ("black_population_percentage", "%", ":.1f"),
    "Median property value, all (USD)": ("median_property_value_total", "$", ":,.0f"),
    "Median property value, Black (USD)": ("median_property_value_black", "$", ":,.0f"),
    "Tangled-title properties (per 1,000 properties)": (
        "tangled_properties_per_1000",
        "rate",
        ":,.1f",
    ),
    "At-risk properties (per 1,000 properties)": (
        "at_risk_properties_per_1000",
        "rate",
        ":,.1f",
    ),
    "Tangled / at-risk ratio": ("ratio", "ratio", ":.3f"),
    "Tangled net equity (USD)": ("tangled_net_equity", "$", ":,.0f"),
    "At-risk net equity (USD)": ("at_risk_net_equity", "$", ":,.0f"),
}

# (fragment id, H2 title) for in-page sidebar TOC on this page only.
_QUANT_TOC_H2: tuple[tuple[str, str], ...] = (
    ("what-is-the-burden-of-tangled-titles", "What is the burden of tangled titles?"),
    ("who-is-carrying-the-burden", "Who's carrying the burden?"),
    ("historical-context", "Historical Context"),
    (
        "impact-of-historical-contemporary-disadvantage",
        "Measuring the impact of historical redlining disadvantage and contemporary segregation disadvantage",
    ),
)


st.set_page_config(page_title="Quantitative Evidence", layout="wide")
apply_theme()

# =============================================================================
# Helpers: I/O, formatting, and chart/map renderers (layout starts near page bottom)
# =============================================================================


@st.cache_data(show_spinner=False)
def _series_to_numeric_loose(series: pd.Series) -> pd.Series:
    """Parse numbers; strip $, commas, and spaces if plain to_numeric fails."""
    first = pd.to_numeric(series, errors="coerce")
    if first.notna().any():
        return first
    cleaned = (
        series.astype("string")
        .str.replace(r"[$,\s]", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def load_tract_metrics(mtime: float | None = None) -> pd.DataFrame | None:
    if not TRACT_METRICS.exists():
        return None
    df = pd.read_csv(TRACT_METRICS, encoding="utf-8-sig")
    df.columns = [str(c).lstrip("\ufeff").strip() for c in df.columns]
    # Rare alternate headers from exports
    _alias = {"at-risk_net_equity": "at_risk_net_equity", "At_risk_net_equity": "at_risk_net_equity"}
    df = df.rename(columns={a: b for a, b in _alias.items() if a in df.columns})
    for col in _TRACT_METRICS_NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        if col in _TRACT_EQUITY_LIKE_COLUMNS:
            df[col] = _series_to_numeric_loose(df[col])
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "GEOID" in df.columns:
        df["GEOID"] = df["GEOID"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(11)
    return df


@st.cache_data(show_spinner=False)
def load_geojson(mtime: float | None = None) -> dict | None:
    if not BALTIMORE_TRACTS_GEOJSON.exists():
        return None
    return json.loads(BALTIMORE_TRACTS_GEOJSON.read_text(encoding="utf-8"))


def fmt_money(value: float | int | str) -> str:
    try:
        if pd.isna(value):
            return "NA"
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "NA"


def file_mtime(path: Path) -> float | None:
    return path.stat().st_mtime if path.exists() else None


def fmt_int(value: float | int | str) -> str:
    try:
        if pd.isna(value):
            return "NA"
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return "NA"


def baltimore_city_tracts(tracts: pd.DataFrame | None) -> pd.DataFrame:
    if tracts is None:
        return pd.DataFrame()
    if "GEOID" in tracts.columns:
        return tracts[tracts["GEOID"].astype(str).str.startswith("24510")].copy()
    return tracts.copy()


def _enrich_city_boxplot_derived_columns(city: pd.DataFrame) -> None:
    """Add per-1,000-property burden columns for group boxplots (mutates `city` in place)."""
    if {"tangled_properties", "total_properties"}.issubset(city.columns):
        denominator = city["total_properties"].where(city["total_properties"] > 0)
        city["tangled_properties_per_1000"] = (city["tangled_properties"] / denominator) * 1000
    if {"at_risk_properties", "total_properties"}.issubset(city.columns):
        denominator = city["total_properties"].where(city["total_properties"] > 0)
        city["at_risk_properties_per_1000"] = (city["at_risk_properties"] / denominator) * 1000


def _group_boxplot_selectable_metric_labels(tracts: pd.DataFrame | None) -> list[str] | None:
    """Metric labels available for the group boxplot selectbox, or None if the boxplot cannot be built."""
    if tracts is None or "intersectionality_group" not in tracts.columns:
        return None
    city = baltimore_city_tracts(tracts).copy()
    if city.empty:
        return None
    _enrich_city_boxplot_derived_columns(city)
    available = {
        label: spec for label, spec in GROUP_BOXPLOT_METRIC_SPECS.items() if spec[0] in city.columns
    }
    if not available:
        return None
    return list(available.keys())


def render_citywide_tract_summary_panel(baltimore: pd.DataFrame) -> None:
    """Baltimore City (GEOID 24510) headline counts, net equity metrics, and gross-positive caption."""
    with st.container(border=True):
        st.markdown(
            """
            <p class="quant-citywide-panel-root" style="font-size: 1.45rem; font-weight: 600; line-height: 1.5; color: #18312d; margin: 0 0 0.35rem 0;">
            In Baltimore, there are:
            </p>
            """,
            unsafe_allow_html=True,
        )
        cols = baltimore.columns

        if "tangled_properties" in cols:
            tangled_property_count = baltimore["tangled_properties"].sum(skipna=True)
        else:
            tangled_property_count = 0
        if "at_risk_properties" in cols:
            at_risk_property_count = baltimore["at_risk_properties"].sum(skipna=True)
        else:
            at_risk_property_count = 0

        if "tangled_net_equity" in cols:
            tangled_net_equity_citywide = baltimore["tangled_net_equity"].sum(skipna=True)
        else:
            tangled_net_equity_citywide = float("nan")
        if "at_risk_net_equity" in cols:
            at_risk_net_equity_citywide = baltimore["at_risk_net_equity"].sum(skipna=True)
        else:
            at_risk_net_equity_citywide = float("nan")

        burden_metrics = (
            ("Tangled-title properties", fmt_int(tangled_property_count)),
            ("At-risk properties", fmt_int(at_risk_property_count)),
            ("Estimated tangled net equity", fmt_money(tangled_net_equity_citywide)),
            ("Estimated at-risk net equity", fmt_money(at_risk_net_equity_citywide)),
        )
        top_left, top_right = st.columns(2)
        with top_left:
            st.metric(burden_metrics[0][0], burden_metrics[0][1])
        with top_right:
            st.metric(burden_metrics[1][0], burden_metrics[1][1])
        bottom_left, bottom_right = st.columns(2)
        with bottom_left:
            st.metric(burden_metrics[2][0], burden_metrics[2][1])
        with bottom_right:
            st.metric(burden_metrics[3][0], burden_metrics[3][1])

        if "tangled_gross_positive_equity" in cols:
            gross_positive_tangled = baltimore["tangled_gross_positive_equity"].sum(skipna=True)
        else:
            gross_positive_tangled = float("nan")
        if "at_risk_gross_positive_equity" in cols:
            gross_positive_at_risk = baltimore["at_risk_gross_positive_equity"].sum(skipna=True)
        else:
            gross_positive_at_risk = float("nan")
        st.caption(
            "Across tracts, gross positive equity stacks each tract's positive slice: "
            f"tangled-title totals {fmt_money(gross_positive_tangled)} and at-risk totals {fmt_money(gross_positive_at_risk)}. "
            "Net equity can read smaller when negative-equity exposure offsets those positive amounts."
        )


def _quant_section_h2(fragment_id: str, title_plain: str) -> None:
    """Native H2 with a stable DOM id for TOC / hash links.

    Streamlit strips ``id`` from raw ``<h2>`` in ``st.markdown``; ``anchor=`` is supported.
    """
    st.header(title_plain, anchor=fragment_id)


def render_interactive_map(tracts: pd.DataFrame | None, geojson: dict | None) -> None:
    if tracts is None or geojson is None:
        if tracts is None:
            st.warning("Cannot show the map: tract metrics CSV is missing.")
        else:
            st.warning("Cannot show the map: `baltimore_tracts.geojson` is missing.")
        return
    tract_ids = {
        str(feature.get("properties", {}).get("GEOID", ""))
        for feature in geojson.get("features", [])
    }
    map_data = baltimore_city_tracts(tracts)
    if "GEOID" in map_data.columns and tract_ids:
        map_data = map_data[map_data["GEOID"].astype(str).isin(tract_ids)].copy()
    if map_data.empty:
        st.warning("The tract table and boundary file are loaded, but their GEOIDs do not overlap.")
        return

    metric_options = {
        "Tangled-title properties": "tangled_properties",
        "At-risk properties": "at_risk_properties",
        "Tangled / at-risk ratio": "ratio",
        "Tangled net equity": "tangled_net_equity",
        "At-risk net equity": "at_risk_net_equity",
    }
    available = {label: col for label, col in metric_options.items() if col in map_data.columns}
    if not available:
        st.warning("No map metrics found in the tract table.")
        return
    selected_label = st.selectbox("Choose tract metric", list(available.keys()))
    selected_col = available[selected_label]

    hover_data: dict = {}
    if "tangled_properties" in map_data.columns:
        hover_data["tangled_properties"] = ":,.0f"
    if "at_risk_properties" in map_data.columns:
        hover_data["at_risk_properties"] = ":,.0f"
    if "ratio" in map_data.columns:
        hover_data["ratio"] = ":.3f"
    if "tangled_net_equity" in map_data.columns:
        hover_data["tangled_net_equity"] = ":$,.0f"
    if "at_risk_net_equity" in map_data.columns:
        hover_data["at_risk_net_equity"] = ":$,.0f"
    if "intersectionality_group" in map_data.columns:
        hover_data["intersectionality_group"] = True
    # Ensure the choropleth color variable appears in the tooltip (Plotly can omit it when hover_data is set).
    if selected_col not in hover_data:
        hover_data[selected_col] = ":$,.0f" if selected_col in ("tangled_net_equity", "at_risk_net_equity") else True

    _equity_map_cols = frozenset({"tangled_net_equity", "at_risk_net_equity"})
    _map_kw: dict = dict(
        data_frame=map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color=selected_col,
        hover_name="GEOID",
        hover_data=hover_data or None,
        map_style="carto-positron",
        center={"lat": 39.299, "lon": -76.61},
        zoom=10,
        opacity=0.78,
        height=_INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX,
    )
    if selected_col in _equity_map_cols:
        # Signed dollars: a sequential cream→green scale collapses contrast when one tract is a huge outlier.
        abs_s = map_data[selected_col].dropna().abs()
        if len(abs_s) > 0:
            vmax = float(abs_s.quantile(0.98))
            if vmax == 0 or pd.isna(vmax):
                vmax = max(float(abs_s.max()), 1.0)
        else:
            vmax = 1.0
        _map_kw["color_continuous_scale"] = "RdBu_r"
        _map_kw["color_continuous_midpoint"] = 0
        _map_kw["range_color"] = (-vmax, vmax)
    else:
        _map_kw["color_continuous_scale"] = ["#fff7dc", "#efc267", "#a9c77b", "#294943"]

    map_fig = px.choropleth_map(**_map_kw)
    map_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(map_fig, width="stretch")


def render_black_homeownership_chart(tracts: pd.DataFrame | None) -> None:
    if tracts is None:
        st.warning("Cannot show the chart: tract metrics CSV is missing.")
        return
    needed = {"black_population_percentage", "median_property_value_black", "median_property_value_total"}
    if not needed.issubset(tracts.columns):
        st.warning("Required columns for Black homeownership / property value are missing in the tract table.")
        return

    city = baltimore_city_tracts(tracts).copy()
    if city.empty:
        st.warning("No Baltimore City tracts available for the chart.")
        return

    chart_df = city.dropna(
        subset=["black_population_percentage", "median_property_value_black"]
    ).copy()
    if "intersectionality_group" in chart_df.columns:
        chart_df["intersectionality_group"] = chart_df["intersectionality_group"].fillna("Excluded from analysis")
        chart_df["intersectionality_group_display"] = (
            chart_df["intersectionality_group"].map(GROUP_LABELS).fillna("Excluded / insufficient data")
        )

    has_population = "total_population" in chart_df.columns
    has_total = "total_properties" in chart_df.columns
    has_tangled = "tangled_properties" in chart_df.columns

    if has_total and has_tangled:
        denom = chart_df["total_properties"].astype(float)
        tangled = chart_df["tangled_properties"].fillna(0).astype(float)
        chart_df["tangled_properties_per_1000"] = (tangled / denom.where(denom > 0)) * 1000.0
        size_col = "tangled_properties_per_1000"
        size_legend = "Tangled per 1,000 properties"
        plot_df = chart_df.dropna(subset=[size_col]).copy()
    else:
        st.info(
            "`total_properties` (ACS B25003_001 occupied housing units) is missing from the loaded "
            "`quant_merged_data.csv`, or `tangled_properties` is missing. Falling back to tangled-title "
            "property counts for bubble size. Re-render `20260507_data_merge.qmd` and reload Streamlit "
            "to use the per-1,000-properties view."
        )
        if has_tangled:
            chart_df["tangled_count_size"] = chart_df["tangled_properties"].fillna(0).clip(lower=0) + 1
        else:
            chart_df["tangled_count_size"] = 1
        size_col = "tangled_count_size"
        size_legend = "Tangled-title properties"
        plot_df = chart_df

    if plot_df.empty:
        st.warning("No tracts left to plot for the Black population × property value chart.")
        return

    hover_data = {
        "black_population_percentage": ":.1f",
        "median_property_value_black": ":$,.0f",
        "median_property_value_total": ":$,.0f",
    }
    if has_tangled:
        hover_data["tangled_properties"] = ":,.0f"
    if has_population:
        hover_data["total_population"] = ":,.0f"
    if has_total:
        hover_data["total_properties"] = ":,.0f"
    if size_col == "tangled_properties_per_1000":
        hover_data["tangled_properties_per_1000"] = ":,.2f"
    if "intersectionality_group_display" in plot_df.columns:
        hover_data["intersectionality_group_display"] = True
    if size_col not in hover_data:
        hover_data[size_col] = False

    scatter_kwargs: dict = dict(
        data_frame=plot_df,
        x="black_population_percentage",
        y="median_property_value_black",
        size=size_col,
        size_max=28,
        hover_name="GEOID",
        hover_data=hover_data,
        labels={
            "black_population_percentage": "Black population (%)",
            "median_property_value_black": "Median property value, Black applicants (USD)",
            "median_property_value_total": "Median property value, all applicants (USD)",
            "intersectionality_group_display": "Historical/current disadvantage group",
            "tangled_properties": "Tangled-title properties",
            "total_population": "Total population (ACS B01003_001)",
            "total_properties": "Total properties (ACS B25003_001)",
            "tangled_properties_per_1000": "Tangled per 1,000 properties",
            "tangled_count_size": size_legend,
        },
    )
    if "intersectionality_group_display" in chart_df.columns:
        scatter_kwargs["color"] = "intersectionality_group_display"
        scatter_kwargs["color_discrete_map"] = GROUP_COLORS
        scatter_kwargs["category_orders"] = {"intersectionality_group_display": DISPLAY_GROUP_ORDER}

    fig = px.scatter(**scatter_kwargs)
    fig.update_traces(marker=dict(line=dict(width=1, color="#294943"), opacity=0.85))
    fig.update_layout(
        height=_IMPACT_SCATTER_BOXPLOT_ROW_FIG_HEIGHT_PX,
        margin=dict(l=10, r=10, t=10, b=120),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        legend=dict(
            title="Historical/current disadvantage group",
            orientation="h",
            yanchor="top",
            y=-0.14,
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(showgrid=True, gridcolor="rgba(41, 73, 67, 0.12)", ticksuffix="%"),
        yaxis=dict(showgrid=True, gridcolor="rgba(41, 73, 67, 0.12)", tickprefix="$", tickformat=",.0f"),
    )
    guide = (
        "Each point is a Baltimore City census tract. **Horizontal axis:** Black population share (%). "
        "**Vertical axis:** FFIEC median property value for Black applicants (USD). "
    )
    if "intersectionality_group_display" in chart_df.columns:
        guide += (
            "**Color:** historical/current disadvantage group. **Legend:** click a group name to hide or show that series; "
            "double-click a name to show only that group (double-click again to restore all). "
        )
    guide += f"**Bubble size:** {size_legend.lower()}."
    if size_col == "tangled_properties_per_1000":
        guide += (
            " Denominator for the rate is ACS 2019 5-year occupied housing units per tract (B25003_001)."
        )
    st.markdown(
        "Each point represents a Baltimore census tract. The plot shows how Black population share, "
        "median property value for Black applicants, tangled-title burden, and intersectionality group overlap. "
        "Tracts with higher Black population share tend to cluster in lower property-value ranges, while bubble size "
        "shows where tangled-title burden is heavier. Use the legend to click groups on or off, or double-click a group to isolate it."
    )
    st.plotly_chart(fig, width="stretch")
    st.markdown(guide)
    st.caption("Tracts with missing FFIEC median values for Black applicants are omitted from the plot.")


def render_demographic_property_value_map(
    tracts: pd.DataFrame | None,
    geojson: dict | None,
    metric_options: dict[str, tuple[str, str]],
    selectbox_label: str,
    selectbox_key: str,
    height: int = 460,
) -> None:
    if tracts is None or geojson is None:
        st.warning("Cannot show the map: tract metrics or boundary file is missing.")
        return

    tract_ids = {
        str(feature.get("properties", {}).get("GEOID", ""))
        for feature in geojson.get("features", [])
    }
    map_data = baltimore_city_tracts(tracts)
    if "GEOID" in map_data.columns and tract_ids:
        map_data = map_data[map_data["GEOID"].astype(str).isin(tract_ids)].copy()
    if map_data.empty:
        st.warning("No overlapping tracts to map.")
        return

    available = {label: spec for label, spec in metric_options.items() if spec[0] in map_data.columns}
    if not available:
        st.warning("None of the requested columns are present in the tract table.")
        return

    if len(available) == 1:
        # Keep control height consistent across side-by-side columns.
        selected_label = next(iter(available))
        st.selectbox(
            selectbox_label,
            [selected_label],
            index=0,
            key=selectbox_key,
            disabled=True,
        )
    else:
        selected_label = st.selectbox(selectbox_label, list(available.keys()), key=selectbox_key)
    selected_col, axis_unit = available[selected_label]

    hover_data: dict = {}
    if "black_population_percentage" in map_data.columns:
        hover_data["black_population_percentage"] = ":.1f"
    if "median_property_value_total" in map_data.columns:
        hover_data["median_property_value_total"] = ":$,.0f"
    if "median_property_value_black" in map_data.columns:
        hover_data["median_property_value_black"] = ":$,.0f"
    if "intersectionality_group" in map_data.columns:
        map_data["intersectionality_group_display"] = (
            map_data["intersectionality_group"].map(GROUP_LABELS).fillna("Excluded / insufficient data")
        )
        hover_data["intersectionality_group_display"] = True

    if axis_unit == "%":
        scale = ["#fff7dc", "#a9c77b", "#294943"]
    else:
        scale = ["#fff7dc", "#efc267", "#c88f2e", "#294943"]

    map_fig = px.choropleth_map(
        map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color=selected_col,
        hover_name="GEOID",
        hover_data=hover_data or None,
        color_continuous_scale=scale,
        map_style="carto-positron",
        center={"lat": 39.299, "lon": -76.61},
        zoom=10,
        opacity=0.78,
        height=height,
        labels={
            "black_population_percentage": "Black population (%)",
            "median_property_value_total": "Median property value, all (USD)",
            "median_property_value_black": "Median property value, Black (USD)",
            "intersectionality_group_display": "Historical/current disadvantage group",
        },
    )
    cb = dict(title=selected_label)
    if axis_unit == "%":
        cb["ticksuffix"] = "%"
    else:
        cb["tickprefix"] = "$"
        cb["tickformat"] = ",.0f"
    map_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar=cb)
    st.plotly_chart(map_fig, width="stretch")


def render_quadrant_diagram() -> None:
    fig = go.Figure()

    # Four filled quadrants with dividing lines. Internal labels are intentionally
    # short so they remain legible when the Streamlit column narrows.
    quadrants = [
        ("Historically disadvantaged + currently advantaged", "Hist. disadvantaged<br>+ current advantaged", 0.0, 0.5, 0.5, 1.0, "Redlining legacy", "Current advantage"),
        ("Historically advantaged + currently advantaged", "Hist. advantaged<br>+ current advantaged", 0.5, 1.0, 0.5, 1.0, "Less redlining legacy", "Current advantage"),
        ("Historically disadvantaged + currently disadvantaged", "Hist. disadvantaged<br>+ current disadvantaged", 0.0, 0.5, 0.0, 0.5, "Redlining legacy", "Current disadvantage"),
        ("Historically advantaged + currently disadvantaged", "Hist. advantaged<br>+ current disadvantaged", 0.5, 1.0, 0.0, 0.5, "Less redlining legacy", "Current disadvantage"),
    ]
    group_color_key = {
        "Historically disadvantaged + currently advantaged": "Historically disadvantaged + currently advantaged",
        "Historically advantaged + currently advantaged": "Historically advantaged + currently advantaged",
        "Historically disadvantaged + currently disadvantaged": "Historically disadvantaged + currently disadvantaged",
        "Historically advantaged + currently disadvantaged": "Historically advantaged + currently disadvantaged",
    }
    text_color = {
        "Historically disadvantaged + currently advantaged": "#101010",
        "Historically advantaged + currently advantaged": "#101010",
        "Historically disadvantaged + currently disadvantaged": "#ffffff",
        "Historically advantaged + currently disadvantaged": "#ffffff",
    }

    for title, short_title, x0, x1, y0, y1, line2, line3 in quadrants:
        fill = GROUP_COLORS[group_color_key[title]]
        fig.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            line=dict(color="#18312d", width=1.8),
            fillcolor=fill,
            layer="below",
        )
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        fig.add_annotation(
            x=cx,
            y=cy + 0.105,
            text=f"<b>{short_title}</b>",
            showarrow=False,
            font=dict(size=12, color=text_color[title], family="Source Sans Pro, sans-serif"),
            align="center",
        )
        fig.add_annotation(
            x=cx,
            y=cy - 0.015,
            text=f"<b>{line2}</b>",
            showarrow=False,
            font=dict(size=10, color=text_color[title], family="Source Sans Pro, sans-serif"),
            align="center",
        )
        fig.add_annotation(
            x=cx,
            y=cy - 0.105,
            text=f"<b>{line3}</b>",
            showarrow=False,
            font=dict(size=10, color=text_color[title], family="Source Sans Pro, sans-serif"),
            align="center",
        )

    # Crosshair between quadrants.
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=0, y1=1, line=dict(color="#18312d", width=2))
    fig.add_shape(type="line", x0=0, x1=1, y0=0.5, y1=0.5, line=dict(color="#18312d", width=2))

    # Axis arrows (outside the square to mimic the reference figure).
    fig.add_annotation(
        x=1.03,
        y=-0.03,
        xref="x",
        yref="y",
        ax=-0.03,
        ay=-0.03,
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.1,
        arrowwidth=2.2,
        arrowcolor="#101010",
        text="",
    )
    fig.add_annotation(
        x=-0.03,
        y=1.03,
        xref="x",
        yref="y",
        ax=-0.03,
        ay=-0.03,
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.1,
        arrowwidth=2.2,
        arrowcolor="#101010",
        text="",
    )

    # Axis labels sit outside the arrow shafts (Plotly draws the arrow line on top of annotations).
    # - Vertical spine at x≈-0.03: keep all left text fully to the left (xanchor='right').
    # - Horizontal spine at y≈-0.03: bottom captions use yanchor='top' with y below the shaft.
    _left_lbl_x = -0.085
    fig.add_annotation(
        x=_left_lbl_x,
        y=0.53,
        xref="x",
        yref="y",
        text="<b>Contemporary<br>Segregation</b>",
        showarrow=False,
        font=dict(size=15, color="#6d3c1d", family="Source Sans Pro, sans-serif"),
        xanchor="right",
        yanchor="middle",
    )
    fig.add_annotation(
        x=_left_lbl_x,
        y=0.85,
        xref="x",
        yref="y",
        text="<b>Advantage</b><br>(High ICE scores)",
        showarrow=False,
        font=dict(size=10, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="right",
        yanchor="middle",
    )
    fig.add_annotation(
        x=_left_lbl_x,
        y=0.15,
        xref="x",
        yref="y",
        text="<b>Disadvantage</b><br>(Low ICE scores)",
        showarrow=False,
        font=dict(size=10, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="right",
        yanchor="middle",
    )
    fig.add_annotation(
        x=0.5,
        y=-0.046,
        text="<b>Historical Redlining</b>",
        showarrow=False,
        font=dict(size=15, color="#9a2f23", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )
    fig.add_annotation(
        x=0.18,
        y=-0.10,
        text="<b>Disadvantage</b><br>(HOLC Grades C/D)",
        showarrow=False,
        font=dict(size=10, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )
    fig.add_annotation(
        x=0.82,
        y=-0.10,
        text="<b>Advantage</b><br>(HOLC Grades A/B)",
        showarrow=False,
        font=dict(size=10, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )

    fig.update_xaxes(range=[-0.22, 1.06], visible=False, fixedrange=True)
    fig.update_yaxes(range=[-0.24, 1.06], visible=False, fixedrange=True)
    fig.update_layout(
        height=_QUADRANT_GROUP_MAP_ROW_FIG_HEIGHT_PX,
        margin=dict(l=118, r=24, t=18, b=96),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")


def render_intersectionality_group_map(tracts: pd.DataFrame | None, geojson: dict | None) -> None:
    if tracts is None or geojson is None:
        st.warning("Cannot show the group map: tract metrics or boundary file is missing.")
        return
    if "intersectionality_group" not in tracts.columns:
        st.warning("`intersectionality_group` column is missing from the tract table.")
        return

    tract_ids = {
        str(feature.get("properties", {}).get("GEOID", ""))
        for feature in geojson.get("features", [])
    }
    map_data = baltimore_city_tracts(tracts)
    if "GEOID" in map_data.columns and tract_ids:
        map_data = map_data[map_data["GEOID"].astype(str).isin(tract_ids)].copy()
    if map_data.empty:
        st.warning("No overlapping tracts to map for historical/current disadvantage groups.")
        return

    map_data["intersectionality_group"] = map_data["intersectionality_group"].fillna("Excluded from analysis")
    map_data["intersectionality_group_display"] = (
        map_data["intersectionality_group"].map(GROUP_LABELS).fillna("Excluded / insufficient data")
    )
    map_data["intersectionality_group_display"] = pd.Categorical(
        map_data["intersectionality_group_display"], categories=DISPLAY_GROUP_ORDER, ordered=False
    )

    map_fig = px.choropleth_map(
        map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color="intersectionality_group_display",
        category_orders={"intersectionality_group_display": DISPLAY_GROUP_ORDER},
        color_discrete_map=GROUP_COLORS,
        hover_name="GEOID",
        hover_data={
            "intersectionality_group_display": True,
            "tangled_properties": ":,.0f" if "tangled_properties" in map_data.columns else False,
            "at_risk_properties": ":,.0f" if "at_risk_properties" in map_data.columns else False,
        },
        map_style="carto-positron",
        center={"lat": 39.299, "lon": -76.61},
        zoom=10,
        opacity=0.78,
        height=_QUADRANT_GROUP_MAP_ROW_FIG_HEIGHT_PX,
    )
    map_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=52),
        legend=dict(title="Historical/current disadvantage group", orientation="h", yanchor="bottom", y=-0.12, x=0),
    )
    st.plotly_chart(map_fig, width="stretch")


def render_group_boxplots(
    tracts: pd.DataFrame | None,
    *,
    selected_metric_label: str | None = None,
) -> None:
    if tracts is None:
        st.warning("Cannot show boxplots: tract metrics CSV is missing.")
        return
    if "intersectionality_group" not in tracts.columns:
        st.warning("`intersectionality_group` column is missing from the tract table.")
        return

    city = baltimore_city_tracts(tracts).copy()
    if city.empty:
        st.warning("No Baltimore City tracts available for boxplots.")
        return

    _enrich_city_boxplot_derived_columns(city)

    available = {
        label: spec for label, spec in GROUP_BOXPLOT_METRIC_SPECS.items() if spec[0] in city.columns
    }
    if not available:
        st.warning("No metrics available for boxplots.")
        return

    if selected_metric_label is None:
        selected_label = st.selectbox(
            "Choose metric for the boxplot", list(available.keys()), key="group_boxplot_metric"
        )
    elif selected_metric_label not in available:
        st.warning(
            f"Metric `{selected_metric_label}` is not available for boxplots; choose another from the list."
        )
        return
    else:
        selected_label = selected_metric_label
    selected_col, axis_unit, _value_fmt = available[selected_label]

    plot_df = city.dropna(subset=["intersectionality_group", selected_col]).copy()
    if plot_df.empty:
        st.warning("No non-missing values to plot for the selected metric.")
        return
    plot_df["intersectionality_group_display"] = (
        plot_df["intersectionality_group"].map(GROUP_LABELS).fillna("Excluded / insufficient data")
    )
    plot_df["intersectionality_group_display"] = pd.Categorical(
        plot_df["intersectionality_group_display"], categories=DISPLAY_GROUP_ORDER, ordered=True
    )
    plot_df = plot_df.sort_values("intersectionality_group_display")

    n_total = len(plot_df)
    group_counts = (
        plot_df.groupby("intersectionality_group_display", observed=True)
        .size()
        .reindex(DISPLAY_GROUP_ORDER)
        .fillna(0)
        .astype(int)
    )

    box_hover = {
        "GEOID": True,
        "intersectionality_group_display": False,
        selected_col: (":$,.0f" if axis_unit == "$" else True),
    }

    fig = px.box(
        plot_df,
        x="intersectionality_group_display",
        y=selected_col,
        color="intersectionality_group_display",
        category_orders={"intersectionality_group_display": DISPLAY_GROUP_ORDER},
        color_discrete_map=GROUP_COLORS,
        points="all",
        hover_data=box_hover,
        labels={
            "intersectionality_group_display": "Historical/current disadvantage group",
            selected_col: selected_label,
        },
        title=f"{selected_label} by historical/current disadvantage group (n = {n_total} tracts)",
    )
    fig.update_traces(
        marker=dict(opacity=0.6, size=5, line=dict(width=0.5, color="#294943")),
        boxmean=True,
    )

    yaxis_kwargs: dict = dict(
        title=selected_label,
        showgrid=True,
        gridcolor="rgba(41, 73, 67, 0.12)",
    )
    if axis_unit == "%":
        yaxis_kwargs["ticksuffix"] = "%"
        yaxis_kwargs["tickformat"] = ".1f"
    elif axis_unit == "$":
        yaxis_kwargs["tickprefix"] = "$"
        yaxis_kwargs["tickformat"] = ",.0f"
    elif axis_unit == "count":
        yaxis_kwargs["tickformat"] = ",.0f"
    elif axis_unit == "rate":
        yaxis_kwargs["tickformat"] = ",.1f"
    elif axis_unit == "ratio":
        yaxis_kwargs["tickformat"] = ".2f"

    xaxis_ticktext = [
        f"{GROUP_SHORT_LABELS[group]}<br><span style='font-size:10px;color:#5d6a64'>n={group_counts[group]}</span>"
        for group in DISPLAY_GROUP_ORDER
    ]
    fig.update_layout(
        height=_IMPACT_SCATTER_BOXPLOT_ROW_FIG_HEIGHT_PX,
        margin=dict(l=10, r=10, t=70, b=84),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        showlegend=False,
        title=dict(x=0.0, xanchor="left", font=dict(size=16, color="#18312d")),
        xaxis=dict(
            title="",
            showgrid=False,
            tickmode="array",
            tickvals=DISPLAY_GROUP_ORDER,
            ticktext=xaxis_ticktext,
            tickfont=dict(size=10),
            automargin=True,
        ),
        yaxis=yaxis_kwargs,
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        f"Box = IQR with median line; dashed mark = mean. Each dot is a Baltimore City census tract; "
        f"y-axis shows {selected_label.lower()}. Tracts with missing values for the selected metric "
        "are dropped before counting."
    )
    st.markdown(
        "These box plots show how each metric differs across historical and contemporary disadvantage groups. "
        "For example, historically and currently disadvantaged tracts tend to have much higher Black population shares, "
        "while more advantaged groups tend to have lower Black population shares and higher property-value profiles."
    )


def render_health_outcomes_chart(tracts: pd.DataFrame | None) -> None:
    """PLACES current asthma vs tangled-title rate (pre-rendered loess from MPPPH analysis)."""
    _ = tracts
    if not PLACES_CASTHMA_TANGLED_LOESS_SVG.exists():
        st.warning(
            "Health outcomes figure is missing (expected "
            f"`{PLACES_CASTHMA_TANGLED_LOESS_SVG.name}` under `data/quant/`)."
        )
        return
    st.markdown("### PLACES current asthma vs tangled-title burden")
    st.caption(
        "CDC PLACES model-based current asthma prevalence (tract) vs tangled-title properties per "
        "10,000 residents (ACS tract population). LOESS smooth with confidence band."
    )
    st.image(str(PLACES_CASTHMA_TANGLED_LOESS_SVG), width="stretch")


def render_csa_life_expectancy_loess_panel() -> None:
    """CSA-level 2018 life expectancy vs tangled titles (pre-rendered loess)."""
    if not CSA_LEVEL_LE_LOESS_SVG.exists():
        st.warning(
            "Life expectancy figure is missing (expected "
            f"`{CSA_LEVEL_LE_LOESS_SVG.name}` under `data/quant/`)."
        )
        return
    st.markdown("### Life expectancy (2018) vs tangled titles by CSA")
    st.caption(
        "Community Statistical Area aggregates: 2018 life expectancy vs tangled titles per 10,000; "
        "LOESS by historical/current disadvantage group (y-axis reversed so higher life expectancy reads toward the bottom)."
    )
    st.image(str(CSA_LEVEL_LE_LOESS_SVG), width="stretch")


# =============================================================================
# Page body: load cached inputs (tract table + GeoJSON)
# =============================================================================
tracts = load_tract_metrics(file_mtime(TRACT_METRICS))
geojson = load_geojson(file_mtime(BALTIMORE_TRACTS_GEOJSON))

_toc_link_rows = "".join(
    f'<a id="quant-toc-link-{fid}" class="quant-toc-item{" toc-active" if idx == 0 else ""}" href="#{fid}">{escape(label)}</a>'
    for idx, (fid, label) in enumerate(_QUANT_TOC_H2)
)

# =============================================================================
# Sidebar: in-page TOC ("On this page")
# =============================================================================
with st.sidebar:
    st.markdown(
        f"""
        <style>
            /* Inherit Streamlit / theme font stack and sidebar font-size (see stMain block). */
            #quant-toc-root {{
                font-family: inherit;
                margin: 0.15rem 0 0.75rem 0;
            }}
            /* Sidebar global theme uses * {{ color: ... !important }} — override inside TOC only. */
            section[data-testid="stSidebar"] #quant-toc-root .quant-toc-page-title {{
                font-size: 1em;
                font-weight: 600;
                color: #fffaf0 !important;
                letter-spacing: 0;
                margin: 0 0 0.5rem 0;
                padding: 0;
                text-decoration: none !important;
                border: none;
                box-shadow: none;
            }}
            section[data-testid="stSidebar"] #quant-toc-root .quant-toc-item {{
                display: block;
                margin: 0.08rem 0;
                padding: 0.38rem 0.45rem;
                border: 2px solid transparent !important;
                border-radius: 6px;
                color: rgba(255, 250, 240, 0.92) !important;
                text-decoration: none !important;
                font-size: 1em;
                line-height: inherit;
                font-weight: 500 !important;
            }}
            section[data-testid="stSidebar"] #quant-toc-root .quant-toc-item:hover {{
                background: rgba(239, 194, 103, 0.15) !important;
            }}
            section[data-testid="stSidebar"] #quant-toc-root .quant-toc-item.toc-active {{
                font-weight: 700 !important;
                color: #fffaf0 !important;
                border: 2px solid #efc267 !important;
                background: rgba(0, 0, 0, 0.18) !important;
            }}
        </style>
        <div id="quant-toc-root">
            <p class="quant-toc-page-title">On this page</p>
            {_toc_link_rows}
        </div>
        """,
        unsafe_allow_html=True,
    )

# =============================================================================
# H1: page title + main-column baseline styles
# =============================================================================
st.title("Quantitative Evidence")
st.markdown(
    """
    <div style="border-left: 6px solid #efc267; background: rgba(255,247,220,0.86); border-radius: 8px; padding: 0.9rem 1rem; margin: 0.55rem 0 1.1rem;">
        <strong>Where is tangled title risk concentrated in Baltimore?</strong><br>
        Use this map descriptively. It shows spatial patterns and overlap, not causal proof.
        Darker areas indicate higher measured burden or risk depending on the selected metric.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
        section[data-testid="stMain"] {
            font-size: 1.08rem;
        }
        section[data-testid="stMain"] h2 {
            scroll-margin-top: 4.5rem;
        }
        section[data-testid="stMain"] p,
        section[data-testid="stMain"] li {
            line-height: 1.62;
        }
        section[data-testid="stMain"] [data-testid="stCaption"] {
            font-size: 0.95rem;
        }
        section[data-testid="stSidebar"] {
            font-size: 1.02rem;
        }
    </style>
    <p style="font-size: 1.18rem; line-height: 1.58; color: #18312d; margin: 0;">
    Tract-level descriptive evidence for tangled-title and at-risk property burden in Baltimore City.
    </p>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# H2: What is the burden of tangled titles?
# =============================================================================
_quant_section_h2(
    "what-is-the-burden-of-tangled-titles",
    "What is the burden of tangled titles?",
)

intro_photo_col, intro_text_col = st.columns([1, 2], gap="large")
with intro_photo_col:
    if INTRO_IMAGE.exists():
        st.image(str(INTRO_IMAGE), width="stretch")
        st.markdown(
            """
            <p style="font-size: 0.78rem; line-height: 1.45; color: #5d6a64; margin: 0.1rem 0 0 0;">
            Photo by
            <a href="https://unsplash.com/@taylormadeglobal?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Andra C Taylor Jr</a>
            on
            <a href="https://unsplash.com/photos/a-brick-building-with-trees-in-front-of-it-mM52YKqAER8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
            </p>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"Image not found: `{INTRO_IMAGE.name}`")

with intro_text_col:
    st.markdown(
        """
        <div style="font-size: 1.4rem; line-height: 1.58; color: #18312d;">
        <p style="margin: 0 0 0.75rem 0;">
        Tangled titles are a major source of housing instability and wealth loss for Black homeowners in Baltimore.
        </p>
        <p style="margin: 0 0 0.75rem 0;">
        The conditions have been created by a history of redlining and segregation, and are still present today.
        </p>
        <p style="margin: 0 0 0.75rem 0;">
        Even decades after the end of redlining, the effects of redlining and segregation are still visible in the city.
        </p>
        <p style="margin: 0;">
        This page explores the extent and distribution of tangled titles in Baltimore, and how they are related to historical and contemporary neighborhood disadvantage.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="border-left: 6px solid #a9c77b; background: rgba(241,247,223,0.9); border-radius: 8px; padding: 0.95rem 1.1rem; margin: 1rem 0 1.25rem;">
        <strong>Key takeaways</strong>
        <ul style="margin-bottom: 0;">
            <li>A high proportion of Baltimore's Black population lives in areas shaped by both historical redlining and contemporary segregation.</li>
            <li>In areas where Black residents are concentrated, median property values are often substantially lower, commonly about 2-3 times lower than values in whiter or more advantaged areas.</li>
            <li>Tangled titles can affect health because unstable ownership can limit housing repair, wealth protection, residential stability, and the ability to recover from neighborhood-level disadvantage.</li>
            <li>The decomposition/intersectionality approach separates historical disadvantage from contemporary segregation, helping show whether today's property burden reflects past redlining, current segregation, or their combined effect.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("At-risk property definition", expanded=False):
    st.markdown(
        """
        There is no broadly adopted standard method for measuring tangled titles.
        BWDC adopted PropertyRadar-based criteria to identify properties likely
        to have tangled-title risk. These include properties owned by a single
        person who is likely deceased, properties with ownership transfers more
        than 50 years ago, properties whose last transfer document was an
        Affidavit of Death more than one year ago, multiple-owner properties with
        inheritance-related transfers, and multiple-owner properties where one
        owner is deceased and ownership does not automatically transfer. In our
        analyses, at-risk properties are identified as those likely to become
        tangled, often due to deceased owners or multiple inheritance-based
        ownership structures.
        """
    )

# -----------------------------------------------------------------------------
# Research Questions (RQ cards; not an H2 in TOC)
# -----------------------------------------------------------------------------
st.markdown("### Research Questions")

rq_cards = [
    (
        "RQ1",
        "Who's carrying the burden?",
        "What is the distribution of Black homeownership in Baltimore, and among Black homeowners "
        "what is the median property value (including Black–White gaps)?",
    ),
    (
        "RQ2",
        "Tangled-title concentration and intersectionality",
        "In which Baltimore census tracts are tangled-title and at-risk properties concentrated, "
        "and what is the effect of historical redlining and contemporary segregation on these outcomes?",
    ),
]
rq_cols = st.columns(2)
for column, (tag, title, question) in zip(rq_cols, rq_cards):
    with column:
        st.markdown(
            f"""
            <div class="soft-card rq-card">
            <span class="rq-badge">{tag}</span>
            <h3>{title}</h3>
            <p>{question}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# -----------------------------------------------------------------------------
# Current situation: Baltimore headline metrics + interactive tract map
# -----------------------------------------------------------------------------
st.markdown("### Current Situation in Baltimore")

st.markdown(
    f"""
    <style>
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark) {{
        align-items: stretch !important;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        > div[data-testid="column"]:first-child {{
        display: flex;
        flex-direction: column;
        font-size: 1.14rem;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        > div[data-testid="column"]:first-child > div {{
        flex: 1 1 auto;
        min-height: {_CITYWIDE_MAP_ROW_LEFT_MIN_HEIGHT_PX}px;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.quant-citywide-panel-root) {{
        flex: 1 1 auto;
        min-height: {_CITYWIDE_MAP_ROW_LEFT_MIN_HEIGHT_PX}px;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        font-size: 1.14rem;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.quant-citywide-panel-root)
        > div[data-testid="stVerticalBlock"] {{
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 0;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.quant-citywide-panel-root)
        [data-testid="stMetricContainer"] label p,
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.quant-citywide-panel-root)
        [data-testid="stMetricContainer"] [data-testid="stMarkdownContainer"] p {{
        font-size: 1.2rem !important;
    }}
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(span.quant-citywide-map-row-mark)
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.quant-citywide-panel-root)
        [data-testid="stCaption"] {{
        font-size: 1.02rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

citywide_col, tract_map_col = st.columns([1, 1.5], gap="medium")
with citywide_col:
    st.markdown(
        '<span class="quant-citywide-map-row-mark" style="display:none" aria-hidden="true"></span>',
        unsafe_allow_html=True,
    )
    render_citywide_tract_summary_panel(baltimore_city_tracts(tracts))
with tract_map_col:
    render_interactive_map(tracts, geojson)

st.caption(
    "Data years: Tangled-title and at-risk property indicators are based on 2026 BWDC/PropertyRadar-derived data."
)

st.divider()

# =============================================================================
# H2: Who's carrying the burden?
# =============================================================================
_quant_section_h2("who-is-carrying-the-burden", "Who's carrying the burden?")

st.markdown(
    """
    <div style="font-size: 1.2rem; line-height: 1.62; color: #18312d;">
    <p style="margin: 0;">
    Historical redlining and related credit-market discrimination concentrated Black residents in particular neighborhoods where families acquired housing and passed it down across generations.<br>
    Tangled title—ownership left unsettled when property moves through intestate succession and informal, generational handoffs without a clear legal chain—is fundamentally a problem of that intergenerational transfer of assets.<br>
    It does not occur at random across homeowners; it structurally skews toward Black homeowners.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left_map, right_map = st.columns(2)
with left_map:
    st.markdown("#### Black population Percentage")
    render_demographic_property_value_map(
        tracts,
        geojson,
        metric_options={
            "Black population (%)": ("black_population_percentage", "%"),
        },
        selectbox_label="Demographic metric",
        selectbox_key="demo_metric_left",
    )
with right_map:
    st.markdown("#### Median property value")
    render_demographic_property_value_map(
        tracts,
        geojson,
        metric_options={
            "Median property value, all applicants (USD)": ("median_property_value_total", "$"),
            "Median property value, Black applicants (USD)": ("median_property_value_black", "$"),
        },
        selectbox_label="Property value metric",
        selectbox_key="pv_metric_right",
    )

st.caption("Data years: Black population and median property value indicators are based on 2024 data.")

st.markdown("### Notice the pattern")
st.markdown(
    """
    - Baltimore's "Black Butterfly" pattern is visible in the distribution of Black population share.
    - The same areas of the Black Butterfly also tend to show much lower median property values.
    - This means the burden is not only about where tangled titles occur, but also about where families have fewer property-value resources to absorb legal, repair, or inheritance shocks.
    - The map pattern supports the interpretation that tangled-title risk is spatially tied to racialized property-value inequality.
    """
)

st.divider()

# =============================================================================
# H2: Historical Context
# =============================================================================
_quant_section_h2("historical-context", "Historical Context behind the Situation")

holc_intro_left, holc_intro_right = st.columns([0.62, 0.42], gap="large")
with holc_intro_left:
    st.markdown(
        """
        ### What is a HOLC legacy?
        In the 1930s, the Home Owners' Loan Corporation (HOLC) graded neighborhoods
        across American cities from A ("Best") to D ("Hazardous") — a practice known
        as **redlining**. Grade D areas, marked in red, were predominantly Black
        neighborhoods systematically denied mortgage lending and investment.
        These historical boundaries continue to shape contemporary patterns of
        wealth, property ownership, and neighborhood disadvantage in Baltimore today.

        The intersectionality framework used here (Uzzi et al., 2023) combines
        **historical advantage** (derived from HOLC legacy) with **contemporary
        advantage** (ICE-based segregation index) to classify each census tract
        into one of four groups shown below.
        """
    )

    st.markdown("### Intersectionality Grouping (Uzzi et al., 2023)")

    st.markdown(
        """
        The intersectionality framework used here (Uzzi et al., 2023) combines historical redlining legacy with contemporary
        segregation disadvantage to classify each census tract into one of four groups shown below.  
        Mathematically, tract ICE is the difference between the affluent-tail count and the poor-tail count, divided by the tract denominator—the equation below states the same relationship in symbols.  
        The Index of Concentration at the Extremes (ICE) is a measure of segregation that is calculated by the Census Bureau.
        """
    )
    st.latex(
        r"\mathrm{ICE}_t = \frac{A_t - P_t}{T_t}"
    )
    st.caption(
        "Tract t: A = population at the affluent extreme, P = population at the poor extreme, "
        "T = total population in the ICE denominator (tail cutoffs follow the variable definition in your tract table)."
    )

with holc_intro_right:
    if HOLC_MAP_IMAGE.exists():
        st.image(str(HOLC_MAP_IMAGE), width="stretch")
        st.caption(
            "Home Owner's Loan Corporation (HOLC) 1937 Map with Overlay of Neighborhoods in Baltimore, MD.\n"
            "Source: Baltimore Sun"
        )
    else:
        st.caption(f"HOLC map image not found: `{HOLC_MAP_IMAGE.name}`")



group_hist_left, group_hist_right = st.columns(2)
with group_hist_left:
    st.markdown("#### Four historical/current disadvantage groups")
    render_quadrant_diagram()
with group_hist_right:
    st.markdown("#### Tract distribution across Baltimore")
    render_intersectionality_group_map(tracts, geojson)

st.divider()

# =============================================================================
# H2: Historical redlining disadvantage and contemporary segregation disadvantage
# =============================================================================

_quant_section_h2(
    "impact-of-historical-contemporary-disadvantage",
    "Measuring the impact of historical redlining disadvantage and contemporary segregation disadvantage",
)
st.caption(
    '"Historically disadvantaged" refers to redlining/HOLC legacy. '
    '"Currently disadvantaged" refers to contemporary segregation measured using ICE.'
)

# -----------------------------------------------------------------------------
# Scatter (left) + boxplots (right), under Impact of Historical / Contemporary Disadvantage H2
# Boxplot metric selectbox sits under the right-hand H3 (replacing the former caption in that column).
# -----------------------------------------------------------------------------
_impact_boxplot_metric_labels = _group_boxplot_selectable_metric_labels(tracts)
_impact_selected_box_metric: str | None = None

_impact_scatter_box_titles_l, _impact_scatter_box_titles_r = st.columns(2, gap="medium")
with _impact_scatter_box_titles_l:
    st.markdown("### Black population share and median property value for Black applicants")
    st.caption(
        "Tract-level FFIEC medians for Black applicants vs Black population share; "
        "the note below the scatter explains axes, color, bubble size, and the legend."
    )
with _impact_scatter_box_titles_r:
    st.markdown("### Metric distributions by historical/current disadvantage group")
    if _impact_boxplot_metric_labels:
        _impact_selected_box_metric = st.selectbox(
            "Choose metric for the boxplot",
            _impact_boxplot_metric_labels,
            key="group_boxplot_metric",
        )

_impact_scatter_box_charts_l, _impact_scatter_box_charts_r = st.columns(2, gap="medium")
with _impact_scatter_box_charts_l:
    render_black_homeownership_chart(tracts)
with _impact_scatter_box_charts_r:
    render_group_boxplots(tracts, selected_metric_label=_impact_selected_box_metric)

# Table 1 values from TanglesTitles_MPPPH/analysis/20260504_intersectionality_explore/
# 20260504_intersectionality_explore.html (knitr::kable black_pct_by_group; inner join n=199).
# Mean tangled (per 1,000 properties) / Mean at-risk (per 1,000 properties): tract means of
# (tangled_properties or at_risk_properties) / total_properties * 1000 by intersectionality_group
# (Baltimore city tracts in data/quant/quant_merged_data.csv; tracts with total_properties <= 0 omitted from those means).
_INTERSECTIONAL_GROUP_SUMMARY_TABLE = pd.DataFrame(
    {
        "Intersectional group": [
            "Historically advantaged + currently advantaged (n=32)",
            "Historically disadvantaged + currently advantaged (n=43)",
            "Historically advantaged + currently disadvantaged (n=21)",
            "Historically disadvantaged + currently disadvantaged (n=54)",
            "Excluded / insufficient data (n=49)",
        ],
        "Mean black %": [53.65, 24.53, 89.34, 83.76, 56.70],
        "Median black %": [56.25, 16.50, 89.20, 88.10, 69.80],
        "SD black %": [27.32, 21.28, 5.96, 12.76, 32.18],
        "Mean tangled (per 1,000 properties)": [7.07, 6.01, 18.70, 25.77, 5.34],
        "Mean at-risk (per 1,000 properties)": [4.38, 4.09, 3.95, 3.89, 2.60],
    }
)

st.caption(
    "Descriptive statistics of the four intersectional groups, excluded tracts and Baltimore city "
    "average (non-fatal shooting rate and selected socioeconomic indicators)."
)
st.dataframe(
    _INTERSECTIONAL_GROUP_SUMMARY_TABLE,
    hide_index=True,
    use_container_width=True,
)
st.caption(
    "Black % columns: tract-level black_pct_of_pop (FFIEC HMDA explorer CSV), by intersectional assignment "
    "(20260502_uzzi_replicate_latestdata_geoid_intersectional_group.csv); inner join on GEOID (n matched = 199). "
    "Tangled / at-risk columns: mean tract rate per 1,000 occupied housing units (ACS B25003_001 "
    "`total_properties` in `quant_merged_data.csv`; tracts with total_properties ≤ 0 excluded from those means)."
)

st.divider()

# =============================================================================
# H2: Association with health outcomes
# =============================================================================

_quant_section_h2(
    "association-with-health-outcomes",
    "Association with health outcomes",
)

_health_outcomes_col, _csa_le_col = st.columns(2, gap="medium")
with _health_outcomes_col:
    render_health_outcomes_chart(tracts)
with _csa_le_col:
    render_csa_life_expectancy_loess_panel()

# =============================================================================
# Scroll spy: inject script (st.iframe) for sidebar "On this page" highlighting
# =============================================================================
_toc_sections_json = json.dumps([{"id": fid, "label": label} for fid, label in _QUANT_TOC_H2])
_QUANT_TOC_SCROLL_SPY = """
<script>
(function () {
    const W = window.parent;
    const doc = W.document;
    const sections = __SECTIONS_JSON__;
    const markerSlackPx = 8;

    function getMarkerPx() {
        const id0 = sections.length ? sections[0].id : "";
        const probe = id0 ? resolveHeading(id0) : null;
        if (!probe) return 100;
        const sm = parseFloat(W.getComputedStyle(probe).scrollMarginTop);
        const base = Number.isFinite(sm) && sm > 0 ? sm : 72;
        return Math.round(base + markerSlackPx);
    }

    if (typeof W.__quantTocCleanup === "function") {
        try { W.__quantTocCleanup(); } catch (e) {}
    }

    function isVerticalScroller(el) {
        if (!el || el.nodeType !== 1) return false;
        const st = W.getComputedStyle(el);
        const oy = st.overflowY;
        if (oy !== "auto" && oy !== "scroll" && oy !== "overlay") return false;
        return el.scrollHeight > el.clientHeight + 10;
    }

    /* Streamlit often scrolls a *descendant* of stMain, not an ancestor. Pick the largest overflow. */
    function findLargestVerticalScrollerFrom(main) {
        if (!main) return W;
        let best = W;
        let bestMax = Math.max(0, doc.documentElement.scrollHeight - W.innerHeight);
        const consider = function (el) {
            if (!isVerticalScroller(el)) return;
            const m = el.scrollHeight - el.clientHeight;
            if (m > bestMax) {
                bestMax = m;
                best = el;
            }
        };
        let n = main;
        while (n) {
            consider(n);
            n = n.parentElement;
        }
        main.querySelectorAll("*").forEach(consider);
        return best;
    }

    function resolveHeading(secId) {
        const main = doc.querySelector('[data-testid="stMain"]');
        if (main) {
            try {
                const idSel = typeof CSS !== "undefined" && CSS.escape ? CSS.escape(secId) : secId;
                const found = main.querySelector("#" + idSel);
                if (found) return found;
            } catch (e) {}
        }
        return doc.getElementById(secId);
    }

    function setActive(id) {
        sections.forEach(function (sec) {
            const link = doc.getElementById("quant-toc-link-" + sec.id);
            if (!link) return;
            if (sec.id === id) link.classList.add("toc-active");
            else link.classList.remove("toc-active");
        });
    }

    function addScrollAncestors(start, set) {
        let el = start;
        while (el) {
            const st = W.getComputedStyle(el);
            const oy = st.overflowY;
            if ((oy === "auto" || oy === "scroll" || oy === "overlay") && el.scrollHeight > el.clientHeight + 2) {
                set.add(el);
            }
            el = el.parentElement;
        }
    }

    function gatherScrollTargets() {
        const targets = new Set();
        targets.add(W);
        const main = doc.querySelector('[data-testid="stMain"]');
        if (main) {
            const primary = findLargestVerticalScrollerFrom(main);
            if (primary && primary !== W) targets.add(primary);
            addScrollAncestors(main, targets);
        }
        const app = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (app) addScrollAncestors(app, targets);
        doc.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"]').forEach(function (el) {
            const st = W.getComputedStyle(el);
            if ((st.overflowY === "auto" || st.overflowY === "scroll" || st.overflowY === "overlay") &&
                el.scrollHeight > el.clientHeight + 2) {
                targets.add(el);
            }
        });
        return Array.from(targets);
    }

    /* Among headings at or above the reading band, pick the one with the largest viewport top.
       "Last where top <= line" fails when later headings sit at negative tops inside a nested
       scroller; max-top matches the heading that has advanced furthest while still not below band. */
    function computeActive() {
        const main = doc.querySelector('[data-testid="stMain"]');
        if (!main) {
            setActive(sections[0].id);
            return;
        }
        const m = main.getBoundingClientRect();
        const markerPx = getMarkerPx();
        const line = m.top + Math.max(markerPx, Math.round(m.height * 0.26));
        let bestId = sections[0].id;
        let bestTop = -Infinity;
        sections.forEach(function (sec) {
            const el = resolveHeading(sec.id);
            if (!el) return;
            const top = el.getBoundingClientRect().top;
            if (top > line) return;
            if (top > bestTop) {
                bestTop = top;
                bestId = sec.id;
            }
        });
        if (bestTop === -Infinity) bestId = sections[0].id;
        setActive(bestId);
    }

    let raf = 0;
    function onScrollOrResize() {
        if (raf) return;
        raf = W.requestAnimationFrame(function () {
            raf = 0;
            computeActive();
        });
    }

    function bind() {
        const scrollTargets = gatherScrollTargets();
        W.__quantTocScrollTargets = [];
        scrollTargets.forEach(function (t) {
            t.addEventListener("scroll", onScrollOrResize, { passive: true });
            W.__quantTocScrollTargets.push([t, onScrollOrResize]);
        });
        W.addEventListener("resize", onScrollOrResize, { passive: true });
        W.__quantTocResizeHandler = onScrollOrResize;
        W.__quantTocCleanup = function () {
            (W.__quantTocScrollTargets || []).forEach(function (pair) {
                pair[0].removeEventListener("scroll", pair[1]);
            });
            W.__quantTocScrollTargets = [];
            if (W.__quantTocResizeHandler) {
                W.removeEventListener("resize", W.__quantTocResizeHandler);
                W.__quantTocResizeHandler = null;
            }
            W.__quantTocCleanup = null;
        };
        setTimeout(computeActive, 0);
        setTimeout(computeActive, 250);
        setTimeout(computeActive, 700);
        setTimeout(computeActive, 1500);
    }

    if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", bind);
    else bind();
})();
</script>
"""
st.iframe(
    _QUANT_TOC_SCROLL_SPY.replace("__SECTIONS_JSON__", _toc_sections_json),
    height=1,
    width="stretch",
    tab_index=-1,
)
