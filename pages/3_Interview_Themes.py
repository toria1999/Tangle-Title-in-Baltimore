from pathlib import Path
import math

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from shared_style import apply_theme


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


st.set_page_config(page_title="Interview Themes", layout="wide")

apply_theme()


@st.cache_data
def load_data():
    themes = pd.read_csv(DATA_DIR / "themes.csv")
    nodes = pd.read_csv(DATA_DIR / "nodes.csv")
    return themes, nodes


themes_df, nodes_df = load_data()


def theme_network(theme_label: str, connected: pd.DataFrame) -> go.Figure:
    center_x, center_y = 0, 0
    count = max(len(connected), 1)
    xs = []
    ys = []
    for idx in range(count):
        angle = 2 * math.pi * idx / count
        xs.append(1.8 * math.cos(angle))
        ys.append(1.2 * math.sin(angle))

    fig = go.Figure()
    for x, y in zip(xs, ys):
        fig.add_trace(
            go.Scatter(
                x=[center_x, x],
                y=[center_y, y],
                mode="lines",
                line=dict(color="#9aa78d", width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[center_x],
            y=[center_y],
            mode="markers+text",
            marker=dict(size=42, color="#294943"),
            text=["Selected theme"],
            textposition="bottom center",
            hovertext=[theme_label],
            hoverinfo="text",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            marker=dict(size=30, color="#efc267", line=dict(color="#18312d", width=1)),
            text=connected["node_id"].tolist(),
            textposition="bottom center",
            hovertext=connected["label"].tolist(),
            hoverinfo="text",
            showlegend=False,
        )
    )
    fig.update_layout(
        height=310,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="#fffaf0",
        paper_bgcolor="#fffaf0",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

st.title("Interview Themes Linked to the Power Map")
st.markdown(
    """
    This page connects qualitative themes to system nodes. It is designed for
    synthesis, not transcript display.
    """
)

theme_label = st.selectbox("Select a theme", themes_df["theme"].tolist())
theme = themes_df.loc[themes_df["theme"] == theme_label].iloc[0]

left, right = st.columns([0.92, 1.08])

with left:
    st.markdown("### Theme Summary")
    st.markdown(theme["summary"])

    st.markdown("### Quote")
    st.markdown(
        f"""
        <div class="quote-card">
        <em>"{theme['quote']}"</em><br>
        <small>{theme['quote_note']}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Evidence Note")
    st.info(theme["evidence_note"])

    st.markdown("### Intervention Meaning")
    st.markdown(theme["intervention_meaning"])

with right:
    connected_ids = [part.strip() for part in str(theme["connected_nodes"]).split(";")]
    connected = nodes_df[nodes_df["node_id"].isin(connected_ids)].copy()

    st.markdown("### Connected Power Map Nodes")
    st.plotly_chart(theme_network(theme_label, connected), width="stretch")
    st.dataframe(
        connected[["node_id", "label", "level", "type", "description"]],
        width="stretch",
        hide_index=True,
    )

st.markdown("### Synthesis Interpretation")
st.markdown(
    """
    The point is not only that residents face barriers. The synthesis question is
    where those barriers enter the system, how they become administrative or
    economic exclusion, and what type of intervention is best matched to that
    pathway.
    """
)
