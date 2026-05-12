import math
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_style import apply_theme, render_page_toc, section_h2
from tangled_titles_content import (
    INTERVENTION_LEVERAGE_POINTS,
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
    ("interview-word-cloud", "Interview Word Cloud"),
    ("theme-explorer", "Theme Explorer"),
    ("intervention-implications", "Intervention Implications"),
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

    st.markdown("**Related Power Map Nodes**")
    for node in related_nodes:
        if st.button(
            f"View node: {node['label']}",
            key=f"theme-{theme['id']}-node-{node['id']}",
            use_container_width=True,
        ):
            switch_to_power_map(node["id"])

    st.caption(theme["implications"])


def interview_word_frequencies(themes: list[dict]) -> list[tuple[str, int]]:
    stopwords = {
        "and", "the", "that", "with", "they", "this", "from", "when", "have", "into",
        "title", "titles", "tangled", "residents", "property", "home", "homes", "legal",
        "because", "their", "can", "not", "are", "for", "after", "through", "about",
        "often", "may", "issue", "issues", "people", "resident", "ownership",
    }
    aliases = {
        "probate": "probate",
        "repair": "home repair",
        "repairs": "home repair",
        "family": "family conflict",
        "siblings": "family conflict",
        "tax": "tax sale",
        "sale": "tax sale",
        "estate": "estate planning",
        "planning": "estate planning",
        "deed": "deed transfer",
        "deeds": "deed transfer",
        "equity": "home equity",
        "wealth": "wealth loss",
        "black": "Black Butterfly",
        "butterfly": "Black Butterfly",
        "outreach": "community outreach",
        "referral": "warm handoff",
        "handoff": "warm handoff",
        "documents": "document burden",
        "document": "document burden",
        "digital": "digital divide",
        "seniors": "fixed-income seniors",
        "fixed": "fixed-income seniors",
        "foreclosure": "foreclosure",
        "heirs": "heirs",
        "heir": "heirs",
    }
    counts: dict[str, int] = {}
    for theme in themes:
        text = " ".join([theme["title"], theme["short_summary"], " ".join(theme["key_quotes"])]).lower()
        for raw in text.replace("/", " ").replace("-", " ").replace(",", " ").replace(".", " ").split():
            word = raw.strip("!?;:()[]\"'")
            if len(word) < 4 or word in stopwords:
                continue
            term = aliases.get(word, word)
            counts[term] = counts.get(term, 0) + 1
    for theme_label, quote, _theme_id, _node_id in QUOTE_WALL_ITEMS:
        for term in theme_label.split():
            if len(term) > 3:
                counts[theme_label] = counts.get(theme_label, 0) + 2
                break
        for word in quote.lower().replace(",", " ").replace(".", " ").split():
            term = aliases.get(word.strip("!?;:()[]\"'"), "")
            if term:
                counts[term] = counts.get(term, 0) + 1
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:34]


def render_interview_word_cloud(themes: list[dict]) -> None:
    terms = interview_word_frequencies(themes)
    max_count = max(count for _term, count in terms)
    xs = []
    ys = []
    sizes = []
    labels = []
    hover = []
    for idx, (term, count) in enumerate(terms):
        angle = idx * 2.35
        radius = 0.12 + (idx % 7) * 0.12 + (idx // 7) * 0.08
        xs.append(0.5 + radius * math.cos(angle))
        ys.append(0.5 + radius * math.sin(angle) * 0.72)
        sizes.append(18 + 34 * (count / max_count))
        labels.append(term)
        hover.append(f"{term}<br>{count} mentions across curated themes and quotes")

    fig = go.Figure(
        data=go.Scatter(
            x=xs,
            y=ys,
            mode="text",
            text=labels,
            textfont=dict(
                size=sizes,
                color=[
                    "#294943", "#8f3d46", "#6fa8c8", "#c88f2e", "#4f8f5b",
                    "#18312d", "#8a5a35", "#c96b68",
                ]
                * 5,
            ),
            hovertext=hover,
            hovertemplate="%{hovertext}<extra></extra>",
        ),
    )
    fig.update_layout(
        height=460,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="#fffaf0",
        plot_bgcolor="#fffaf0",
        xaxis=dict(visible=False, range=[-0.1, 1.1], fixedrange=True),
        yaxis=dict(visible=False, range=[-0.05, 1.05], fixedrange=True),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


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
st.info(
    "The interview evidence shows that tangled titles are not only a paperwork problem. "
    "They emerge from the interaction of individual knowledge gaps, family relationships, "
    "community service pathways, legal institutions, economic constraints, and racialized housing inequality."
)
st.markdown(
    """
    The interview themes emphasize that residents often do not discover a tangled
    title as an abstract legal issue. They discover it when something urgent
    happens: a roof needs repair, property taxes are overdue, a foreclosure notice
    arrives, a family member dies, or a program says the resident is not legally
    recognized as the homeowner.
    """
)

section_h2("interview-word-cloud", "Interview Word Cloud")
st.markdown(
    """
    This view combines the former quote wall with a word-cloud style summary of
    the interview evidence. Larger terms appear more often across curated themes
    and selected quotes; the cards below keep representative quotes close to the
    themes they support.
    """
)
render_interview_word_cloud(INTERVIEW_THEMES)

with st.expander("Selected quotes behind the word cloud", expanded=True):
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
                    <div class="evidence-card">
                        <div class="mini-quote">"{quote}"</div>
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
                render_theme_card(theme)

section_h2("intervention-implications", "Intervention Implications")
st.markdown(
    """
    The strongest intervention logic is prevention plus proactive outreach.
    Interviews point to estate planning before death, transfer-on-death deeds,
    repair-grant-linked title clearing, mediation for family conflict, legal aid
    clinics, warm handoffs, and data-driven outreach as practical leverage points.
    """
)

for leverage_point, theme_ids in INTERVENTION_LEVERAGE_POINTS:
    with st.expander(leverage_point, expanded=False):
        for theme_id in theme_ids:
            theme = THEME_BY_ID.get(theme_id)
            if not theme:
                continue
            st.markdown(f"**{theme['title']}**")
            st.caption(theme["implications"])
            related_labels = [
                NODE_BY_ID[node_id]["label"]
                for node_id in theme["related_power_nodes"]
                if node_id in NODE_BY_ID
            ]
            st.markdown(
                "Related power nodes: "
                + ", ".join(related_labels)
            )
