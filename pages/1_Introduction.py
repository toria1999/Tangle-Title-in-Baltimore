import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_style import apply_theme, render_page_toc, section_h2, support_badge
from tangled_titles_content import GLOSSARY_TERMS, PROBLEM_PATHWAY_DETAIL, TITLE_COMPARISON


st.set_page_config(page_title="Introduction", layout="wide")

apply_theme()

support_badge()

INTRODUCTION_TOC = (
    ("key-terms", "Key Terms"),
    ("clear-vs-tangled-title", "Clear vs Tangled Title"),
    ("resident-pathway", "Resident Pathway"),
    ("synthesis-question", "Synthesis Question"),
    ("evidence-streams", "Evidence Streams"),
    ("use-this-site-to", "Use This Site To"),
)

render_page_toc("introduction", INTRODUCTION_TOC)

st.title("Introduction")

st.markdown(
    """
    This platform frames tangled titles as a system-level housing stability issue:
    a resident may live in and maintain a family home, but still lack the formal
    documentation required by legal, financial, and government systems.
    """
)

section_h2("key-terms", "Key Terms / Keyword Guide")
st.markdown(
    """
    These terms appear across the site. The definitions below are intentionally
    plain-language starting points, not legal advice.
    """
)
glossary_query = st.text_input("Search key terms", placeholder="probate, deed, tax sale, legal aid...")
filtered_terms = [
    item
    for item in GLOSSARY_TERMS
    if not glossary_query.strip()
    or glossary_query.lower() in " ".join(item).lower()
]
for idx in range(0, len(filtered_terms), 2):
    cols = st.columns(2)
    for col, term_item in zip(cols, filtered_terms[idx : idx + 2]):
        term, definition, why_it_matters = term_item
        with col:
            with st.expander(term, expanded=False):
                st.markdown(definition)
                st.caption(f"Why it matters: {why_it_matters}")

section_h2("clear-vs-tangled-title", "Clear Title vs Tangled Title")
clear_col, tangled_col = st.columns(2)
with clear_col:
    st.markdown(
        """
        <div class="evidence-card" style="border-top: 7px solid #4f8f5b;">
            <h3>Clear Title</h3>
            <p class="muted-note">Formal ownership and lived ownership line up.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for point in TITLE_COMPARISON["clear"]:
        st.success(point)
with tangled_col:
    st.markdown(
        """
        <div class="evidence-card" style="border-top: 7px solid #c96b68;">
            <h3>Tangled Title</h3>
            <p class="muted-note">The resident's lived relationship to the home is not fully recognized by legal records.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for point in TITLE_COMPARISON["tangled"]:
        st.warning(point)

section_h2("resident-pathway", "Resident Pathway")
st.markdown(
    """
    <div class="pathway-scene">
        <div class="scene-row">
            <div class="scene-step">
                <div class="mini-house"></div>
                <strong>Family Home</strong>
                <span>A homeowner dies and the house remains the family's main asset.</span>
            </div>
            <div class="scene-step">
                <div class="mini-doc"></div>
                <strong>Deed Not Updated</strong>
                <span>Informal inheritance does not automatically change legal ownership.</span>
            </div>
            <div class="scene-step">
                <div class="mini-doc" style="opacity:0.55;"></div>
                <strong>Unclear Ownership</strong>
                <span>The resident may live in the home but lack formal documentation.</span>
            </div>
            <div class="scene-step">
                <div class="mini-lock"></div>
                <strong>Blocked Access</strong>
                <span>Repairs, loans, tax relief, or sale can become harder to secure.</span>
            </div>
            <div class="scene-step">
                <div class="mini-wealth"></div>
                <strong>Wealth Loss Risk</strong>
                <span>Housing instability can interrupt wealth preservation across generations.</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Detailed pathway behind the visual", expanded=False):
    for idx, step in enumerate(PROBLEM_PATHWAY_DETAIL, start=1):
        st.markdown(f"**{idx}. {step}**")

st.write("")

col1, col2 = st.columns([1.1, 0.9])

with col1:
    section_h2("synthesis-question", "Synthesis Question")
    st.markdown(
        """
        How do individual knowledge gaps, family inheritance processes, service
        access, administrative systems, and neighborhood-level inequities interact
        to shape tangled title risk in Baltimore?
        """
    )

    section_h2("evidence-streams", "Evidence Streams")
    st.markdown(
        """
        - **Resident journey:** a fictional composite pathway showing how title problems become visible.
        - **Quant analysis:** tract-level patterns in title risk and wealth context.
        - **Interviews:** lived experience, service navigation, institutional trust.
        - **Power mapping:** actors, barriers, facilitators, and intervention points.
        - **Policy/context review:** rules and administrative systems shaping access.
        """
    )

with col2:
    section_h2("use-this-site-to", "Use This Site To")
    st.info(
        "Move from evidence to interpretation: each page helps explain how a finding "
        "fits into the broader system and what it suggests for community-facing action."
    )
    st.warning(
        "The quantitative page should be read descriptively. It shows spatial patterns "
        "and overlap, not causal proof."
    )
