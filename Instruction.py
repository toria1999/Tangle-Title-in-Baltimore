import streamlit as st

from shared_style import apply_theme, support_badge


st.set_page_config(
    page_title="Tangled Titles Synthesis Platform",
    layout="wide",
)

apply_theme()

support_badge()

st.title("Tangled Titles Synthesis Platform")

st.markdown(
    """
    <p class="section-note">
    This interactive site synthesizes qualitative interviews, power mapping, and
    quantitative spatial analysis to explain how tangled titles shape housing
    stability and Black wealth preservation in Baltimore.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="takeaway">
    <strong>How to use this platform:</strong> begin with the Overview to understand
    the resident pathway, then move through the Power Map, Interview Themes,
    Quantitative Patterns, and Synthesis Matrix to build the final presentation
    narrative.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="soft-card">
            <h3>Explore the Power Map</h3>
            <p>See barriers, facilitators, agencies, and structural determinants as
            a connected system rather than isolated findings.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="soft-card">
            <h3>See Interview Themes</h3>
            <p>Connect lived experience and stakeholder interviews to specific
            system nodes and intervention opportunities.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="soft-card">
            <h3>View Spatial Patterns</h3>
            <p>Use descriptive maps and charts to examine where title risk and
            related wealth indicators are concentrated.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

st.markdown("### Synthesis Logic")
st.markdown(
    """
    This site is organized as a synthesis product. Each page connects a different
    source of evidence to the same explanatory question: where does the tangled
    title problem become a barrier, and where can intervention enter the system?
    """
)
