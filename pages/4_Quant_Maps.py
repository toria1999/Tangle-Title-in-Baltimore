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

TRACT_METRICS = QUANT_DIR / "tract_intersectional_group_merged.csv"
BALTIMORE_TRACTS_GEOJSON = QUANT_DIR / "baltimore_tracts.geojson"
P5_TABLE = QUANT_DIR / "p5_publication_style_table.csv"
ACS_TABLE = QUANT_DIR / "acs_acs5_2019_tract_baltimore_city_md_ice_input_derived.csv"
SHOOTING_POINTS = QUANT_DIR / "Part1_Crime_Beta_9S(shooting).geojson"
FIGURE_DIRS = [QUANT_DIR / "figures", QUANT_DIR / "svg_output"]

GROUP_COLORS = {
    "Sustained advantage": "#a9c77b",
    "Contemporary advantage": "#f0c56a",
    "Previous advantage": "#e58b60",
    "Sustained disadvantage": "#8f3d46",
    "Excluded from analysis": "#b9b9b9",
    "Baltimore city average": "#294943",
}

FIGURE_NOTES = {
    "plot_1.png": {
        "title": "Where tangled-title and at-risk properties are concentrated",
        "caption": (
            "This side-by-side map compares counts of tangled-title properties and at-risk "
            "properties by Baltimore City census tract. Darker colors indicate more properties. "
            "Use it to see spatial concentration, not to infer why a tract has a higher count."
        ),
    },
    "plot_2_tangled_to_at_risk.png": {
        "title": "Current burden relative to future risk",
        "caption": (
            "This map shows the ratio of tangled-title properties to at-risk properties. Higher "
            "values mean a tract has relatively more current tangled-title burden than future "
            "risk. Gray areas indicate missing or unavailable ratio values."
        ),
    },
    "plot_2_at_risk_to_tangled.png": {
        "title": "Future risk relative to current burden",
        "caption": (
            "This map shows the ratio of at-risk properties to tangled-title properties. Higher "
            "values mean a tract has relatively more future risk than current tangled-title burden. "
            "Gray areas indicate missing or unavailable ratio values."
        ),
    },
    "plot_3.png": {
        "title": "Estimated property wealth exposure",
        "caption": (
            "This map compares estimated net equity tied to tangled-title and at-risk properties. "
            "Red indicates positive estimated net equity and blue indicates negative estimated net "
            "equity. Net equity should be read as estimated property wealth affected, not cash on hand."
        ),
    },
    "plot_4.png": {
        "title": "Negative-equity share",
        "caption": (
            "This map shows where negative equity makes up a larger share of tract-level exposure. "
            "It helps flag where property wealth may be more financially fragile. It is still a "
            "tract-level descriptive measure."
        ),
    },
    "plot_5.png": {
        "title": "Data availability check",
        "caption": (
            "This map shows where gross negative equity values are observed or missing. It should be "
            "used as a caution when interpreting the equity maps, because missing data can affect "
            "what the visual evidence can support."
        ),
    },
    "intersectional_group_x_black_pct_of_pop.svg": {
        "title": "Black resident share by neighborhood group",
        "caption": (
            "This figure compares the Black resident percentage across neighborhood groups. It "
            "contextualizes the tract groups demographically without making individual-level claims."
        ),
    },
    "places_casthma_boxplot.svg": {
        "title": "PLACES asthma indicator by neighborhood group",
        "caption": (
            "This figure compares tract-level PLACES asthma indicators across neighborhood groups. "
            "PLACES indicators are contextual measures and should not be interpreted as individual "
            "health effects of tangled titles."
        ),
    },
    "places_casthma_map.svg": {
        "title": "PLACES asthma indicator map",
        "caption": (
            "This map shows a tract-level PLACES asthma indicator. It is useful as neighborhood "
            "context only; it does not show that tangled titles cause asthma or any health outcome."
        ),
    },
}


st.set_page_config(page_title="Quantitative Evidence", layout="wide")
apply_theme()


@st.cache_data(show_spinner=False)
def load_p5_table(_mtime: float | None = None) -> pd.DataFrame:
    return pd.read_csv(P5_TABLE)


