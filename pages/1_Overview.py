import streamlit as st

from shared_style import apply_theme, support_badge


st.set_page_config(page_title="Overview", layout="wide")

apply_theme()

support_badge()

st.title("Project Overview")

st.markdown(
    """
    This platform frames tangled titles as a system-level housing stability issue:
    a resident may live in and maintain a family home, but still lack the formal
    documentation required by legal, financial, and government systems.
    """
)

st.markdown("### Resident Pathway")
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

st.write("")

col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.markdown("### Synthesis Question")
    st.markdown(
        """
        How do individual knowledge gaps, family inheritance processes, service
        access, administrative systems, and neighborhood-level inequities interact
        to shape tangled title risk in Baltimore?
        """
    )

    st.markdown("### Evidence Streams")
    st.markdown(
        """
        - **Interviews:** lived experience, service navigation, institutional trust.
        - **Power mapping:** actors, barriers, facilitators, and intervention points.
        - **Quant analysis:** tract-level patterns in title risk and wealth context.
        - **Policy/context review:** rules and administrative systems shaping access.
        """
    )

with col2:
    st.markdown("### Use This Site To")
    st.info(
        "Move from evidence to interpretation: each page helps explain how a finding "
        "fits into the broader system and what it suggests for community-facing action."
    )
    st.warning(
        "The quantitative page should be read descriptively. It shows spatial patterns "
        "and overlap, not causal proof."
    )
