from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from shared_style import apply_theme


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


st.set_page_config(page_title="Quantitative Spatial Patterns", layout="wide")

apply_theme()


@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "tract_data.csv")


tracts = load_data()

st.title("Quantitative Spatial Patterns")
st.markdown(
    """
    This page translates the quantitative work plan into placeholder-ready charts.
    When the quant group shares a GitHub link, GeoJSON, or final interactive map,
    this page can replace the placeholder map without changing the rest of the site.
    """
)

metric_options = {
    "Tangled title risk": "tangled_title_risk",
    "At-risk tangled title count": "at_risk_tangled_title_count",
    "Black homeownership": "black_homeownership_pct",
    "Median property value": "median_property_value",
    "Black-white homeownership difference": "black_white_homeownership_diff",
    "Black-white property value difference": "black_white_property_value_diff",
    "Black mortgage loans per 100 residents": "black_mortgage_loans_per_100",
    "Black median interest rate": "black_median_interest_rate",
    "Black-white interest rate difference": "black_white_interest_rate_diff",
}

st.markdown("### Quant Work Plan Questions")
q1, q2, q3 = st.columns(3)
with q1:
    st.markdown(
        """
        <div class="soft-card">
        <h3>Homeownership and Value</h3>
        <p>Where does Black homeownership exist in Baltimore, and what is the
        median property value of those homes?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with q2:
    st.markdown(
        """
        <div class="soft-card">
        <h3>Mortgage Access</h3>
        <p>How accessible are mortgage loans, and what interest-rate costs do
        Black residents face relative to white residents?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with q3:
    st.markdown(
        """
        <div class="soft-card">
        <h3>Proxy Risk Measure</h3>
        <p>Which tracts show high homeownership, low mortgage lending, and lower
        property value as a proxy signal for tangled title risk?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

metric_label = st.selectbox("Select metric", list(metric_options.keys()))
metric_col = metric_options[metric_label]

left, right = st.columns([1.1, 0.9])

with left:
    map_fig = px.scatter_map(
        tracts,
        lat="lat",
        lon="lon",
        color=metric_col,
        size="at_risk_tangled_title_count",
        hover_name="tract_id",
        hover_data={
            "black_homeownership_pct": ":.1f",
            "black_mortgage_loans_per_100": ":.1f",
            "median_property_value": ":$,.0f",
            "lat": False,
            "lon": False,
        },
        color_continuous_scale=["#fff7dc", "#efc267", "#a9c77b", "#294943"],
        zoom=10,
        height=430,
        title="Placeholder interactive tract map",
    )
    map_fig.update_layout(
        map_style="carto-positron",
        margin=dict(l=0, r=0, t=45, b=0),
    )
    st.plotly_chart(map_fig, width="stretch")

with right:
    st.markdown("### Map Placeholder")
    st.markdown(
        """
        <div class="placeholder-map">
        Final quant map slot: replace with GitHub/GeoJSON/Folium output when the
        quantitative team shares the interactive map.
        </div>
        """,
        unsafe_allow_html=True,
    )
    quant_link = st.text_input("Optional quant GitHub or map link", "")
    if quant_link:
        st.markdown(f"[Open quant output]({quant_link})")

bar_left, bar_right = st.columns([1.3, 0.7])

with bar_left:
    fig = px.bar(
        tracts.sort_values(metric_col, ascending=False).head(10),
        x="tract_id",
        y=metric_col,
        color=metric_col,
        color_continuous_scale=["#fff7dc", "#efc267", "#a9c77b", "#294943"],
        title=f"Top tracts by {metric_label.lower()}",
    )
    fig.update_layout(xaxis_title="Census tract", yaxis_title=metric_label)
    st.plotly_chart(fig, width="stretch")

with bar_right:
    st.markdown("### What This Helps Us Understand")
    st.markdown(
        """
        - Where is Black-owned housing wealth potentially at risk?
        - Do high homeownership tracts also have lower mortgage access?
        - Where does lower property value overlap with proxy risk?
        - Which patterns should qualitative findings help explain?
        """
    )
    st.warning("These charts are descriptive and should not be presented as causal claims.")

scatter = px.scatter(
    tracts,
    x="black_mortgage_loans_per_100",
    y="tangled_title_risk",
    size="at_risk_tangled_title_count",
    color="black_homeownership_pct",
    hover_name="tract_id",
    color_continuous_scale=["#fff7dc", "#efc267", "#a9c77b", "#294943"],
    title="Mortgage access and tangled title proxy risk by tract",
)
scatter.update_layout(
    xaxis_title="Black mortgage loans per 100 residents",
    yaxis_title="Tangled title risk score",
)
st.plotly_chart(scatter, width="stretch")

value_scatter = px.scatter(
    tracts,
    x="black_homeownership_pct",
    y="median_property_value",
    size="tangled_title_risk",
    color="black_white_property_value_diff",
    hover_name="tract_id",
    color_continuous_scale=["#c96b68", "#fff7dc", "#294943"],
    title="Black homeownership and median property value",
)
value_scatter.update_layout(
    xaxis_title="Black homeownership (%)",
    yaxis_title="Median property value",
)
st.plotly_chart(value_scatter, width="stretch")

with st.expander("Tract data table"):
    st.dataframe(tracts, width="stretch", hide_index=True)
