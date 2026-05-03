from pathlib import Path

import pandas as pd
import streamlit as st

from shared_style import apply_theme


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


st.set_page_config(page_title="Synthesis Matrix", layout="wide")

apply_theme()


@st.cache_data
def load_matrix():
    return pd.read_csv(DATA_DIR / "synthesis_matrix.csv")


matrix = load_matrix()

st.title("Synthesis Matrix and Intervention Entry Points")
st.markdown(
    """
    The matrix compares interview evidence, power map evidence, and quantitative
    patterns to produce a shared interpretation for presentation and community use.
    """
)

domains = ["All domains"] + matrix["domain"].tolist()
selected_domain = st.selectbox("Filter by domain", domains)

shown = matrix if selected_domain == "All domains" else matrix[matrix["domain"] == selected_domain]

st.dataframe(shown, width="stretch", hide_index=True)

st.markdown("### Intervention Entry Points")

col1, col2, col3, col4 = st.columns(4)

cards = [
    (
        "For Residents",
        "Clarify where to seek help for probate navigation, deed transfer, tax sale prevention, and repair eligibility.",
    ),
    (
        "For CBOs",
        "Target outreach to high-risk domains and translate formal systems into practical next steps.",
    ),
    (
        "For Legal Services",
        "Prioritize knowledge gaps, unclear heirs, and administrative processes that block ownership proof.",
    ),
    (
        "For Policymakers",
        "Identify bottlenecks where eligibility rules and documentation requirements amplify property loss risk.",
    ),
]

for column, (title, body) in zip([col1, col2, col3, col4], cards):
    with column:
        st.markdown(
            f"""
            <div class="soft-card" style="min-height:180px;">
            <h3 style="font-size:1.05rem;margin-top:0;">{title}</h3>
            <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Final Takeaway")
st.success(
    "Tangled titles are not only a documentation problem. They are produced through "
    "interacting legal, family, service, economic, and structural pathways. The "
    "strongest synthesis product shows where those pathways converge and where "
    "intervention can reduce housing instability and wealth loss."
)
