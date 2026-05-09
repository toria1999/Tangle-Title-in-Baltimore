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
INTRO_IMAGE = QUANT_DIR / "andra-c-taylor-jr-mM52YKqAER8-unsplash.jpg"
HOLC_MAP_IMAGE = QUANT_DIR / "holc-map.png"

# Match `render_interactive_map` Plotly height + selectbox/caption slack; left column stretches to this min.
_INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX = 560
_CITYWIDE_MAP_ROW_LEFT_MIN_HEIGHT_PX = _INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX + 220
# Quadrant diagram + tract group map (same Streamlit row): shared Plotly height for visual alignment.
_QUADRANT_GROUP_MAP_ROW_FIG_HEIGHT_PX = 480

GROUP_COLORS = {
    "Sustained advantage": "#a9c77b",
    "Contemporary advantage": "#f0c56a",
    "Previous advantage": "#e58b60",
    "Sustained disadvantage": "#8f3d46",
    "Excluded from analysis": "#b9b9b9",
}
GROUP_ORDER = [
    "Sustained advantage",
    "Contemporary advantage",
    "Previous advantage",
    "Sustained disadvantage",
    "Excluded from analysis",
]

# (fragment id, H2 title) for in-page sidebar TOC on this page only.
_QUANT_TOC_H2: tuple[tuple[str, str], ...] = (
    ("what-is-the-burden-of-tangled-titles", "What is the burden of tangled titles?"),
    ("who-is-carrying-the-burden", "Who's carrying the burden?"),
    ("historical-context", "Historical Context"),
    (
        "impact-of-historical-contemporary-disadvantage",
        "Impact of Historical Disadvantage and Contemporary Disadvantage",
    ),
)


st.set_page_config(page_title="Quantitative Evidence", layout="wide")
apply_theme()

# =============================================================================
# Helpers: I/O, formatting, and chart/map renderers (layout starts near page bottom)
# =============================================================================


