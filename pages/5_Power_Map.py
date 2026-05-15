import sys
import base64
from html import escape
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
PLACEHOLDER_DIR = ROOT_DIR / "assets" / "placeholders"

from shared_style import apply_theme, render_page_toc, section_h2
from tangled_titles_content import (
    INTERVENTION_LEVERAGE_POINTS,
    LEVELS,
    LEVEL_ORDER,
    NODE_BY_ID,
    POWER_NODES,
    STRUCTURAL_SUBLEVELS,
    SYSTEM_TOUCHPOINT_LANES,
    THEME_BY_ID,
    related_quotes_for_node,
    themes_for_node,
)
try:
    from tangled_titles_content import QUALITATIVE_SLIDE_RESOURCE_LINKS
except ImportError:
    QUALITATIVE_SLIDE_RESOURCE_LINKS = []


st.set_page_config(page_title="Power Map", layout="wide")
apply_theme()

POWER_MAP_TOC = (
    ("overview", "Overview"),
    ("hierarchical-power-map", "Hierarchical Power Map"),
    ("system-touchpoint-map", "System Touchpoint Map"),
    ("intervention-leverage-points", "Intervention Leverage Points"),
)
render_page_toc("power-map", POWER_MAP_TOC)


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


def switch_to_interview(theme_id: str) -> None:
    st.session_state["selected_section"] = "Interview"
    st.session_state["selected_theme"] = theme_id
    st.switch_page("pages/4_Interview.py")


def type_badge(node_type: str) -> str:
    colors = {
        "Barrier": "#c96b68",
        "Facilitator": "#4f8f5b",
        "Mixed": "#8a5a35",
    }
    icons = {"Barrier": "Lock", "Facilitator": "Bridge", "Mixed": "Two-way"}
    return (
        f'<span class="type-badge" style="background:{colors.get(node_type, "#294943")};">'
        f'<span class="badge-icon">{icons.get(node_type, "Node")}</span>{node_type}</span>'
    )


def level_badge(level: str) -> str:
    color = LEVELS.get(level, {}).get("color", "#d7e8bd")
    icons = {
        "Central Issue": "Home",
        "Individual Level Factors": "Person",
        "Interpersonal Level Factors": "Family",
        "Community Level Factors": "Neighborhood",
        "Policy-Level Determinants": "Policy",
        "Economic-Level Determinants": "Tax",
        "Societal Determinants": "City",
    }
    return (
        f'<span class="level-badge" style="background:{color};">'
        f'<span class="badge-icon">{icons.get(level, "Level")}</span>{level}</span>'
    )


def level_background(level: str) -> str:
    colors = {
        "Individual Level Factors": "#edf6fa",
        "Interpersonal Level Factors": "#fdecef",
        "Community Level Factors": "#fff7dc",
        "Policy-Level Determinants": "#eef7e8",
        "Economic-Level Determinants": "#eef7e8",
        "Societal Determinants": "#eef7e8",
    }
    return colors.get(level, "#fffaf0")


def node_matches_filters(node: dict, levels: list[str], node_types: list[str], query: str) -> bool:
    if levels and node["level"] not in levels:
        return False
    if node_types and node["type"] not in node_types:
        return False
    if not query:
        return True
    related_theme_text = " ".join(
        THEME_BY_ID[theme_id]["title"]
        for theme_id in node["related_interview_themes"]
        if theme_id in THEME_BY_ID
    )
    haystack = " ".join(
        [
            node["id"],
            node["label"],
            node["level"],
            node["type"],
            node["description"],
            related_theme_text,
        ]
    ).lower()
    return query.lower() in haystack


def plot_node_number(node_id: str) -> int:
    node_ids = [node["id"] for node in POWER_NODES if node["id"] != "tangled_titles"]
    return node_ids.index(node_id) + 1 if node_id in node_ids else 0


def selected_node_id_from_plot_state(plot_state) -> str | None:
    """Read a clicked Plotly point from Streamlit's selection event."""
    if not plot_state:
        return None
    try:
        points = plot_state.selection.points
    except AttributeError:
        points = plot_state.get("selection", {}).get("points", []) if isinstance(plot_state, dict) else []
    if not points:
        return None
    point = points[0]
    customdata = getattr(point, "customdata", None)
    if customdata is None and isinstance(point, dict):
        customdata = point.get("customdata")
    return customdata if isinstance(customdata, str) else None