@st.cache_data(show_spinner=False)
def load_tract_metrics(_mtime: float | None = None) -> pd.DataFrame | None:
    if not TRACT_METRICS.exists():
        return None
    df = pd.read_csv(TRACT_METRICS)
    if "GEOID" in df.columns:
        df["GEOID"] = df["GEOID"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(11)
    if "at_risk_properties" in df.columns and "tangled_properties" in df.columns:
        denominator = df["at_risk_properties"].where(df["at_risk_properties"] > 0)
        df["tangled_to_at_risk_ratio"] = df["tangled_properties"] / denominator
    return df


@st.cache_data(show_spinner=False)
def load_acs_context(_mtime: float | None = None) -> pd.DataFrame | None:
    if not ACS_TABLE.exists():
        return None
    df = pd.read_csv(ACS_TABLE)
    if "GEOID" in df.columns:
        df["GEOID"] = df["GEOID"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(11)
    return df


@st.cache_data(show_spinner=False)
def load_geojson(_mtime: float | None = None) -> dict | None:
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


def clean_group_context(df: pd.DataFrame) -> pd.DataFrame:
    display = df.copy()
    for col in display.columns:
        if display[col].isna().all():
            display = display.drop(columns=[col])
    return display


def baltimore_city_tracts(tracts: pd.DataFrame | None) -> pd.DataFrame:
    if tracts is None:
        return pd.DataFrame()
    if "county_name" in tracts.columns:
        city = tracts[tracts["county_name"].astype(str).str.contains("Baltimore city", na=False)].copy()
        if not city.empty:
            return city
    if "GEOID" in tracts.columns:
        return tracts[tracts["GEOID"].astype(str).str.startswith("24510")].copy()
    return tracts.copy()


def merge_acs_context(tracts: pd.DataFrame | None, acs: pd.DataFrame | None) -> pd.DataFrame:
    if tracts is None:
        return pd.DataFrame()
    out = tracts.copy()
    if acs is None or "GEOID" not in out.columns or "GEOID" not in acs.columns:
        return out
    context_cols = [
        col
        for col in [
            "total_population",
            "vacant_housing_pct",
            "college_educated_pct",
            "black_residents_pct",
            "median_household_income",
            "ice_income_households",
            "ice_poverty_mixed",
        ]
        if col in acs.columns and col not in out.columns
    ]
    if not context_cols:
        return out
    return out.merge(acs[["GEOID", *context_cols]], on="GEOID", how="left")


def find_figures() -> list[Path]:
    figures: list[Path] = []
    for directory in FIGURE_DIRS:
        if directory.exists():
            for pattern in ("*.png", "*.svg", "*.jpg", "*.jpeg"):
                figures.extend(sorted(directory.glob(pattern)))
    return sorted(figures)


def render_quadrant_diagram() -> None:
    fig = go.Figure()
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=0, y1=1, line=dict(color="#294943", width=2))
    fig.add_shape(type="line", x0=0, x1=1, y0=0.5, y1=0.5, line=dict(color="#294943", width=2))
    quadrants = [
        ("Sustained advantage", 0.75, 0.75, "Historically advantaged + currently advantaged", "#a9c77b"),
        ("Contemporary advantage", 0.75, 0.25, "Currently advantaged, less historically advantaged", "#f0c56a"),
        ("Previous advantage", 0.25, 0.75, "Historically advantaged, less currently advantaged", "#e58b60"),
        ("Sustained disadvantage", 0.25, 0.25, "Historically disadvantaged + currently disadvantaged", "#8f3d46"),
    ]
    for group, x, y, note, color in quadrants:
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=dict(size=28, color=color, line=dict(width=2, color="#294943")),
                hovertemplate=f"<b>{group}</b><br>{note}<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_annotation(x=x, y=y + 0.10, text=f"<b>{group}</b>", showarrow=False, font=dict(size=15))
        fig.add_annotation(x=x, y=y - 0.13, text=note, showarrow=False, font=dict(size=12), opacity=0.9)
    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#fff9e6",
        paper_bgcolor="#fff9e6",
        xaxis=dict(
            title="Current neighborhood advantage",
            range=[0, 1],
            tickvals=[0.25, 0.75],
            ticktext=["Lower", "Higher"],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            title="Historical neighborhood advantage",
            range=[0, 1],
            tickvals=[0.25, 0.75],
            ticktext=["Lower", "Higher"],
            showgrid=False,
            zeroline=False,
        ),
    )
    st.plotly_chart(fig, width="stretch")


