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
from tangled_titles_content import RESIDENT_JOURNEY_STAGES, TASHA_JOURNEY_OVERVIEW_IMAGE


st.set_page_config(page_title="Resident Journey", layout="wide")
apply_theme()

JOURNEY_TOC = (
    ("overview", "Overview"),
    ("tasha-journey", "Tasha's Journey"),
    ("system-encounters", "System Encounters"),
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
                <p>{escape(stage['narrative'])}</p>
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
            </div>
            """,
            unsafe_allow_html=True,
        )


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
        """
        <div class="central-issue-card">
            <h3>The Hostage Home: Tasha Johnson's Journey</h3>
            <p>Tasha Johnson is a 35-year-old Black/African-American head of
            household in West Baltimore. She works full-time as a front desk
            receptionist at Freedman's Health Clinic and lives in a long-time
            family home that represents shelter, memory, and a 66-year family
            legacy.</p>
            <p>The home becomes "held hostage" by a tangled title: her
            grandparents did not leave clear estate documents, the deed remains
            outdated, and the systems that should protect low-income homeowners
            do not recognize Tasha as the legal owner.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with overview_right:
    render_journey_overview_image()

section_h2("tasha-journey", "Tasha's Journey")
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