def render_structured_power_plot(nodes: list[dict]) -> str | None:
    """Render a fixed-position ecosystem map with no force layout or overlapping labels."""
    level_sequence = [
        "Individual Level Factors",
        "Interpersonal Level Factors",
        "Community Level Factors",
        "Policy-Level Determinants",
        "Economic-Level Determinants",
        "Societal Determinants",
    ]
    level_short_labels = {
        "Individual Level Factors": "Individual",
        "Interpersonal Level Factors": "Interpersonal",
        "Community Level Factors": "Community",
        "Policy-Level Determinants": "Policy",
        "Economic-Level Determinants": "Economic",
        "Societal Determinants": "Societal",
    }
    type_colors = {"Barrier": "#c96b68", "Facilitator": "#4f8f5b", "Mixed": "#8a5a35"}
    type_symbols = {"Barrier": "circle", "Facilitator": "diamond", "Mixed": "square"}

    x_centers = {level: idx * 2.35 for idx, level in enumerate(level_sequence)}
    central_x = (min(x_centers.values()) + max(x_centers.values())) / 2
    central_y = 5.2
    header_y = 4.15
    node_start_y = 3.2
    row_gap = 0.58
    col_gap = 0.68

    fig = go.Figure()

    # Central issue to level headers.
    for level in level_sequence:
        x = x_centers[level]
        fig.add_trace(
            go.Scatter(
                x=[central_x, x],
                y=[central_y - 0.18, header_y + 0.1],
                mode="lines",
                line=dict(color="rgba(41,73,67,0.18)", width=1.2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[central_x],
            y=[central_y],
            mode="markers+text",
            marker=dict(size=58, color="#4f8f5b", line=dict(width=2.4, color="#18312d")),
            text=["Tangled<br>Titles"],
            textposition="middle center",
            textfont=dict(size=12, color="#ffffff"),
            hovertemplate="<b>Tangled Titles</b><br>Central issue<extra></extra>",
            showlegend=False,
        )
    )

    for level in level_sequence:
        level_nodes = sorted(
            [node for node in nodes if node["level"] == level],
            key=lambda item: (item["type"], item["label"]),
        )
        x_center = x_centers[level]
        level_color = LEVELS.get(level, {}).get("color", "#d7e8bd")
        fig.add_trace(
            go.Scatter(
                x=[x_center],
                y=[header_y],
                mode="markers",
                marker=dict(size=28, color=level_color, line=dict(width=1.5, color="#18312d")),
                hovertemplate=f"<b>{level}</b><br>{len(level_nodes)} visible nodes<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_annotation(
            x=x_center,
            y=header_y + 0.38,
            text=f"<b>{level_short_labels[level]}</b>",
            showarrow=False,
            font=dict(size=12, color="#18312d"),
        )

        xs: list[float] = []
        ys: list[float] = []
        texts: list[str] = []
        colors: list[str] = []
        symbols: list[str] = []
        hover_texts: list[str] = []
        node_ids: list[str] = []

        for idx, node in enumerate(level_nodes):
            columns = 2
            col = idx % columns
            row = idx // columns
            x = x_center + (col - 0.5) * col_gap
            y = node_start_y - row * row_gap
            number = plot_node_number(node["id"])
            related_titles = [
                THEME_BY_ID[theme_id]["title"]
                for theme_id in node["related_interview_themes"]
                if theme_id in THEME_BY_ID
            ]

            fig.add_trace(
                go.Scatter(
                    x=[x_center, x],
                    y=[header_y - 0.16, y + 0.14],
                    mode="lines",
                    line=dict(color="rgba(41,73,67,0.12)", width=1),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            xs.append(x)
            ys.append(y)
            texts.append(str(number))
            colors.append(type_colors.get(node["type"], "#294943"))
            symbols.append(type_symbols.get(node["type"], "circle"))
            node_ids.append(node["id"])
            hover_texts.append(
                "<br>".join(
                    [
                        f"<b>{number}. {node['label']}</b>",
                        f"{node['level']} · {node['type']}",
                        node["description"],
                        "<b>Interview themes:</b> " + "; ".join(related_titles[:4]),
                    ]
                )
            )

        if xs:
            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers+text",
                    marker=dict(
                        size=30,
                        color=colors,
                        symbol=symbols,
                        line=dict(width=1.5, color="#fffaf0"),
                    ),
                    text=texts,
                    textposition="middle center",
                    textfont=dict(size=10, color="#ffffff"),
                    hovertext=hover_texts,
                    hovertemplate="%{hovertext}<extra></extra>",
                    customdata=node_ids,
                    showlegend=False,
                )
            )

    for node_type, color in type_colors.items():
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=12, color=color, symbol=type_symbols[node_type]),
                name=node_type,
            )
        )

    fig.update_layout(
        height=720,
        margin=dict(l=10, r=10, t=30, b=20),
        paper_bgcolor="#fffaf0",
        plot_bgcolor="#fffaf0",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
    )
    plot_state = st.plotly_chart(
        fig,
        width="stretch",
        key="structured-power-plot",
        on_select="rerun",
        selection_mode="points",
        config={"displayModeBar": False},
    )
    return selected_node_id_from_plot_state(plot_state)