@st.cache_data(show_spinner=False)
def load_tract_metrics(mtime: float | None = None) -> pd.DataFrame | None:
    if not TRACT_METRICS.exists():
        return None
    df = pd.read_csv(TRACT_METRICS)
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
    if "intersectionality_group" in map_data.columns:
        hover_data["intersectionality_group"] = True

    map_fig = px.choropleth_map(
        map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color=selected_col,
        hover_name="GEOID",
        hover_data=hover_data or None,
        color_continuous_scale=["#fff7dc", "#efc267", "#a9c77b", "#294943"],
        map_style="carto-positron",
        center={"lat": 39.299, "lon": -76.61},
        zoom=10,
        opacity=0.78,
        height=_INTERACTIVE_TRACT_MAP_FIG_HEIGHT_PX,
    )
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

    has_total = "total_properties" in chart_df.columns
    has_tangled = "tangled_properties" in chart_df.columns

    if has_total:
        tangled = (
            chart_df["tangled_properties"].fillna(0).astype(float)
            if has_tangled
            else pd.Series(0.0, index=chart_df.index, dtype=float)
        )
        denom = chart_df["total_properties"].astype(float)
        chart_df["tangled_per_1000_properties"] = (tangled / denom.where(denom > 0)) * 1000.0
        size_col = "tangled_per_1000_properties"
        size_legend = "Tangled per 1,000 properties"
        plot_df = chart_df.dropna(subset=[size_col]).copy()
        n_dropped = len(chart_df) - len(plot_df)
        if n_dropped:
            st.caption(
                f"{n_dropped} tract(s) omitted from this chart: missing `total_properties` or "
                "`total_properties` ≤ 0 (cannot compute tangled per 1,000 properties)."
            )
    else:
        st.info(
            "`total_properties` (ACS B25003_001 occupied housing units) is missing from the loaded "
            "`quant_merged_data.csv`. Falling back to tangled-title property counts for bubble size. "
            "Re-render `20260507_data_merge.qmd` and reload Streamlit to enable the per-1,000 view."
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
    if has_total:
        hover_data["total_properties"] = ":,.0f"
        hover_data["tangled_per_1000_properties"] = ":,.2f"
    if "intersectionality_group" in plot_df.columns:
        hover_data["intersectionality_group"] = True
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
            "intersectionality_group": "Intersectionality group",
            "tangled_properties": "Tangled-title properties",
            "total_properties": "Total properties (ACS B25003_001)",
            "tangled_per_1000_properties": "Tangled per 1,000 properties",
            "tangled_count_size": size_legend,
        },
    )
    if "intersectionality_group" in chart_df.columns:
        scatter_kwargs["color"] = "intersectionality_group"
        scatter_kwargs["color_discrete_map"] = GROUP_COLORS
        scatter_kwargs["category_orders"] = {"intersectionality_group": GROUP_ORDER}

    fig = px.scatter(**scatter_kwargs)
    fig.update_traces(marker=dict(line=dict(width=1, color="#294943"), opacity=0.85))
    fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        legend=dict(title="Group", orientation="h", yanchor="bottom", y=-0.25, x=0),
        xaxis=dict(showgrid=True, gridcolor="rgba(41, 73, 67, 0.12)", ticksuffix="%"),
        yaxis=dict(showgrid=True, gridcolor="rgba(41, 73, 67, 0.12)", tickprefix="$", tickformat=",.0f"),
    )
    st.plotly_chart(fig, width="stretch")
    if has_total:
        st.caption(
            "Each dot is a Baltimore City census tract. X = Black population share; Y = FFIEC median "
            "property value for Black applicants; bubble size = tangled-title properties per 1,000 "
            "properties (ACS 2019 5-year B25003_001 occupied housing units as denominator, matching "
            "`20260505_healthoutcomes_explore`). Tracts with missing FFIEC values for Black applicants "
            "are dropped."
        )
    else:
        st.caption(
            "Each dot is a Baltimore City census tract. X = Black population share; Y = FFIEC median "
            "property value for Black applicants; bubble size = tangled-title property count (fallback). "
            "Tracts with missing FFIEC values for Black applicants are dropped."
        )


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
        hover_data["intersectionality_group"] = True

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
            "intersectionality_group": "Intersectionality group",
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

    # Four filled quadrants with dividing lines.
    quadrants = [
        ("Contemporary Advantage", 0.0, 0.5, 0.5, 1.0, "High Redlining (Disadvantage)", "High Socioeconomic Status"),
        ("Sustained Advantage", 0.5, 1.0, 0.5, 1.0, "No Redlining (Advantage)", "High Socioeconomic Status"),
        ("Sustained Disadvantage", 0.0, 0.5, 0.0, 0.5, "High Redlining (Disadvantage)", "Low Socioeconomic Status"),
        ("Previous Advantage", 0.5, 1.0, 0.0, 0.5, "No Redlining (Advantage)", "Low Socioeconomic Status"),
    ]
    group_color_key = {
        "Contemporary Advantage": "Contemporary advantage",
        "Sustained Advantage": "Sustained advantage",
        "Sustained Disadvantage": "Sustained disadvantage",
        "Previous Advantage": "Previous advantage",
    }
    text_color = {
        "Contemporary Advantage": "#ffffff",
        "Sustained Advantage": "#101010",
        "Sustained Disadvantage": "#ffffff",
        "Previous Advantage": "#ffffff",
    }

    for title, x0, x1, y0, y1, line2, line3 in quadrants:
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
            y=cy + 0.12,
            text=f"<b><u>{title}</u></b>",
            showarrow=False,
            font=dict(size=17, color=text_color[title], family="Source Sans Pro, sans-serif"),
        )
        fig.add_annotation(
            x=cx,
            y=cy + 0.03,
            text=f"<b>{line2}</b>",
            showarrow=False,
            font=dict(size=13, color=text_color[title], family="Source Sans Pro, sans-serif"),
        )
        fig.add_annotation(
            x=cx,
            y=cy - 0.07,
            text=f"<b>{line3}</b>",
            showarrow=False,
            font=dict(size=13, color=text_color[title], family="Source Sans Pro, sans-serif"),
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
        font=dict(size=18, color="#6d3c1d", family="Source Sans Pro, sans-serif"),
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
        font=dict(size=11, color="#101010", family="Source Sans Pro, sans-serif"),
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
        font=dict(size=11, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="right",
        yanchor="middle",
    )
    fig.add_annotation(
        x=0.5,
        y=-0.046,
        text="<b>Historical Redlining</b>",
        showarrow=False,
        font=dict(size=17, color="#9a2f23", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )
    fig.add_annotation(
        x=0.18,
        y=-0.10,
        text="<b>Disadvantage</b><br>(HOLC Grades C/D)",
        showarrow=False,
        font=dict(size=11, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )
    fig.add_annotation(
        x=0.82,
        y=-0.10,
        text="<b>Advantage</b><br>(HOLC Grades A/B)",
        showarrow=False,
        font=dict(size=11, color="#101010", family="Source Sans Pro, sans-serif"),
        xanchor="center",
        yanchor="top",
    )

    fig.update_xaxes(range=[-0.22, 1.06], visible=False, fixedrange=True)
    fig.update_yaxes(range=[-0.24, 1.06], visible=False, fixedrange=True)
    fig.update_layout(
        height=_QUADRANT_GROUP_MAP_ROW_FIG_HEIGHT_PX,
        margin=dict(l=132, r=36, t=24, b=106),
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
        st.warning("No overlapping tracts to map for intersectionality groups.")
        return

    map_data["intersectionality_group"] = map_data["intersectionality_group"].fillna("Excluded from analysis")
    map_data["intersectionality_group"] = pd.Categorical(
        map_data["intersectionality_group"], categories=GROUP_ORDER, ordered=False
    )

    map_fig = px.choropleth_map(
        map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color="intersectionality_group",
        category_orders={"intersectionality_group": GROUP_ORDER},
        color_discrete_map=GROUP_COLORS,
        hover_name="GEOID",
        hover_data={
            "intersectionality_group": True,
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
        legend=dict(title="Group", orientation="h", yanchor="bottom", y=-0.12, x=0),
    )
    st.plotly_chart(map_fig, width="stretch")


def render_group_boxplots(tracts: pd.DataFrame | None) -> None:
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

    if {"tangled_properties", "total_properties"}.issubset(city.columns):
        denominator = city["total_properties"].where(city["total_properties"] > 0)
        city["tangled_properties_per_1000"] = (
            city["tangled_properties"] / denominator
        ) * 1000
    if {"at_risk_properties", "total_properties"}.issubset(city.columns):
        denominator = city["total_properties"].where(city["total_properties"] > 0)
        city["at_risk_properties_per_1000"] = (
            city["at_risk_properties"] / denominator
        ) * 1000

    metric_options = {
        "Tangled-title properties (count)": ("tangled_properties", "count", ":,.0f"),
        "At-risk properties (count)": ("at_risk_properties", "count", ":,.0f"),
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
        "Black population (%)": ("black_population_percentage", "%", ":.1f"),
        "Median property value, all (USD)": ("median_property_value_total", "$", ":,.0f"),
        "Median property value, Black (USD)": ("median_property_value_black", "$", ":,.0f"),
    }
    available = {label: spec for label, spec in metric_options.items() if spec[0] in city.columns}
    if not available:
        st.warning("No metrics available for boxplots.")
        return

    selected_label = st.selectbox(
        "Choose metric for the boxplot", list(available.keys()), key="group_boxplot_metric"
    )
    selected_col, axis_unit, _value_fmt = available[selected_label]

    plot_df = city.dropna(subset=["intersectionality_group", selected_col]).copy()
    if plot_df.empty:
        st.warning("No non-missing values to plot for the selected metric.")
        return
    plot_df["intersectionality_group"] = pd.Categorical(
        plot_df["intersectionality_group"], categories=GROUP_ORDER, ordered=True
    )
    plot_df = plot_df.sort_values("intersectionality_group")

    n_total = len(plot_df)
    group_counts = (
        plot_df.groupby("intersectionality_group", observed=True)
        .size()
        .reindex(GROUP_ORDER)
        .fillna(0)
        .astype(int)
    )

    fig = px.box(
        plot_df,
        x="intersectionality_group",
        y=selected_col,
        color="intersectionality_group",
        category_orders={"intersectionality_group": GROUP_ORDER},
        color_discrete_map=GROUP_COLORS,
        points="all",
        hover_data={
            "GEOID": True,
            "intersectionality_group": False,
            selected_col: True,
        },
        labels={
            "intersectionality_group": "Intersectionality group",
            selected_col: selected_label,
        },
        title=f"{selected_label} by intersectionality group (n = {n_total} tracts)",
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
        f"{group}<br><span style='font-size:11px;color:#5d6a64'>n={group_counts[group]}</span>"
        for group in GROUP_ORDER
    ]
    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=70, b=10),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        showlegend=False,
        title=dict(x=0.0, xanchor="left", font=dict(size=16, color="#18312d")),
        xaxis=dict(
            title="",
            showgrid=False,
            tickmode="array",
            tickvals=GROUP_ORDER,
            ticktext=xaxis_ticktext,
        ),
        yaxis=yaxis_kwargs,
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        f"Box = IQR with median line; dashed mark = mean. Each dot is a Baltimore City census tract; "
        f"y-axis shows {selected_label.lower()}. Tracts with missing values for the selected metric "
        "are dropped before counting."
    )


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
        The intersectionality framework used here (Uzzi et al., 2023) combines historical advantage (derived from HOLC legacy) with contemporary
        advantage (ICE-based segregation index) to classify each census tract into one of four groups shown below.  
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
    st.markdown("#### Four Intersectionality Groups")
    render_quadrant_diagram()
with group_hist_right:
    st.markdown("#### Tract distribution across Baltimore")
    render_intersectionality_group_map(tracts, geojson)

st.divider()

# =============================================================================
# H2: Impact of Historical Disadvantage and Contemporary Disadvantage
# =============================================================================

_quant_section_h2(
    "impact-of-historical-contemporary-disadvantage",
    "Impact of Historical Disadvantage and Contemporary Disadvantage",
)

# -----------------------------------------------------------------------------
# Scatter (left) + boxplots (right), under Impact of Historical / Contemporary Disadvantage H2
# -----------------------------------------------------------------------------
scatter_col, boxplot_col = st.columns(2, gap="medium")
with scatter_col:
    st.markdown("### Black population share and median property value for Black applicants")
    st.markdown(
        "Bubble size reflects tangled-title properties per 1,000 total properties."
    )
    render_black_homeownership_chart(tracts)
with boxplot_col:
    st.markdown("### Metric distributions by intersectionality group")
    st.caption(
        "Compare how tract-level metrics vary across the four intersectionality groups."
    )
    render_group_boxplots(tracts)

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
