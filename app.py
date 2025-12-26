import streamlit as st
import plotly.express as px
from database.queries import *

st.set_page_config(page_title="War Dashboard", layout="wide")
st.title("War & Conflict Analysis Dashboard")

# -------- SIDEBAR --------
conflicts = load_conflicts()
st.sidebar.header("Filters")

# choose a default conflict that has casualty data when possible
try:
    from database.queries import casualties_heatmap
    available_ids = list(casualties_heatmap()["conflict_id"].unique())
except Exception:
    available_ids = []

default_id = available_ids[0] if available_ids else int(conflicts["id"].iloc[0])
conflict_id = st.sidebar.selectbox(
    "Select Conflict",
    conflicts["id"],
    index=int(conflicts["id"].tolist().index(int(default_id)))
)

year_range = st.sidebar.slider(
    "Select Year Range",
    1900, 2025, (1950, 2025)
)

# -------- KPIs --------
kpis = kpi_metrics()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Conflicts", kpis["total_conflicts"])
c2.metric("Active Conflicts", kpis["active_conflicts"])
c3.metric("Civilian Deaths", f"{kpis['civilian_deaths']:,}")
c4.metric("Military Deaths", f"{kpis['military_deaths']:,}")

# -------- TABLE --------
st.subheader("Conflicts Table")
st.dataframe(conflicts, width='stretch')

# -------- LINE CHART --------
casualties = load_casualties(conflict_id, year_range)
st.subheader("Casualties Over Time")
if casualties.empty:
    st.info("No casualty data for the selected conflict and year range.")
else:
    fig_line = px.line(
        casualties,
        x="year",
        y=["civilian_deaths", "military_deaths"]
    )
    st.plotly_chart(fig_line, width='stretch')

# -------- TIMELINE --------
st.subheader("Conflict Timeline")
timeline_df = conflict_timeline()
fig_timeline = px.timeline(
    timeline_df,
    x_start="start",
    x_end="end",
    y="name",
    color="status"
)
fig_timeline.update_yaxes(autorange="reversed")
st.plotly_chart(fig_timeline, width='stretch')

# -------- HEAT MAP --------
st.subheader("Conflict Intensity Heat Map")
heat_df = casualties_heatmap()
fig_heat = px.density_heatmap(
    heat_df,
    x="year",
    y="conflict_id",
    z="total_deaths",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig_heat, width='stretch')

# -------- MAP --------
st.subheader("Geographic Distribution of Conflicts")
map_df = countries_conflict_count()
fig_map = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    size="conflicts_count",
    color="continent",
    hover_name="name",
    projection="natural earth"
)
st.plotly_chart(fig_map, width='stretch')