def render_metric_cards(tracts: pd.DataFrame | None) -> None:
    if tracts is None:
        st.info(
            "The full tract-level table is not loaded in this local site yet. The maps below are "
            "shown as precomputed figure outputs rather than a live tract explorer."
        )
        return

    baltimore = baltimore_city_tracts(tracts)
    cards = [
        ("Census tracts included", len(baltimore), fmt_int),
        ("Tracts with tangled-title properties", (baltimore["tangled_properties"] > 0).sum(), fmt_int),
        ("Tangled-title properties", baltimore["tangled_properties"].sum(skipna=True), fmt_int),
        ("At-risk properties", baltimore["at_risk_properties"].sum(skipna=True), fmt_int),
        ("Estimated tangled net equity", baltimore["tangled_net_equity"].sum(skipna=True), fmt_money),
        ("Estimated at-risk net equity", baltimore["at_risk_net_equity"].sum(skipna=True), fmt_money),
    ]
    cols = st.columns(3)
    for idx, (label, value, formatter) in enumerate(cards):
        with cols[idx % 3]:
            st.metric(label, formatter(value))


def render_interactive_map(tracts: pd.DataFrame | None, geojson: dict | None) -> None:
    if tracts is None or geojson is None:
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

    st.markdown("### Interactive Tract Explorer")
    st.caption(
        "Use this live map to inspect one metric at a time. It is separate from the static figure "
        "outputs below, which preserve the quantitative team's finished visuals."
    )
    metric_options = {
        "Tangled-title properties": "tangled_properties",
        "At-risk properties": "at_risk_properties",
        "Tangled / at-risk ratio": "tangled_to_at_risk_ratio",
        "Tangled net equity": "tangled_net_equity",
        "At-risk net equity": "at_risk_net_equity",
    }
    available = {label: col for label, col in metric_options.items() if col in tracts.columns}
    selected_label = st.selectbox("Choose tract metric", list(available.keys()))
    selected_col = available[selected_label]
    map_fig = px.choropleth_map(
        map_data,
        geojson=geojson,
        locations="GEOID",
        featureidkey="properties.GEOID",
        color=selected_col,
        hover_name="tract_name" if "tract_name" in tracts.columns else "GEOID",
        hover_data={
            "tangled_properties": ":,.0f" if "tangled_properties" in tracts.columns else False,
            "at_risk_properties": ":,.0f" if "at_risk_properties" in tracts.columns else False,
            "intersectional_group": True if "intersectional_group" in tracts.columns else False,
        },
        color_continuous_scale=["#fff7dc", "#efc267", "#a9c77b", "#294943"],
        map_style="carto-positron",
        center={"lat": 39.299, "lon": -76.61},
        zoom=10,
        opacity=0.78,
        height=560,
    )
    map_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(map_fig, width="stretch")


def render_group_summary(tracts: pd.DataFrame | None) -> None:
    city = baltimore_city_tracts(tracts)
    if city.empty or "intersectional_group" not in city.columns:
        return
    st.markdown("### Tract Burden by Neighborhood Group")
    grouped = (
        city.dropna(subset=["intersectional_group"])
        .groupby("intersectional_group", dropna=False)
        .agg(
            tracts=("GEOID", "nunique"),
            total_tangled_properties=("tangled_properties", "sum"),
            mean_tangled_properties=("tangled_properties", "mean"),
            total_at_risk_properties=("at_risk_properties", "sum"),
            mean_at_risk_properties=("at_risk_properties", "mean"),
            total_tangled_net_equity=("tangled_net_equity", "sum"),
            total_at_risk_net_equity=("at_risk_net_equity", "sum"),
        )
        .reset_index()
    )
    display = grouped.copy()
    for col in ["mean_tangled_properties", "mean_at_risk_properties"]:
        display[col] = display[col].map(lambda value: f"{value:,.1f}")
    for col in ["total_tangled_properties", "total_at_risk_properties", "tracts"]:
        display[col] = display[col].map(fmt_int)
    for col in ["total_tangled_net_equity", "total_at_risk_net_equity"]:
        display[col] = display[col].map(fmt_money)
    display = display.rename(
        columns={
            "intersectional_group": "Neighborhood group",
            "tracts": "Census tracts",
            "total_tangled_properties": "Tangled-title properties",
            "mean_tangled_properties": "Mean tangled-title properties per tract",
            "total_at_risk_properties": "At-risk properties",
            "mean_at_risk_properties": "Mean at-risk properties per tract",
            "total_tangled_net_equity": "Estimated tangled net equity",
            "total_at_risk_net_equity": "Estimated at-risk net equity",
        }
    )
    st.dataframe(display, width="stretch", hide_index=True)
    chart = px.bar(
        grouped,
        x="intersectional_group",
        y=["total_tangled_properties", "total_at_risk_properties"],
        barmode="group",
        color_discrete_sequence=["#8a5a35", "#a9c77b"],
        title="Tangled-title and at-risk properties by neighborhood group",
    )
    chart.update_layout(xaxis_title="", yaxis_title="Property count", legend_title="")
    st.plotly_chart(chart, width="stretch")
    st.caption("Data vintage: tract-level tangled-title and at-risk property outputs dated March 2026.")


