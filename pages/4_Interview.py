import sys
import json
import base64
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
PLACEHOLDER_DIR = ROOT_DIR / "assets" / "placeholders"

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
    ("evidence-highlights", "Evidence Highlights"),
    ("interview-word-cloud", "Repeated Interview Language"),
    ("theme-explorer", "Theme Explorer"),
)
render_page_toc("interview", INTERVIEW_TOC)


def switch_to_power_map(node_id: str) -> None:
    st.session_state["selected_section"] = "Power Map"
    st.session_state["selected_node"] = node_id
    st.switch_page("pages/5_Power_Map.py")


def render_local_image(filename: str, class_name: str, alt: str) -> None:
    image_bytes = (PLACEHOLDER_DIR / filename).read_bytes()
    encoded = base64.b64encode(image_bytes).decode("ascii")
    st.markdown(
        f"""
        <div class="{class_name}">
            <img src="data:image/jpeg;base64,{encoded}" alt="{escape(alt)}">
        </div>
        """,
        unsafe_allow_html=True,
    )


QUOTE_SOURCE_BY_TEXT = {
    "Most people are seeing a symptom usually.": "Legal Assistance Organization Leader 1",
    "They assume because they were the adult child living in the property that they automatically inherited it, which is not true.": "Legal Assistance Organization Leader 1",
    "Instead of waiting for people to come to you, go to them.": "Legal Assistance Organization Leader 2",
    "One of the conditions of receiving home repair funding in the city, in particular, is that you have to have a clear title.": "Local Policymaker 1",
    "They know that their mom is on the deed. But they assume that they are the owner and it's fine.": "Legal Assistance Organization Leader 1",
    "If people had their wills and they had life estate deeds, this would not be an issue.": "Legal Assistance Organization Leader 1",
    "If they can't come to consensus, then in many ways the property may sit in limbo.": "Local Policymaker 1",
    "People don't even know they need to go to the Register of Wills.": "Legal Assistance Organization Leader 1",
    "Transportation is a big issue.": "Legal Assistance Organization Leader 1",
    "One of the most important things that people are actually getting from these homes is shelter.": "Local Policymaker 1",
    "Most of the times it is the Black Butterfly region.": "Legal Assistance Organization Leader 3",
    "People don't know what they don't know.": "Legal Assistance Organization Leader 1",
    "People don't even know where to start.": "Legal Assistance Organization Leader 1",
    "Dead-on-arrival situations": "Legal Assistance Organization Leader 1",
    "Our population (clients) is about 90% Black and mostly seniors.": "Legal Assistance Organization Leader 3",
    "The communities that they serve are mostly the Black Butterfly region. Most of the times it is the Black Butterfly region.": "Legal Assistance Organization Leader 3",
    "Grown people's business was grown people's business.": "Legal Assistance Organization Leader 1",
    "Because there is no enforcement in the city, there is no good data on how many properties are going unregulated or how many rentals are essentially illegal because they are not going through the proper process.": "Local Policymaker 1",
    "So rather than finding it out in court, which is too expensive; they just let it go. And so that is, I think, I would say that's probably the biggest.": "Legal Assistance Organization Leader 1",
    "Other barriers are connected to human psychology and, partly, American culture. We do not interface with death or deal with death very well. Death is not at the forefront of our minds, so people may think estate planning is just something they will do when it happens, rather than something they should plan for.": "Local Policymaker 1",
    "The easiest to dissolve is the soonest they come, right? In the event that the homeowner is the person on the deed and they are the ones that pass away, as soon as they're done grieving with that process and ready to tackle and take on this new endeavor, the better. There's another reason to do it sooner: before someone else dies and there's more people with an interest in the home who could make it more complicated to sort through.": "Legal Assistance Organization Leader 1",
    "In Baltimore, given health risk factors, the people who should be prioritized are people who may be closer to death than others. That is a real reality when you are dealing with older homeowners. You cannot take for granted that they will still be there to resolve deed issues in one or two years. In terms of priority, the first cut is likely elderly people.": "Local Policymaker 1",
    "We did a heat map of those 3000 properties affected by tangled titles. And it was pretty close to like what people would call a 'black butterfly'.": "Legal Assistance Organization Leader 2",
    "Come to consensus on what happens to that property.": "Local Policymaker 1",
    "Now we have legislation that's implemented to where someone doesn't necessarily have access to a lawyer or legal counsel, and they want to transfer the property to their family. Now it's just a document that you can go and you can fill out.": "Legal Assistance Organization Leader 1",
    "If we educate the younger generation, and we get it out there, maybe they can have these conversations with their parents.": "Local Policymaker 1",
    "These people are in their home, like, installing grab bars in the shower. But they can be trained by us to spot some issues and send them our way.": "Legal Assistance Organization Leader 1",
    "For people accessing grants to repair their homes, is there a way that, in exchange for receiving repair grant money, we can require or strongly encourage them to do estate planning? Can we ask them to go through the process of clearing the title and doing this work while they are still alive?": "Legal Assistance Organization Leader 2",
    "Can the city partner with someone who offers mediation services, so family members can arrive at a resolution about what to do with the property? It is hard for me to see siblings or any other group of people who own a house together resolving that issue on their own.": "Legal Assistance Organization Leader 2",
}


