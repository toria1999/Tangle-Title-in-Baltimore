import sys
import base64
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_style import apply_theme, render_page_toc, section_h2, support_badge
from tangled_titles_content import GLOSSARY_TERMS, PROBLEM_PATHWAY_DETAIL


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

essential_terms = {
    "Tangled title",
    "Deed",
    "Clear title",
    "Probate",
    "Tax sale",
    "Home repair grant",
    "Legal aid",
}

INTRO_HERO_IMAGE = ROOT_DIR / "assets" / "introduction" / "resident_rowhouse_deed_mismatch.png"
if INTRO_HERO_IMAGE.exists():
    _intro_hero_image = (
        f'<img src="data:image/png;base64,{base64.b64encode(INTRO_HERO_IMAGE.read_bytes()).decode("ascii")}" '
        'alt="Resident near a Baltimore rowhouse with a deed mismatch illustration" />'
    )
else:
    _intro_hero_image = """
        <h3>Illustration placeholder: resident, rowhouse, and deed mismatch</h3>
        <p class="muted-note">A future image can show the human story beside the paperwork record.</p>
    """

st.markdown(
    f"""
    <div class="page-hero">
        <div class="hero-copy">
            <span class="rq-badge">What is a tangled title, and why does it matter?</span>
            <h2>A family can live in a home for decades and still be treated as if they do not legally belong there.</h2>
            <p>A tangled title happens when the legal ownership record does not match the person who lives in, maintains, or inherits the home.</p>
            <p class="muted-note">This matters because legal recognition often controls access to repairs, tax credits, notices, loans, and protection from displacement.</p>
        </div>
        <div class="hero-visual">
            {_intro_hero_image}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="key-takeaway-card">
        <strong>Key takeaway</strong>
        Tangled titles are not just a legal paperwork problem. They are a pathway
        through which family inheritance, housing repair systems, tax sale risk,
        and wealth loss can become connected.
    </div>
    """
    ,
    unsafe_allow_html=True,
)

section_h2("key-terms", "Key Terms / Keyword Guide")
st.markdown(
    """
    <p class="section-subtitle">Start with the essentials. The full glossary stays available below without taking over the first view.</p>
    """
    ,
    unsafe_allow_html=True,
)

essential_items = [item for item in GLOSSARY_TERMS if item[0] in essential_terms]
st.markdown('<div class="compact-grid">', unsafe_allow_html=True)
for term, definition, why_it_matters in essential_items:
    st.markdown(
        f"""
        <div class="compact-card">
            <h3>{term}</h3>
            <p>{definition}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Open the full glossary", expanded=False):
    st.caption("Plain-language starting points, not legal advice.")
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
            <ul>
                <li>Name on deed</li>
                <li>Repair grants and tax credits are easier to access</li>
                <li>Notices reach the right person</li>
                <li>Transfer, refinance, or equity access is easier</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with tangled_col:
    st.markdown(
        """
        <div class="evidence-card" style="border-top: 7px solid #c96b68;">
            <h3>Tangled Title</h3>
            <p class="muted-note">The resident's lived relationship to the home is not fully recognized by legal records.</p>
            <ul>
                <li>Resident's name may not be on deed</li>
                <li>Repair grants or tax credits may be blocked</li>
                <li>Notices may go to deceased or absent titled owners</li>
                <li>Family conflict or unresolved inheritance may remain</li>
                <li>Higher risk of tax sale, foreclosure, vacancy, or displacement</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

with st.expander("Details behind", expanded=False):
    for idx, step in enumerate(PROBLEM_PATHWAY_DETAIL, start=1):
        st.markdown(f"**{idx}. {step}**")

st.write("")

col1, col2 = st.columns([1.1, 0.9])

with col1:
    section_h2("synthesis-question", "Synthesis Question")
    st.markdown(
        """
        How do family inheritance processes, service access, administrative
        systems, and neighborhood-level inequities interact to shape tangled
        title risk in Baltimore?
        """
    )

    section_h2("evidence-streams", "Evidence Streams")
    st.markdown(
        """
        <div class="compact-grid">
            <div class="compact-card"><h3>Quant map</h3><p>Tract-level patterns in title risk and wealth context.</p></div>
            <div class="compact-card"><h3>Interviews</h3><p>Stakeholder themes about crisis, navigation, and institutional trust.</p></div>
            <div class="compact-card"><h3>Power map</h3><p>Actors, barriers, facilitators, and intervention points.</p></div>
        </div>
        """
        ,
        unsafe_allow_html=True,
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
