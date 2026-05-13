import base64
import mimetypes
import sys
from html import escape
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_style import apply_theme, render_page_toc, section_h2
from tangled_titles_content import (
    RESIDENT_JOURNEY_STAGES,
    TASHA_BALTIMORE_SCALE_CONTEXT,
    TASHA_CASE_STUDY_IMPLICATIONS,
    TASHA_CASE_STUDY_SOURCES,
    TASHA_JOURNEY_OVERVIEW_IMAGE,
    TASHA_PROFILE,
)


st.set_page_config(page_title="Resident Journey", layout="wide")
apply_theme()

JOURNEY_TOC = (
    ("overview", "Overview"),
    ("tasha-journey", "Tasha's Journey"),
    ("system-encounters", "System Encounters"),
    ("sources-and-implications", "Sources and Implications"),
)
render_page_toc("resident-journey", JOURNEY_TOC)

BASE_DIR = ROOT_DIR


def render_stage_image(stage: dict[str, str], idx: int) -> None:
    image_path = BASE_DIR / stage["image"]
    if image_path.exists():
        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        st.markdown(
            f"""
            <figure class="journey-figure">
                <img src="data:{mime_type};base64,{encoded}" alt="{escape(stage['alt'])}">
                <figcaption>{idx}. {escape(stage['title'])}</figcaption>
            </figure>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="journey-image-placeholder" role="img" aria-label="{escape(stage['alt'])}">
            <div class="mini-doc"></div>
            <h3>{idx}. {escape(stage['title'])}</h3>
            <p class="muted-note">Add image file:<br><code>{escape(stage['image'])}</code></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stage(stage: dict[str, str], idx: int) -> None:
    image_col, text_col = st.columns([0.44, 0.56], gap="large")
    if idx % 2 == 0:
        text_col, image_col = image_col, text_col

    with image_col:
        render_stage_image(stage, idx)

    with text_col:
        st.markdown(
            f"""
            <div class="journey-stage-card">
                <p class="rq-badge">Stage {idx}</p>
                <h3>{escape(stage['title'])}</h3>
                <p class="story-hook">{escape(stage.get('story_hook', ''))}</p>
                <p>{escape(stage['narrative'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("System details", expanded=False):
            st.markdown(
                f"""
                <div class="journey-stage-meta">
                    <strong>System touchpoint</strong>
                    <span>{escape(stage['touchpoint'])}</span>
                </div>
                <div class="journey-stage-meta">
                    <strong>Power map connection</strong>
                    <span>{escape(stage['power_map_connection'])}</span>
                </div>
                <div class="journey-stage-barrier">
                    <strong>Barrier</strong>
                    <span>{escape(stage['barrier'])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with st.expander("Evidence and source notes", expanded=False):
            st.markdown(stage.get("evidence_note", ""))
            source_labels = stage.get("source_labels", [])
            if source_labels:
                st.caption("Source anchors: " + ", ".join(source_labels))


def render_journey_overview_image() -> None:
    image_path = BASE_DIR / TASHA_JOURNEY_OVERVIEW_IMAGE["image"]
    if image_path.exists():
        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        st.markdown(
            f"""
            <figure class="journey-figure">
                <img src="data:{mime_type};base64,{encoded}" alt="{escape(TASHA_JOURNEY_OVERVIEW_IMAGE['alt'])}">
                <figcaption>{escape(TASHA_JOURNEY_OVERVIEW_IMAGE['caption'])}</figcaption>
            </figure>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="journey-image-placeholder hero-placeholder" role="img" aria-label="{escape(TASHA_JOURNEY_OVERVIEW_IMAGE['alt'])}">
                <div class="mini-house"></div>
                <h3>Tasha Johnson overview image</h3>
                <p class="muted-note">Add image file:<br><code>{escape(TASHA_JOURNEY_OVERVIEW_IMAGE['image'])}</code></p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.title("Resident Journey")
st.markdown(
    """
    Meet Tasha Johnson, a fictional composite resident whose journey illustrates
    how tangled titles can move from an invisible paperwork issue to a housing
    stability crisis. Her story connects individual estate-planning gaps, family
    inheritance, repair eligibility, tax sale risk, and the loss of
    intergenerational wealth.
    """
)
st.info("This composite case is illustrative. It is not a real person's full transcript or legal case.")

section_h2("overview", "Overview")
overview_left, overview_right = st.columns([0.52, 0.48], gap="large")
with overview_left:
    st.markdown(
        f"""
        <div class="central-issue-card">
            <h3>The Hostage Home: Tasha Johnson's Journey</h3>
            <p><strong>{escape(TASHA_PROFILE["name"])}</strong> is a {escape(TASHA_PROFILE["age"])}
            {escape(TASHA_PROFILE["race_ethnicity"])} head of household from
            {escape(TASHA_PROFILE["hometown"])}. She works full time as a
            {escape(TASHA_PROFILE["job"])} and earns {escape(TASHA_PROFILE["income"])}.</p>
            <p>The home becomes "held hostage" by a tangled title: the deed remains
            outdated, the tax system does not see Tasha as the legal owner, and
            support systems that could protect low-income homeowners become harder
            to access.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    profile_cols = st.columns(2)
    profile_items = [
        ("Problem", TASHA_PROFILE["problem"]),
        ("Resources needed", TASHA_PROFILE["resources_needed"]),
    ]
    for col, (label, value) in zip(profile_cols, profile_items):
        with col:
            st.markdown(
                f"""
                <div class="compact-card">
                    <h3>{escape(label)}</h3>
                    <p>{escape(value)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
with overview_right:
    render_journey_overview_image()

section_h2("tasha-journey", "Tasha's Journey")
st.markdown(
    """
    <div class="key-takeaway-card">
        <strong>How does a hidden paperwork problem become a housing crisis?</strong>
        Follow the points where Tasha's lived ownership meets systems that require formal title.
    </div>
    """,
    unsafe_allow_html=True,
)
for idx, stage in enumerate(RESIDENT_JOURNEY_STAGES, start=1):
    with st.container(border=True):
        render_stage(stage, idx)

section_h2("system-encounters", "System Encounters")
st.markdown(
    """
    The journey shows when the system becomes visible: after family inheritance
    records fall out of sync, when a repair application requires proof of
    ownership, when tax payments and notices move through systems tied to a
    deceased owner's name, and when tax sale or foreclosure risk brings market
    actors to the doorstep. Solutions and intervention recommendations are
    intentionally kept out of this section and remain in the final intervention
    sections elsewhere in the site.
    """
)
st.markdown(
    """
    <div class="takeaway">
    Tasha's story shows how a hidden title mismatch becomes visible through
    repair systems, tax systems, and market pressure. The next pages show how
    interview evidence and spatial data connect this story to broader patterns
    in Baltimore.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Baltimore-scale context")
context_cols = st.columns(3)
for col, (label, value) in zip(
    context_cols,
    [
        ("Tax sale exposure", TASHA_BALTIMORE_SCALE_CONTEXT["tax_sale"]),
        ("Locked family assets", TASHA_BALTIMORE_SCALE_CONTEXT["locked_assets"]),
        ("Vacancy and public cost", TASHA_BALTIMORE_SCALE_CONTEXT["vacancy_cost"]),
    ],
):
    with col:
        st.markdown(
            f"""
            <div class="compact-card">
                <h3>{escape(label)}</h3>
                <p>{escape(value)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

section_h2("sources-and-implications", "Sources and Implications")
st.markdown(
    """
    This section keeps the case study transparent: Tasha is fictional, but the
    profile, tax-sale pathway, wage assumption, surname choice, and Baltimore-wide
    wealth framing are grounded in the sources below.
    """
)

source_cols = st.columns(2)
for idx, source in enumerate(TASHA_CASE_STUDY_SOURCES):
    with source_cols[idx % 2]:
        st.markdown(
            f"""
            <div class="evidence-card">
                <h3>{escape(source["label"])}</h3>
                <p class="muted-note">{escape(source["date"])}</p>
                <p>{escape(source["note"])}</p>
                <p><a href="{escape(source["url"])}" target="_blank" rel="noopener">Open source</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander("Community implications from the composite case", expanded=False):
    for item in TASHA_CASE_STUDY_IMPLICATIONS:
        st.markdown(f"- {item}")