def quote_source_for(quote: str) -> str:
    normalized = quote.strip().strip('"').replace("’", "'").replace("“", "").replace("”", "")
    return QUOTE_SOURCE_BY_TEXT.get(normalized, "Interview participant")


def quote_block(quote: str, source=None) -> str:
    speaker = source or quote_source_for(quote)
    return (
        f'<div class="quote-card">"{escape(quote)}"'
        f'<br><small>{escape(speaker)}</small></div>'
    )


def render_theme_card(theme: dict, compact: bool = False) -> None:
    related_nodes = nodes_for_theme(theme["id"])
    st.markdown(
        f"""
        <div class="reference-card" id="theme-{theme["id"]}">
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
        st.markdown(quote_block(quote), unsafe_allow_html=True)

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


query_theme_id = st.query_params.get("theme")
if isinstance(query_theme_id, list):
    query_theme_id = query_theme_id[0] if query_theme_id else None
if query_theme_id:
    st.session_state["selected_theme"] = query_theme_id

selected_theme_id = st.session_state.get("selected_theme")
selected_theme = THEME_BY_ID.get(selected_theme_id) if selected_theme_id else None

intro_text_col, intro_image_col = st.columns([0.62, 0.38], vertical_alignment="bottom")
with intro_text_col:
    st.title("Interview")
    st.markdown(
        """
        <div class="overview-inline-card" id="overview">
            <p>Tangled titles in Baltimore sit at the intersection of law, family, housing, and structural inequality. Interviews with legal, housing, civic design, and policy stakeholders show that title problems often remain invisible until residents seek repairs, receive tax sale notices, or try to access public benefits.</p>
            <p class="overview-transition">Across interviews, stakeholders repeatedly emphasized:</p>
            <ul>
                <li>Tangled titles are not only a paperwork problem.</li>
                <li>Ownership mismatch can turn family history into administrative burden.</li>
                <li>Trusted outreach, warm handoffs, and service coordination are needed before residents reach crisis.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with intro_image_col:
    render_local_image(
        "power_map_multilevel_ecosystem.png",
        "image-card medium",
        "Multilevel ecosystem around tangled title risk.",
    )

if selected_theme:
    st.markdown(
        f"""
        <div class="detail-panel" id="selected-interview-evidence">
            <span class="tag-pill">Selected from Power Map</span>
            <h3>{escape(selected_theme["title"])}</h3>
            <p>{escape(selected_theme["short_summary"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for quote in selected_theme["key_quotes"][:3]:
        st.markdown(quote_block(quote), unsafe_allow_html=True)
    if st.button("Clear selected theme", key="clear-selected-theme"):
        st.session_state.pop("selected_theme", None)
        if "theme" in st.query_params:
            del st.query_params["theme"]
        st.rerun()

section_h2("interviewee-perspectives", "Interviewee Perspectives")
st.markdown(
    """
    <p class="section-subtitle">
    Speaker labels are de-identified role labels from the qualitative materials.
    They name the perspective behind a quote, not a personal identity.
    </p>
    """,
    unsafe_allow_html=True,
)
perspective_cards = [
    (
        "Legal Assistance Organization Leader 1",
        "Homeownership-preservation and legal-aid perspective on estate planning, probate, legal costs, education, transfer tools, and frontline case finding.",
    ),
    (
        "Legal Assistance Organization Leader 2",
        "Legal and housing-systems perspective on repair-grant-linked estate planning, mediation, community partnerships, and data-informed outreach.",
    ),
    (
        "Legal Assistance Organization Leader 3",
        "Community-facing service perspective on client demographics, Black Butterfly geography, warm referrals, and tracking gaps after referral.",
    ),
    (
        "Local Policymaker 1",
        "Policy and city-systems perspective on enforcement, data gaps, intergenerational education, elderly homeowner prioritization, and mediation.",
    ),
]
perspective_cols = st.columns(4)
for col, (title, description) in zip(perspective_cols, perspective_cards):
    with col:
        st.markdown(
            f"""
            <div class="profile-card">
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
        quote_html = quote_block(quote)
        st.markdown(
            f"""
            <div class="summary-card">
                <span class="rq-badge">Interview message</span>
                <h3>{title}</h3>
                <p>{explanation}</p>
                {quote_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

section_h2("evidence-highlights", "Interview Evidence Highlights")
st.markdown(
    """
    <p class="section-subtitle">
    These highlights translate the strongest recurring interview patterns into a compact reader guide.
    The theme explorer below keeps the fuller evidence set available.
    </p>
    """,
    unsafe_allow_html=True,
)
highlight_cards = [
    (
        "Multilevel impacts",
        [
            "Financial impacts and loss of wealth-building opportunities",
            "Chronic stress and psychological burden",
            "Unsafe living conditions and housing instability",
            "Family dynamics and interpersonal conflict",
        ],
        [],
    ),
    (
        "Social patterns and demographic concentration",
        [
            "Interviewees described concentration among Black, older, and long-term homeowners.",
            "Several participants connected title risk to Baltimore's Black Butterfly geography.",
            "Some barriers are also cultural and intergenerational: families may avoid death, inheritance, and estate-planning conversations.",
        ],
        [
            "Our population (clients) is about 90% Black and mostly seniors.",
            "The communities that they serve are mostly the Black Butterfly region. Most of the times it is the Black Butterfly region.",
            "Grown people's business was grown people's business.",
        ],
    ),
    (
        "Barriers and systemic gaps",
        [
            "Residents often do not know where to start.",
            "Repair or aid applications can become dead-on-arrival when formal ownership is unresolved.",
            "Referral systems may connect residents to legal providers without tracking whether the barrier is actually resolved.",
            "City data and enforcement gaps can obscure how many properties are affected by informal or unresolved ownership.",
        ],
        [
            "People don't know what they don't know.",
            "So rather than finding it out in court, which is too expensive; they just let it go. And so that is, I think, I would say that's probably the biggest.",
            "Other barriers are connected to human psychology and, partly, American culture. We do not interface with death or deal with death very well. Death is not at the forefront of our minds, so people may think estate planning is just something they will do when it happens, rather than something they should plan for.",
        ],
    ),
    (
        "Facilitators and prevention",
        [
            "Early legal aid and title clearing are easier before more heirs and documents accumulate.",
            "Community partnerships can prioritize older homeowners and high-risk neighborhoods.",
            "Prevention includes transfer tools, intergenerational education, frontline worker training, repair-program screening, and mediation.",
        ],
        [
            "Now we have legislation that's implemented to where someone doesn't necessarily have access to a lawyer or legal counsel, and they want to transfer the property to their family. Now it's just a document that you can go and you can fill out.",
            "For people accessing grants to repair their homes, is there a way that, in exchange for receiving repair grant money, we can require or strongly encourage them to do estate planning? Can we ask them to go through the process of clearing the title and doing this work while they are still alive?",
            "Can the city partner with someone who offers mediation services, so family members can arrive at a resolution about what to do with the property? It is hard for me to see siblings or any other group of people who own a house together resolving that issue on their own.",
        ],
    ),
]
highlight_columns = st.columns(2)
for idx, (title, bullets, quotes) in enumerate(highlight_cards):
    with highlight_columns[idx % 2]:
        bullet_html = "".join(f"<li>{escape(item)}</li>" for item in bullets)
        quote_html = "".join(quote_block(quote) for quote in quotes)
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="evidence-card evidence-board-card">
                    <span class="rq-badge">Evidence pattern</span>
                    <h3>{escape(title)}</h3>
                    <ul>{bullet_html}</ul>
                    {quote_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

section_h2("interview-word-cloud", "What Came Up Repeatedly in Interviews")
word_intro_col, word_image_col = st.columns([0.68, 0.32], vertical_alignment="center")
with word_intro_col:
    st.markdown(
        """
        <div class="interpretive-lead-card">
            <p class="section-lead">This word cloud is a quick orientation to major interview patterns, not a substitute for the deeper evidence below.</p>
            <p class="section-supporting-text">It helps readers see which ideas, barriers, and processes appeared repeatedly across stakeholder interviews: repairs, deed transfer, estate planning, heirs' property, taxes, family conflict, and community outreach. The selected quotes and theme explorer provide the fuller interpretation.</p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )
with word_image_col:
    render_local_image(
        "interview_recurring_themes.png",
        "image-card compact",
        "Interview evidence and recurring themes.",
    )

st.markdown(
    """
    <div class="figure-container">
        <h3>Recurring interview language</h3>
        <p class="figure-caption">Click a term inside the visualization for a short interpretive note.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_interactive_word_cloud_panel(WORD_CLOUD_TERMS)
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
            speaker = quote_source_for(quote)
            with columns[idx % 2]:
                st.markdown(
                    f"""
                    <div class="evidence-card" style="min-height:285px;">
                        <div class="quote-card">"{escape(quote)}"<br><small>{escape(speaker)}</small></div>
                        <div class="badge-row">
                            <span class="tag-pill">{escape(theme_label)}</span>
                        </div>
                        <p class="muted-note">Theme: {escape(theme["title"] if theme else theme_id)}</p>
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