def render_highest_burden_table(tracts: pd.DataFrame | None, acs: pd.DataFrame | None) -> None:
    city = baltimore_city_tracts(merge_acs_context(tracts, acs))
    if city.empty:
        return
    st.markdown("### Highest-Burden Tracts")
    st.caption(
        "This table shows tract-level summaries only. It excludes owner names, addresses, parcel IDs, and other identifying records."
    )
    ranking_options = {
        "Tangled-title properties": "tangled_properties",
        "At-risk properties": "at_risk_properties",
        "Tangled net equity": "tangled_net_equity",
        "At-risk net equity": "at_risk_net_equity",
        "Tangled / at-risk ratio": "tangled_to_at_risk_ratio",
    }
    available = {label: col for label, col in ranking_options.items() if col in city.columns}
    selected = st.selectbox("Rank tracts by", list(available.keys()))
    rank_col = available[selected]
    safe_cols = [
        col
        for col in [
            "GEOID",
            "tract_name",
            "tangled_properties",
            "at_risk_properties",
            "tangled_to_at_risk_ratio",
            "tangled_net_equity",
            "at_risk_net_equity",
            "intersectional_group",
            "black_residents_pct",
            "vacant_housing_pct",
            "college_educated_pct",
            "median_household_income",
        ]
        if col in city.columns
    ]
    table = city.sort_values(rank_col, ascending=False, na_position="last")[safe_cols].head(25).copy()
    rename = {
        "tract_name": "Tract",
        "tangled_properties": "Tangled-title properties",
        "at_risk_properties": "At-risk properties",
        "tangled_to_at_risk_ratio": "Tangled / at-risk ratio",
        "tangled_net_equity": "Estimated tangled net equity",
        "at_risk_net_equity": "Estimated at-risk net equity",
        "intersectional_group": "Neighborhood group",
        "black_residents_pct": "Black residents (%)",
        "vacant_housing_pct": "Vacant housing (%)",
        "college_educated_pct": "College educated (%)",
        "median_household_income": "Median household income",
    }
    table = table.rename(columns=rename)
    for col in ["Estimated tangled net equity", "Estimated at-risk net equity", "Median household income"]:
        if col in table.columns:
            table[col] = table[col].map(fmt_money)
    if "Tangled / at-risk ratio" in table.columns:
        table["Tangled / at-risk ratio"] = table["Tangled / at-risk ratio"].map(
            lambda value: "NA" if pd.isna(value) else f"{value:,.2f}"
        )
    st.dataframe(table, width="stretch", hide_index=True)


def render_figure(path: Path) -> None:
    note = FIGURE_NOTES.get(
        path.name,
        {
            "title": path.stem.replace("_", " ").replace("-", " ").title(),
            "caption": (
                "This precomputed output provides neighborhood-level quantitative context. Read it "
                "descriptively, not as an individual-level causal claim."
            ),
        },
    )
    st.markdown(f"#### {note['title']}")
    st.image(str(path), use_container_width=True)
    st.caption(f"{note['caption']} Data vintage: tract counts/equity file dated March 2026 unless noted otherwise.")


p5 = load_p5_table(file_mtime(P5_TABLE))
tracts = load_tract_metrics(file_mtime(TRACT_METRICS))
acs = load_acs_context(file_mtime(ACS_TABLE))
geojson = load_geojson(file_mtime(BALTIMORE_TRACTS_GEOJSON))

st.title("Quantitative Evidence")
st.markdown(
    """
    This section summarizes precomputed quantitative outputs from the Tangled Titles in Baltimore
    project. The goal is to identify spatial concentration and overlapping neighborhood-level
    vulnerabilities, not to estimate individual-level causal effects.
    """
)
st.caption(
    "Data timing: tract-level tangled-title and at-risk property outputs are dated March 2026; "
    "the neighborhood group validation field in the group-merged table is dated May 5, 2026 where "
    "that file is available; ACS demographic context uses 2019 ACS 5-year derived tract data."
)

st.markdown("### Key Quantitative Takeaways")
st.markdown(
    """
    - The strongest evidence on this page is descriptive and tract-level.
    - The finished maps show spatial concentration in tangled-title counts, at-risk property counts, ratios, and estimated net equity exposure.
    - The neighborhood group table helps describe how housing, income, education, and race-related context overlap across tract groups.
    - PLACES health indicators, where shown, are contextual tract-level indicators only.
    """
)

