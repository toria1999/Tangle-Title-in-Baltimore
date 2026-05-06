from pathlib import Path
import tempfile

import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from shared_style import apply_theme

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

TYPE_COLORS = {
    "barrier": "#c96b68",
    "facilitator": "#a9c77b",
    "formal actor": "#6fa8c8",
    "community actor": "#efc267",
    "structural determinant": "#294943",
}


st.set_page_config(page_title="Power Map", layout="wide")

apply_theme()

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #8a5a35 !important;
        border-color: #6f4528 !important;
        color: #fffaf0 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="tag"] span,
    section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: #fffaf0 !important;
        fill: #fffaf0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    nodes = pd.read_csv(DATA_DIR / "nodes.csv")
    edges = pd.read_csv(DATA_DIR / "edges.csv")
    return nodes, edges


def contains_source(value: str, selected: list[str]) -> bool:
    parts = {part.strip().lower() for part in str(value).split(";")}
    return any(item.lower() in parts for item in selected)


def build_network(nodes: pd.DataFrame, edges: pd.DataFrame) -> str:
    graph = nx.Graph()

    for _, row in nodes.iterrows():
        color = TYPE_COLORS.get(str(row["type"]).lower(), "#8a93a6")
        title = (
            f"<b>{row['label']}</b><br>"
            f"Level: {row['level']}<br>"
            f"Type: {row['type']}<br>"
            f"Evidence: {row['evidence_source']}<br><br>"
            f"{row['description']}"
        )
        graph.add_node(
            row["node_id"],
            label=row["label"],
            title=title,
            color=color,
            level=row["level"],
            group=row["type"],
        )

    visible_ids = set(nodes["node_id"])
    for _, row in edges.iterrows():
        if row["source"] in visible_ids and row["target"] in visible_ids:
            graph.add_edge(
                row["source"],
                row["target"],
                title=f"{row['relationship']}: {row['mechanism']}",
                label=row["relationship"],
            )

    net = Network(
        height="690px",
        width="100%",
        bgcolor="#fffaf0",
        font_color="#18312d",
        notebook=False,
        cdn_resources="remote",
    )
    net.from_nx(graph)
    net.barnes_hut(gravity=-18000, central_gravity=0.2, spring_length=180, damping=0.35)
    net.set_options(
        """
        const options = {
          "nodes": {
            "borderWidth": 1,
            "borderWidthSelected": 3,
            "font": {"size": 18, "face": "Arial", "strokeWidth": 4, "strokeColor": "#ffffff"},
            "shape": "box",
            "margin": 12,
            "widthConstraint": {"maximum": 190}
          },
            "edges": {
            "color": {"color": "#9aa78d", "highlight": "#18312d"},
            "font": {"size": 10, "align": "middle"},
            "smooth": {"type": "dynamic"}
          },
          "interaction": {"hover": true, "navigationButtons": true, "keyboard": true},
          "physics": {"stabilization": {"iterations": 180}}
        }
        """
    )

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        net.save_graph(f.name)
        return Path(f.name).read_text(encoding="utf-8")


nodes_df, edges_df = load_data()

st.title("Interactive Power Map")
st.markdown(
    """
    Use filters to view parts of the tangled title system. Hover over a node to see
    its description and evidence source; drag and zoom to explore relationships.
    """
)

all_sources = sorted(
    {
        part.strip()
        for value in nodes_df["evidence_source"].dropna()
        for part in str(value).split(";")
    }
)

with st.sidebar:
    st.header("Power Map Filters")
    selected_levels = st.multiselect(
        "Level",
        sorted(nodes_df["level"].dropna().unique()),
        default=sorted(nodes_df["level"].dropna().unique()),
    )
    selected_types = st.multiselect(
        "Node type",
        sorted(nodes_df["type"].dropna().unique()),
        default=sorted(nodes_df["type"].dropna().unique()),
    )
    selected_sources = st.multiselect(
        "Evidence source",
        all_sources,
        default=all_sources,
    )
    search = st.text_input("Search node", "")

filtered = nodes_df[
    nodes_df["level"].isin(selected_levels)
    & nodes_df["type"].isin(selected_types)
    & nodes_df["evidence_source"].apply(lambda value: contains_source(value, selected_sources))
].copy()

if search:
    query = search.lower()
    filtered = filtered[
        filtered["label"].str.lower().str.contains(query)
        | filtered["description"].str.lower().str.contains(query)
    ]

html = build_network(filtered, edges_df)
components.html(html, height=720, scrolling=False)

st.caption(f"Showing {len(filtered)} of {len(nodes_df)} nodes.")

with st.expander("Filtered nodes table", expanded=False):
    st.dataframe(
        filtered[["node_id", "label", "level", "type", "evidence_source", "description"]],
        width="stretch",
        hide_index=True,
    )

st.markdown("### What This Part of the System Means")
st.markdown(
    """
    Read the map as an explanatory framework: barriers can appear at individual,
    interpersonal, community, policy, economic, and societal levels, while
    facilitators show where navigation, legal help, outreach, or administrative
    change may reduce harm.
    """
)
