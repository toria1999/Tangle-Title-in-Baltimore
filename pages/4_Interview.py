import sys
import json
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_style import apply_theme, render_page_toc, section_h2
from tangled_titles_content import (
    INTERVIEW_THEMES,
    NODE_BY_ID,
    QUOTE_WALL_ITEMS,
    THEME_BY_ID,
    THEME_LEVEL_ORDER,
    nodes_for_theme,
)

st.set_page_config(page_title="Interview", layout="wide")
apply_theme()

INTERVIEW_TOC = (
    ("overview", "Overview"),
    ("interviewee-perspectives", "Interviewee Perspectives"),
    ("three-messages", "Three Messages"),
    ("interview-word-cloud", "Repeated Interview Language"),
    ("theme-explorer", "Theme Explorer"),
)
render_page_toc("interview", INTERVIEW_TOC)


def switch_to_power_map(node_id: str) -> None:
    st.session_state["selected_section"] = "Power Map"
    st.session_state["selected_node"] = node_id
    st.switch_page("pages/5_Power_Map.py")


def render_theme_card(theme: dict, compact: bool = False) -> None:
    related_nodes = nodes_for_theme(theme["id"])
    st.markdown(
        f"""
        <div class="evidence-card" id="theme-{theme["id"]}">
            <div class="badge-row">
                <span class="level-badge" style="background:#eef7e8;">{theme["level"]}</span>
            </div>
            <h3>{theme["title"]}</h3>
            <p>{theme["short_summary"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quote_count = 1 if compact else min(3, len(theme["key_quotes"]))
    for quote in theme["key_quotes"][:quote_count]:
        st.markdown(f'<div class="mini-quote">"{quote}"</div>', unsafe_allow_html=True)

    with st.expander("Related Power Map nodes", expanded=False):
        for node in related_nodes:
            if st.button(
                f"View node: {node['label']}",
                key=f"theme-{theme['id']}-node-{node['id']}",
                use_container_width=True,
            ):
                switch_to_power_map(node["id"])

    st.caption(theme["implications"])


WORD_CLOUD_TERMS = [
    {
        "text": "repairs",
        "value": 58,
        "theme": "Home repair barriers",
        "description": "Repair needs often reveal title problems because assistance programs usually require proof of ownership.",
        "quote": "One of the conditions of receiving home repair funding in the city, in particular, is that you have to have a clear title.",
    },
    {
        "text": "deed transfer",
        "value": 54,
        "theme": "Ownership mismatch",
        "description": "The deed is the formal record that systems use to decide who is recognized as the homeowner.",
        "quote": "They know that their mom is on the deed. But they assume that they are the owner and it's fine.",
    },
    {
        "text": "estate planning",
        "value": 52,
        "theme": "Prevention",
        "description": "Wills, life estate deeds, and transfer-on-death tools can prevent some tangled title problems before death.",
        "quote": "If people had their wills and they had life estate deeds, this would not be an issue.",
    },
    {"text": "family", "value": 48, "theme": "Family inheritance", "description": "Interviewees repeatedly framed the home as family memory, family responsibility, and family wealth.", "quote": ""},
    {"text": "wills", "value": 44, "theme": "Estate planning", "description": "Wills help clarify who should receive the home, reducing later disagreement and uncertainty.", "quote": ""},
    {"text": "heirs' property", "value": 42, "theme": "Inheritance structure", "description": "Multiple heirs can hold interests in a property even when one person lives there and maintains it.", "quote": ""},
    {"text": "taxes", "value": 39, "theme": "Tax burden", "description": "Property taxes and water bills can become harder to manage when residents lack owner-occupied protections.", "quote": ""},
    {"text": "income", "value": 36, "theme": "Economic constraint", "description": "Fixed or low incomes make legal fees, repairs, and tax payments harder to absorb.", "quote": ""},
    {"text": "death", "value": 34, "theme": "Trigger point", "description": "A title often becomes tangled after a homeowner dies and no formal transfer is completed.", "quote": ""},
    {"text": "family conflict", "value": 33, "theme": "Interpersonal barrier", "description": "Disagreement among siblings or heirs can stall probate, repair decisions, or title clearing.", "quote": "If they can't come to consensus, then in many ways the property may sit in limbo."},
    {"text": "tax sale", "value": 32, "theme": "Tax sale risk", "description": "Tax sale can turn unpaid bills into foreclosure pressure, especially when notices go to the titled owner.", "quote": ""},
    {"text": "foreclosure", "value": 30, "theme": "Housing loss risk", "description": "Tangled title can make it harder for the resident to defend the property when foreclosure pressure appears.", "quote": ""},
    {"text": "probate", "value": 29, "theme": "Legal process", "description": "Probate or estate administration is often needed before a deceased owner's property can transfer.", "quote": "People don't even know they need to go to the Register of Wills."},
    {"text": "home equity", "value": 27, "theme": "Wealth access", "description": "When title is unclear, residents may be unable to borrow against or otherwise use home equity.", "quote": ""},
    {"text": "wealth loss", "value": 26, "theme": "Intergenerational wealth", "description": "Tangled titles can interrupt the transfer of family wealth across generations.", "quote": ""},
    {"text": "vacant housing", "value": 24, "theme": "Neighborhood impact", "description": "Unresolved title and repair barriers can contribute to deterioration, vacancy, and neighborhood instability.", "quote": ""},
    {"text": "legal help", "value": 23, "theme": "Facilitator", "description": "Legal aid, mediation, and holistic services help residents navigate probate, deeds, and tax sale risk.", "quote": ""},
    {"text": "community outreach", "value": 22, "theme": "Trusted access", "description": "Interviewees emphasized meeting residents in neighborhoods instead of waiting for residents to find services.", "quote": "Instead of waiting for people to come to you, go to them."},
    {"text": "shelter", "value": 21, "theme": "Housing stability", "description": "The home is not only an asset; for many residents it is their primary affordable shelter.", "quote": "One of the most important things that people are actually getting from these homes is shelter."},
    {"text": "Black Butterfly", "value": 20, "theme": "Spatial inequality", "description": "Interviewees linked tangled title risk to Baltimore's racialized geography and historic disinvestment.", "quote": "Most of the times it is the Black Butterfly region."},
    {"text": "records", "value": 19, "theme": "Administrative mismatch", "description": "Public records may continue to name deceased or absent owners rather than the person living in the home.", "quote": ""},
    {"text": "access", "value": 18, "theme": "Program eligibility", "description": "Clear title often controls access to grants, credits, loans, legal protections, and notices.", "quote": ""},
    {"text": "fixed-income seniors", "value": 17, "theme": "Compounded risk", "description": "Older homeowners on fixed incomes can face overlapping repair, tax, legal, and digital burdens.", "quote": ""},
    {"text": "asset", "value": 16, "theme": "Family wealth", "description": "A modest home can still be the family's largest asset and a foundation for future stability.", "quote": ""},
    {"text": "transportation", "value": 14, "theme": "Administrative burden", "description": "Getting to offices, clinics, or document appointments can be another barrier in the title-clearing process.", "quote": "Transportation is a big issue."},
    {"text": "clearing", "value": 13, "theme": "Title resolution", "description": "Title clearing can require documents, legal help, heir outreach, and time.", "quote": ""},
    {"text": "consensus", "value": 12, "theme": "Joint decision-making", "description": "When several heirs have interests, repair, transfer, or sale decisions may require agreement.", "quote": ""},
]


def render_interactive_word_cloud_panel(terms: list[dict]) -> None:
    cloud_terms = sorted(terms, key=lambda item: item["value"], reverse=True)[:30]
    payload = json.dumps(cloud_terms).replace("</", "<\\/")
    components.html(
        f"""
        <div class="cloud-card">
            <svg id="word-cloud" viewBox="0 0 920 390" role="img" aria-label="Interactive interview word cloud"></svg>
            <div id="cloud-detail" class="cloud-detail">
                <strong>Select a word</strong>
                <p>Click any term in the cloud to see its theme and interpretation.</p>
            </div>
        </div>
        <style>
            body {{
                margin: 0;
                background: transparent;
                font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}
            .cloud-card {{
                background: radial-gradient(circle at 45% 35%, #fffdf6 0%, #fffaf0 52%, #f7efd8 100%);
                border: 1px solid rgba(24, 49, 45, 0.16);
                border-radius: 16px;
                box-shadow: 0 12px 28px rgba(24, 49, 45, 0.08);
                padding: 14px 16px 16px;
            }}
            #word-cloud {{
                width: 100%;
                height: 390px;
                display: block;
            }}
            .cloud-word {{
                cursor: pointer;
                dominant-baseline: middle;
                text-anchor: middle;
                paint-order: stroke;
                stroke: rgba(255, 250, 240, 0.78);
                stroke-width: 4px;
                transition: opacity 160ms ease, transform 160ms ease, filter 160ms ease;
            }}
            .cloud-word:hover, .cloud-word.active {{
                opacity: 1 !important;
                filter: drop-shadow(0 3px 5px rgba(24, 49, 45, 0.24));
            }}
            .cloud-detail {{
                min-height: 82px;
                margin: 4px 6px 0;
                padding: 0.85rem 1rem;
                border-left: 5px solid #b88a2d;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.72);
                color: #18312d;
                font-size: 0.98rem;
                line-height: 1.45;
            }}
            .cloud-detail p {{
                margin: 0.32rem 0 0;
            }}
            .cloud-detail .quote {{
                margin-top: 0.45rem;
                color: #5f6b64;
                font-style: italic;
            }}
        </style>
        <script>
            const terms = {payload};
            const svg = document.getElementById("word-cloud");
            const detail = document.getElementById("cloud-detail");
            const colors = ["#294943", "#6b5637", "#b88a2d", "#5e8fa8", "#8f4f4b"];
            const positions = [
                [460, 186], [292, 150], [608, 154], [405, 104], [530, 92], [198, 222],
                [710, 226], [355, 250], [574, 256], [132, 140], [796, 148], [246, 292],
                [672, 306], [452, 304], [82, 250], [842, 268], [186, 86], [742, 82],
                [326, 344], [592, 346], [86, 78], [846, 72], [458, 44], [700, 374],
                [226, 374], [560, 40], [360, 46], [106, 330], [812, 340], [462, 358]
            ];
            const minValue = Math.min(...terms.map(d => d.value));
            const maxValue = Math.max(...terms.map(d => d.value));

            function fontSize(value) {{
                const scaled = (value - minValue) / Math.max(1, maxValue - minValue);
                return 18 + scaled * 26;
            }}

            function showDetail(term, element) {{
                document.querySelectorAll(".cloud-word").forEach(node => node.classList.remove("active"));
                element.classList.add("active");
                const quote = term.quote ? `<p class="quote">"${{term.quote}}"</p>` : "";
                detail.innerHTML = `
                    <strong>${{term.text}}</strong>
                    <p><b>Theme:</b> ${{term.theme}}</p>
                    <p>${{term.description}}</p>
                    ${{quote}}
                `;
            }}

            terms.forEach((term, index) => {{
                const [x, y] = positions[index % positions.length];
                const word = document.createElementNS("http://www.w3.org/2000/svg", "text");
                word.textContent = term.text;
                word.setAttribute("x", x);
                word.setAttribute("y", y);
                word.setAttribute("font-size", fontSize(term.value));
                word.setAttribute("font-weight", term.value >= 30 ? 720 : 610);
                word.setAttribute("fill", colors[index % colors.length]);
                word.setAttribute("class", "cloud-word");
                word.style.opacity = String(0.76 + Math.min(0.2, term.value / 250));
                word.addEventListener("click", () => showDetail(term, word));
                svg.appendChild(word);
            }});
        </script>
        """,
        height=540,
    )


selected_theme_id = st.session_state.get("selected_theme")
selected_theme = THEME_BY_ID.get(selected_theme_id) if selected_theme_id else None

st.title("Interview")
st.markdown(
    """
    Tangled titles in Baltimore sit at the intersection of law, family, housing,
    and structural inequality. Interviews with legal, housing, civic design, and
    policy stakeholders show that title problems often remain invisible until
    residents seek repairs, receive tax sale notices, or try to access public
    benefits.
    """
)

if selected_theme:
    st.markdown(
        f"""
        <div class="detail-panel">
            <strong>Selected theme from Power Map:</strong><br>
            {selected_theme["title"]}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Clear selected theme", key="clear-selected-theme"):
        st.session_state.pop("selected_theme", None)
        st.rerun()

section_h2("overview", "Overview")
st.markdown(
    """
    <div class="key-takeaway-card">
        <strong>What did stakeholders repeatedly say?</strong>
        Tangled titles are not only a paperwork problem. They emerge when family
        relationships, service pathways, legal institutions, economic constraints,
        and racialized housing inequality collide.
    </div>
    """
    ,
    unsafe_allow_html=True,
)

section_h2("interviewee-perspectives", "Interviewee Perspectives")
st.markdown(
    """
    <p class="section-subtitle">
    The interview evidence reflects institutional and practice-based perspectives
    from people working across civic design, city innovation, legal aid, and
    homeownership preservation.
    </p>
    """,
    unsafe_allow_html=True,
)
perspective_cards = [
    (
        "Civic design / city innovation",
        "Baltimore Mayor's Office of Innovation civic design perspective, including work connected to homeownership preservation.",
    ),
    (
        "Legal aid / homeownership preservation",
        "Practitioners who see tangled titles through repair eligibility, probate, foreclosure, and title-clearing cases.",
    ),
    (
        "Baltimore City innovation team",
        "City-facing perspective on service pathways, resident touchpoints, and how administrative systems become visible in crisis.",
    ),
    (
        "Maryland Volunteer Legal Services",
        "Legal service perspective on estate planning, probate assistance, tax sale prevention, and warm referrals.",
    ),
]
perspective_cols = st.columns(4)
for col, (title, description) in zip(perspective_cols, perspective_cards):
    with col:
        st.markdown(
            f"""
            <div class="evidence-card compact-card" style="min-height:190px;">
                <span class="rq-badge">Perspective</span>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

section_h2("three-messages", "Three messages from the interviews")
message_cards = [
    (
        "Tangled titles often stay invisible until crisis.",
        "Residents often discover title problems when they seek repairs, receive tax sale notices, face foreclosure, or apply for support.",
        "Most people are seeing a symptom usually.",
    ),
    (
        "Ownership mismatch turns family history into administrative burden.",
        "Living in the home, paying bills, or being family does not automatically make someone legally recognized as the owner.",
        "They assume because they were the adult child living in the property that they automatically inherited it, which is not true.",
    ),
    (
        "Navigation requires trusted outreach and warm handoffs.",
        "Interviewees emphasized that residents need more than a phone number. They need trusted, proactive connection to legal and housing support.",
        "Instead of waiting for people to come to you, go to them.",
    ),
]
cols = st.columns(3)
for col, (title, explanation, quote) in zip(cols, message_cards):
    with col:
        st.markdown(
            f"""
            <div class="evidence-card" style="min-height:285px;">
                <span class="rq-badge">Interview message</span>
                <h3>{title}</h3>
                <p>{explanation}</p>
                <div class="mini-quote">"{quote}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

section_h2("interview-word-cloud", "What Came Up Repeatedly in Interviews")
st.markdown(
    """
    <p class="section-subtitle">This interactive word cloud offers a quick orientation to recurring interview language. It is not a substitute for the themes, quotes, and resident narratives below.</p>
    """
    ,
    unsafe_allow_html=True,
)

with st.expander("Explore recurring words from interviews", expanded=False):
    render_interactive_word_cloud_panel(WORD_CLOUD_TERMS)
    term_options = {term["text"]: term for term in WORD_CLOUD_TERMS}
    selected_word = st.selectbox(
        "Explore a term",
        ["Choose a term"] + [term["text"] for term in WORD_CLOUD_TERMS],
        key="word-cloud-term-select",
    )
    if selected_word != "Choose a term":
        term = term_options[selected_word]
        quote_html = (
            f'<div class="mini-quote" style="margin-top:0.65rem;">"{escape(term["quote"])}"</div>'
            if term.get("quote")
            else ""
        )
        st.markdown(
            f"""
            <div class="detail-panel">
                <span class="rq-badge">Selected term</span>
                <h3>{escape(term["text"])}</h3>
                <p><strong>Theme:</strong> {escape(term["theme"])}</p>
                <p>{escape(term["description"])}</p>
                {quote_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.caption(
        "Terms were cleaned and grouped to emphasize analytically meaningful interview language rather than raw transcript frequency."
    )

with st.expander("Selected quotes behind the recurring words", expanded=False):
    quote_wall_query = st.text_input("Search selected quotes", key="quote-wall-search")
    quote_items = [
        item for item in QUOTE_WALL_ITEMS if not quote_wall_query.strip() or quote_wall_query.lower() in " ".join(item).lower()
    ]
    quote_groups = sorted({item[0] for item in quote_items})
    for group in quote_groups:
        st.markdown(f"### {group}")
        group_items = [item for item in quote_items if item[0] == group]
        columns = st.columns(2)
        for idx, (theme_label, quote, theme_id, node_id) in enumerate(group_items):
            node = NODE_BY_ID.get(node_id)
            theme = THEME_BY_ID.get(theme_id)
            with columns[idx % 2]:
                st.markdown(
                    f"""
                    <div class="evidence-card" style="min-height:285px;">
                        <div class="mini-quote" style="line-height:1.48;">"{quote}"</div>
                        <div class="badge-row">
                            <span class="node-chip">{theme_label}</span>
                        </div>
                        <p class="muted-note">Theme: {theme["title"] if theme else theme_id}</p>
                        <p class="muted-note">Power map node: {node["label"] if node else node_id}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if node and st.button(
                    f"View node: {node['label']}",
                    key=f"word-cloud-quote-{theme_id}-{node_id}-{idx}",
                    use_container_width=True,
                ):
                    switch_to_power_map(node_id)

section_h2("theme-explorer", "Theme Explorer")
st.markdown(
    """
    <p class="section-subtitle">The full evidence set remains available, but it is collapsed by default so the page reads as a synthesis first.</p>
    """,
    unsafe_allow_html=True,
)
with st.expander("Explore all interview themes and quotes", expanded=False):
    level_options = ["All levels"] + list(THEME_LEVEL_ORDER)
    search_term = st.text_input(
        "Search themes, quotes, or related nodes",
        value="",
        placeholder="probate, repair, tax sale, family conflict, Black Butterfly...",
    )
    selected_level = st.selectbox("Filter by interview level", level_options)

    filtered_themes = INTERVIEW_THEMES
    if selected_level != "All levels":
        filtered_themes = [theme for theme in filtered_themes if theme["level"] == selected_level]
    if search_term.strip():
        query = search_term.lower()
        filtered_themes = [
            theme
            for theme in filtered_themes
            if query in theme["title"].lower()
            or query in theme["short_summary"].lower()
            or query in " ".join(theme["key_quotes"]).lower()
            or query in " ".join(theme["related_power_nodes"]).lower()
        ]

    for level in THEME_LEVEL_ORDER:
        themes_for_level = [theme for theme in filtered_themes if theme["level"] == level]
        if not themes_for_level:
            continue
        st.markdown(f"### {level}")
        columns = st.columns(2)
        for idx, theme in enumerate(themes_for_level):
            with columns[idx % 2]:
                with st.container(border=True):
                    render_theme_card(theme, compact=True)

st.info(
    "Action recommendations are consolidated on the Power Map page so this page can focus on interview evidence."
)