st.markdown("### Neighborhood Group Framework")
st.markdown(
    """
    The four-quadrant framework organizes census tracts by historical and contemporary neighborhood
    advantage. These groups are descriptive categories for comparing overlapping vulnerabilities,
    not causal categories.
    """
)
render_quadrant_diagram()
q1, q2, q3, q4 = st.columns(4)
quadrant_cards = [
    (q1, "Sustained advantage", "Higher historical advantage and higher current advantage."),
    (q2, "Contemporary advantage", "Higher current advantage, but lower historical advantage."),
    (q3, "Previous advantage", "Higher historical advantage, but lower current advantage."),
    (q4, "Sustained disadvantage", "Lower historical advantage and lower current advantage."),
]
for column, group, description in quadrant_cards:
    with column:
        st.markdown(
            f"""
            <div class="soft-card">
            <h3>{group}</h3>
            <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Group-Level Context")
display_p5 = clean_group_context(p5)
if "Median household income ($)" in display_p5.columns:
    display_p5["Median household income ($)"] = display_p5["Median household income ($)"].apply(fmt_money)
st.dataframe(display_p5, width="stretch", hide_index=True)
if "Non-fatal shooting rate" in p5.columns and p5["Non-fatal shooting rate"].isna().all():
    st.caption(
        "Non-fatal shooting rate is omitted because the current group summary table has no filled values for that field."
    )

chart_df = p5[p5["intersectional_group"] != "Baltimore city average"].copy()
left, right = st.columns(2)
with left:
    fig_income = px.bar(
        chart_df,
        x="intersectional_group",
        y="Median household income ($)",
        color="intersectional_group",
        color_discrete_map=GROUP_COLORS,
        title="Median household income by group",
    )
    fig_income.update_layout(xaxis_title="", yaxis_title="Median household income", showlegend=False)
    st.plotly_chart(fig_income, width="stretch")
    st.caption("Data vintage: ACS 2019 5-year derived tract indicators summarized by neighborhood group.")

with right:
    fig_context = px.scatter(
        chart_df,
        x="Black residents percentage",
        y="Vacant housing percentage",
        size="College educated percentage",
        color="intersectional_group",
        color_discrete_map=GROUP_COLORS,
        hover_data={"Median household income ($)": ":$,.0f", "College educated percentage": ":.1f"},
        title="Vacancy, Black residents, and college education by group",
    )
    fig_context.update_layout(xaxis_title="Black residents (%)", yaxis_title="Vacant housing (%)")
    fig_context.update_traces(marker=dict(sizemin=8, line=dict(width=1, color="#294943"), opacity=0.82))
    st.plotly_chart(fig_context, width="stretch")
    st.caption("Data vintage: ACS 2019 5-year derived tract indicators summarized by neighborhood group.")

st.markdown("### Burden and Equity Evidence")
render_metric_cards(tracts)
render_interactive_map(tracts, geojson)
render_group_summary(tracts)
render_highest_burden_table(tracts, acs)

figures = find_figures()
if figures:
    spatial = [f for f in figures if f.suffix.lower() == ".png"]
    context = [f for f in figures if f.suffix.lower() == ".svg"]
    tabs = st.tabs(["Spatial burden maps", "Contextual indicators"])
    with tabs[0]:
        for figure in spatial:
            render_figure(figure)
    with tabs[1]:
        for figure in context:
            render_figure(figure)
else:
    st.info("No precomputed figure outputs are currently available in the local quantitative folder.")

st.markdown("### Non-Fatal Shooting Rate Status")
if SHOOTING_POINTS.exists():
    st.info(
        "The raw shooting incident point file is available locally, but the website does not display it directly. "
        "To show a non-fatal shooting rate responsibly, the point data should first be aggregated to census tracts "
        "and divided by tract population in the analysis workflow."
    )
else:
    st.info(
        "A tract-level non-fatal shooting rate is not available in the current summary table. Add a precomputed "
        "tract or group summary before displaying this metric."
    )

st.markdown("### Methods and Limitations")
st.markdown(
    """
    <div class="soft-card">
    <p>This page reads precomputed outputs and does not rerun the full R analysis pipeline.</p>
    <p>Most results are census-tract-level descriptive outputs. Ecological and temporal limitations apply.</p>
    <p>Net equity estimates should be interpreted as estimated property wealth affected, not immediately
    available cash, legal damages, or individual household resources.</p>
    <p>Address-level, owner-level, and parcel-level records are not displayed.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