def render_node_card(node: dict, detail: bool = False, key_prefix: str = "node", show_select_button: bool = True) -> None:
    first_sentence = node["description"].split(".")[0].strip() + "."
    st.markdown(
        f"""
        <div class="reference-card" id="node-{node["id"]}">
            <div class="badge-row">
                {level_badge(node["level"])}
                {type_badge(node["type"])}
            </div>
            <h3>{node["label"]}</h3>
            <p>{first_sentence}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    related_themes = themes_for_node(node["id"])
    if related_themes:
        with st.expander("Related interview evidence", expanded=detail):
            st.markdown(node["description"])
            for theme in related_themes[:5]:
                if st.button(
                    f"View interview evidence: {theme['title']}",
                    key=f"{key_prefix}-{node['id']}-theme-{theme['id']}",
                    use_container_width=True,
                ):
                    switch_to_interview(theme["id"])

    if detail:
        quotes = related_quotes_for_node(node["id"], limit=5)
        if quotes:
            with st.expander("Selected supporting quotes", expanded=False):
                for theme_title, quote in quotes:
                    st.markdown(
                        f'<div class="mini-quote">"{quote}"<br><small>{theme_title}</small></div>',
                        unsafe_allow_html=True,
                    )

    if show_select_button:
        if st.button(
            "Show details here",
            key=f"{key_prefix}-select-node-{node['id']}",
            use_container_width=True,
        ):
            st.session_state["selected_node"] = node["id"]
            st.rerun()


def render_level(level: str, nodes: list[dict], expanded: bool = False) -> None:
    if not nodes:
        return
    color = LEVELS.get(level, {}).get("color", "#d7e8bd")
    st.markdown(
        f"""
        <div class="hierarchy-level" style="--level-color:{color};">
            <h3>{level}</h3>
            <p class="muted-note">{len(nodes)} nodes shown. Items are laid out as cards to avoid overlap.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for node_type in ("Barrier", "Facilitator", "Mixed"):
        typed_nodes = [node for node in nodes if node["type"] == node_type]
        if not typed_nodes:
            continue
        with st.expander(f"{node_type}s ({len(typed_nodes)})", expanded=expanded):
            columns = st.columns(2)
            for idx, node in enumerate(typed_nodes):
                with columns[idx % 2]:
                    render_node_card(node, key_prefix=f"hierarchy-{level}-{node_type}")


selected_node_id = st.session_state.get("selected_node")
selected_node = NODE_BY_ID.get(selected_node_id) if selected_node_id else None

intro_text_col, intro_image_col = st.columns([0.62, 0.38], vertical_alignment="center")
with intro_text_col:
    st.title("Power Map")
    st.markdown(
        """
        <div class="report-intro">
        <p>
        Tangled titles are not caused by one missing form. They emerge when family
        inheritance, legal records, repair programs, tax systems, and housing markets
        fail to recognize the same person as the homeowner.
        </p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="overview-inline-card" id="overview">
            <h2>Overview</h2>
            <p><strong>Which systems create or reduce tangled title risk?</strong> The map shows where individual knowledge gaps, family conflict, community services, legal systems, tax pressure, and structural inequality become connected.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with intro_image_col:
    render_local_image(
        "power_map_system_touchpoints.png",
        "image-card medium",
        "System touchpoints around tangled title risk.",
    )

if selected_node:
    st.markdown(
        f"""
        <div class="detail-panel">
            <strong>Selected node:</strong><br>
            {selected_node["label"]}
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_node_card(selected_node, detail=True, key_prefix="selected")
    if st.button("Clear selected node", key="clear-selected-node"):
        st.session_state.pop("selected_node", None)
        st.rerun()

section_h2("hierarchical-power-map", "Hierarchical Power Map")
central = NODE_BY_ID["tangled_titles"]
st.markdown(
    f"""
    <div class="central-issue-card">
        <div class="badge-row">{level_badge(central["level"])} {type_badge(central["type"])}</div>
        <h3>{central["label"]}</h3>
        <p>{central["description"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Power Map Filters")
level_filter = st.sidebar.multiselect(
    "Level",
    [level for level in LEVEL_ORDER if level != "Central Issue"],
    default=[],
)
type_filter = st.sidebar.multiselect("Node type", ["Barrier", "Facilitator", "Mixed"], default=[])
search = st.sidebar.text_input(
    "Search nodes",
    placeholder="probate, repair, tax sale, family conflict...",
)

filtered_nodes = [
    node
    for node in POWER_NODES
    if node["id"] != "tangled_titles" and node_matches_filters(node, level_filter, type_filter, search.strip())
]

with st.container(border=True):
    st.markdown(
        """
        <div class="figure-container">
            <h3>Structured Interactive Plot</h3>
            <p class="figure-caption">The plot uses fixed positions: columns are ecosystem levels, node numbers are stable, and hover reveals the full label, description, and related interview themes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    clicked_plot_node_id = render_structured_power_plot(filtered_nodes)
    if clicked_plot_node_id:
        st.session_state["plot_selected_node"] = clicked_plot_node_id
        components.html(
            """
            <script>
            setTimeout(() => {
                const target = window.parent.document.getElementById("plot-node-detail");
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }, 150);
            </script>
            """,
            height=0,
        )
    if filtered_nodes:
        st.caption("Click any numbered node in the plot to open its detail panel below.")
    else:
        st.warning("No nodes match the current filters.")

    filtered_node_ids = {node["id"] for node in filtered_nodes}
    plot_detail_node = NODE_BY_ID.get(st.session_state.get("plot_selected_node"))
    if plot_detail_node and plot_detail_node["id"] in filtered_node_ids:
        st.markdown(
            """
            <div class="detail-panel" id="plot-node-detail">
                <span class="tag-pill">Selected node detail</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_node_card(
            plot_detail_node,
            detail=True,
            key_prefix="plot-detail",
            show_select_button=False,
        )

with st.expander("Node number key", expanded=False):
    key_rows = [
        {
            "#": plot_node_number(node["id"]),
            "Node": node["label"],
            "Level": node["level"],
            "Type": node["type"],
        }
        for node in sorted(filtered_nodes, key=lambda item: plot_node_number(item["id"]))
    ]
    st.dataframe(key_rows, width="stretch", hide_index=True, height=260)

primary_levels = [
    "Individual Level Factors",
    "Interpersonal Level Factors",
    "Community Level Factors",
]
for level in primary_levels:
    render_level(level, [node for node in filtered_nodes if node["level"] == level], expanded=False)

st.markdown("### Structural Factors")
st.caption("Structural factors are split into policy, economic, and societal determinants.")
structural_tabs = st.tabs(["Policy", "Economic", "Societal"])
for tab, level in zip(structural_tabs, STRUCTURAL_SUBLEVELS):
    with tab:
        render_level(level, [node for node in filtered_nodes if node["level"] == level], expanded=False)

section_h2("system-touchpoint-map", "System Touchpoint Map")
touchpoint_text_col, touchpoint_image_col = st.columns([0.68, 0.32], vertical_alignment="center")
with touchpoint_text_col:
    st.markdown(
        """
        <div class="interpretive-lead-card">
            <p class="section-lead">Touchpoints are the moments when the broader ecosystem becomes visible to residents in everyday life.</p>
            <p class="section-supporting-text">They often appear when a death in the family, urgent repair need, tax notice, probate issue, or paperwork mismatch forces someone to seek help. The map shows where fragmented systems become relevant and where support or intervention can enter.</p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )
with touchpoint_image_col:
    render_local_image(
        "community.jpg",
        "image-card compact",
        "Community touchpoints and resident-facing outreach.",
    )
touchpoint_levels = {
    "Resident / household": "Individual Level Factors",
    "Family / interpersonal actors": "Interpersonal Level Factors",
    "Community support actors": "Community Level Factors",
    "Housing and legal service providers": "Community Level Factors",
    "Formal legal and administrative systems": "Policy-Level Determinants",
    "Tax and municipal systems": "Economic-Level Determinants",
    "Data and spatial targeting actors": "Societal Determinants",
    "Market actors": "Economic-Level Determinants",
}
touchpoint_cols = st.columns(2)
for idx, lane in enumerate(SYSTEM_TOUCHPOINT_LANES):
    with touchpoint_cols[idx % 2]:
        level = touchpoint_levels.get(lane["lane"], "Community Level Factors")
        border_color = LEVELS.get(level, {}).get("color", "#d7e8bd")
        background = level_background(level)
        st.markdown(
            f"""
            <div class="profile-card" style="background:{background}; border-left:8px solid {border_color};">
                <div class="badge-row">{level_badge(level)}</div>
                <h3>{idx + 1}. {lane["lane"]}</h3>
                <p><strong>Actors:</strong> {", ".join(lane["examples"])}</p>
                <p class="muted-note"><strong>Resident encounters:</strong> {", ".join(lane["encounters"])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

section_h2("intervention-leverage-points", "Intervention Leverage Points")
st.markdown(
    """
    <p class="section-subtitle">The strongest intervention logic is prevention plus proactive outreach. Detailed evidence is collapsed below.</p>
    """
    ,
    unsafe_allow_html=True,
)

with st.expander("Explore intervention leverage points", expanded=False):
    leverage_cols = st.columns(2)
    for idx, (leverage_point, theme_ids) in enumerate(INTERVENTION_LEVERAGE_POINTS):
        with leverage_cols[idx % 2]:
            themes = [THEME_BY_ID.get(theme_id) for theme_id in theme_ids]
            themes = [theme for theme in themes if theme]
            summary = themes[0]["implications"] if themes else "Connect this leverage point to related interview evidence."
            theme_rows = "".join(
                (
                    "<li>"
                    f'<a class="action-bullet-link" href="/Interview?theme={escape(theme["id"])}#selected-interview-evidence" target="_self">'
                    f"<strong>{escape(theme['title'])}</strong><br>"
                    f"{escape(theme['implications'])}"
                    '<br><span class="link-cue">View in Interview evidence</span>'
                    "</a>"
                    "</li>"
                )
                for theme in themes
            )
            st.markdown(
                (
                    '<div class="action-tile">'
                    '<div class="action-kicker">'
                    '<span class="tag-pill">Leverage point</span>'
                    f'<span class="action-number">{idx + 1}</span>'
                    '</div>'
                    f'<h3>{escape(leverage_point)}</h3>'
                    f'<p class="action-summary">{escape(summary)}</p>'
                    '<p class="action-button-note"><strong>Evidence connections</strong></p>'
                    f'<ul class="action-bullet-list">{theme_rows}</ul>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

implementation_text_col, implementation_image_col = st.columns([0.62, 0.38], vertical_alignment="center")
with implementation_text_col:
    st.markdown(
        """
        <div class="key-takeaway-card">
            <strong>Implementation requires coordination.</strong>
            Local legal, housing, financial, community, and tax-sale prevention resources sit across the same ecosystem shown above.
        </div>
        """,
        unsafe_allow_html=True,
    )
with implementation_image_col:
    render_local_image(
        "implentation resoureces.png",
        "image-card implementation",
        "Legal paperwork and service coordination.",
    )

with st.expander("Local implementation resources", expanded=False):
    st.markdown(
        "These links supplement the intervention logic with concrete local planning, legal aid, financial counseling, and tax-sale prevention touchpoints."
    )
    resource_cols = st.columns(2)
    for idx, resource in enumerate(QUALITATIVE_SLIDE_RESOURCE_LINKS):
        with resource_cols[idx % 2]:
            st.markdown(
                f"""
                <div class="link-card">
                    <span class="tag-pill">Local resource</span>
                    <h3><a href="{escape(resource['url'])}" target="_blank">{escape(resource['label'])}</a></h3>
                    <p>{escape(resource['focus'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

render_local_image(
    "interview_stakeholder_evidence.png",
    "image-card stakeholder",
    "Community-facing stakeholder engagement and outreach.",
)
