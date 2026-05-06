from pathlib import Path

import pandas as pd
import streamlit as st

from shared_style import apply_theme


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
QUANT_DIR = DATA_DIR / "quant"
P5_TABLE = QUANT_DIR / "p5_publication_style_table.csv"


st.set_page_config(page_title="Synthesis", layout="wide")
apply_theme()


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def fmt_money(value: float | int | str) -> str:
    try:
        if pd.isna(value):
            return "NA"
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "NA"


def clean_display_table(df: pd.DataFrame) -> pd.DataFrame:
    display = df.copy()
    for col in display.columns:
        if display[col].isna().all():
            display = display.drop(columns=[col])
    if "Median household income ($)" in display.columns:
        display["Median household income ($)"] = display["Median household income ($)"].apply(fmt_money)
    return display


matrix = load_csv(DATA_DIR / "synthesis_matrix.csv")
themes = load_csv(DATA_DIR / "themes.csv")
nodes = load_csv(DATA_DIR / "nodes.csv")
quant_profile = load_csv(P5_TABLE)

st.title("Synthesis: How the Evidence Fits Together")
st.markdown(
    """
    This page is the integration layer of the site. It connects interview themes,
    power-map pathways, and neighborhood-level quantitative patterns into a shared
    explanatory framework for tangled titles in Baltimore.
    """
)

st.markdown("### Shared Explanatory Framework")
st.markdown(
    """
    <div class="soft-card">
    <h3>Core pathway</h3>
    <p><strong>Homeowner dies</strong> -> deed is not updated -> ownership becomes legally unclear ->
    residents face barriers to repairs, loans, tax relief, sale, or inheritance planning ->
    housing stability and intergenerational wealth are put at risk.</p>
    <p>The evidence does not point to one single cause. It shows a system where family decisions,
    legal documentation, service access, administrative rules, and neighborhood conditions interact.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Evidence Integration Matrix")
st.caption(
    "Use this matrix as the presentation spine: each row connects qualitative evidence, power-map logic, "
    "quantitative context, interpretation, and an intervention entry point."
)

if matrix.empty:
    st.warning("The synthesis matrix file is missing.")
else:
    domains = ["All domains"] + matrix["domain"].tolist()
    selected_domain = st.selectbox("Filter by synthesis domain", domains)
    shown = matrix if selected_domain == "All domains" else matrix[matrix["domain"] == selected_domain]
    st.dataframe(shown, width="stretch", hide_index=True)

st.markdown("### Theme-to-System Linkages")
if themes.empty or nodes.empty:
    st.warning("Theme or power-map node files are missing.")
else:
    selected_theme = st.selectbox("Select an interview theme", themes["theme"].tolist())
    theme = themes.loc[themes["theme"] == selected_theme].iloc[0]
    connected_ids = [
        item.strip()
        for item in str(theme.get("connected_nodes", "")).split(";")
        if item.strip()
    ]
    connected_nodes = nodes[nodes["node_id"].isin(connected_ids)].copy()

    left, right = st.columns([1, 1.3])
    with left:
        st.markdown(
            f"""
            <div class="soft-card">
            <h3>{theme["theme"]}</h3>
            <p>{theme["summary"]}</p>
            <p><strong>Evidence:</strong> {theme.get("evidence_note", "Qualitative and mapping evidence")}</p>
            <p><strong>Intervention meaning:</strong> {theme.get("intervention_meaning", "Use this theme to locate practical entry points.")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("#### Related Power-Map Nodes")
        if connected_nodes.empty:
            st.info("No connected node IDs are listed for this theme yet.")
        else:
            st.dataframe(
                connected_nodes[["label", "level", "type", "evidence_source", "description"]],
                width="stretch",
                hide_index=True,
            )

st.markdown("### Cross-Evidence Interpretation")
cols = st.columns(3)
cards = [
    (
        "What interviews add",
        "Interviews explain how residents experience uncertainty: family disagreement, legal confusion, cost, distrust, and difficulty knowing where to start.",
    ),
    (
        "What the power map adds",
        "The power map shows where barriers sit in the system: individual knowledge, family inheritance, courts, agencies, legal services, tax sale processes, and community organizations.",
    ),
    (
        "What quantitative evidence adds",
        "Quantitative outputs show spatial concentration and neighborhood-level context. They help describe where vulnerabilities overlap, without claiming individual-level causation.",
    ),
]
for column, (title, body) in zip(cols, cards):
    with column:
        st.markdown(
            f"""
            <div class="soft-card" style="min-height:190px;">
            <h3>{title}</h3>
            <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Neighborhood Context Used in the Synthesis")
if quant_profile.empty:
    st.info("Neighborhood group context is not loaded yet.")
else:
    display_quant = clean_display_table(quant_profile)
    st.caption(
        "These group-level indicators are used only as context for synthesis. The non-fatal shooting rate "
        "field is not shown when it is entirely missing."
    )
    st.dataframe(display_quant, width="stretch", hide_index=True)

    q = quant_profile.set_index("intersectional_group")
    if "Sustained disadvantage" in q.index:
        row = q.loc["Sustained disadvantage"]
        st.info(
            "For presentation: the sustained disadvantage group combines higher vacancy, lower median household "
            "income, lower college education, and higher Black resident share in the currently available P5 table. "
            "Use this as neighborhood context, not as proof that tangled titles cause these conditions."
        )

st.markdown("### Intervention Entry Points")
intervention_cards = [
    (
        "Residents",
        "Clear, trusted guidance before and after a homeowner dies: deed transfer, probate navigation, estate planning, tax sale prevention, and repair eligibility.",
    ),
    (
        "Community organizations",
        "Outreach and navigation in neighborhoods where legal, financial, and service barriers overlap.",
    ),
    (
        "Legal services",
        "Prioritize unclear heirs, probate bottlenecks, deed clinics, and low-cost title-clearing support.",
    ),
    (
        "Policy and administration",
        "Reduce documentation bottlenecks and make ownership proof less confusing across courts, agencies, tax sale systems, and benefit programs.",
    ),
]
columns = st.columns(4)
for column, (title, body) in zip(columns, intervention_cards):
    with column:
        st.markdown(
            f"""
            <div class="soft-card" style="min-height:190px;">
            <h3>{title}</h3>
            <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Final Narrative")
st.success(
    "The synthesis story is that tangled titles are not only a paperwork problem. They are produced "
    "through interacting legal, family, service, economic, and neighborhood pathways. The strongest "
    "deliverable is a platform that shows where those pathways converge and where intervention can happen."
)
