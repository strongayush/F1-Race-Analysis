"""
F1 Race Performance & Strategy Analysis - Streamlit app.
Reads pre-exported lap data from CSV (see export_data.py) instead of
calling FastF1 live, so it works reliably once deployed.
"""

import streamlit as st

from data import load_laps_data
from charts import lap_time_chart, compare_drivers_chart, tyre_stint_chart, pit_stop_delta_chart

st.set_page_config(page_title="F1 Race Analysis",
                   page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Race Performance & Strategy Analysis")
st.caption("2024 Abu Dhabi Grand Prix — Race")
st.markdown(
    "Explore real race data — lap-by-lap pace, tyre strategy, and pit stop "
    "timing — for any driver from the 2024 season finale. Built with "
    "[FastF1](https://github.com/theOehrly/Fast-F1), pandas, Plotly, and Streamlit."
)

# A plain DataFrame caches cleanly with st.cache_data (unlike a live
# FastF1 Session object, which doesn't survive serialization intact).


@st.cache_data
def get_data():
    return load_laps_data()


laps_df = get_data()

st.success(
    f"Loaded: {laps_df['Driver'].nunique()} drivers, {len(laps_df)} laps")

all_drivers = sorted(laps_df['Driver'].unique())

st.sidebar.header("Controls")
main_driver = st.sidebar.selectbox(
    "Driver for lap time / tyre stint view",
    options=all_drivers,
    index=all_drivers.index('VER') if 'VER' in all_drivers else 0,
)
compare_drivers = st.sidebar.multiselect(
    "Drivers to compare",
    options=all_drivers,
    default=[d for d in ['VER', 'NOR', 'LEC'] if d in all_drivers],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Built by [Ayush](https://strongayush.github.io) · "
    "[GitHub](https://github.com/strongayush)"
)

st.header(f"{main_driver} — Lap Time Evolution")
st.plotly_chart(lap_time_chart(laps_df, main_driver), use_container_width=True)

if compare_drivers:
    st.header("Lap Time Comparison")
    st.plotly_chart(compare_drivers_chart(
        laps_df, compare_drivers), use_container_width=True)
else:
    st.info("Select at least one driver in the sidebar to see the comparison chart.")

st.header(f"{main_driver} — Tyre Stint Timeline")
st.plotly_chart(tyre_stint_chart(laps_df, main_driver),
                use_container_width=True)

if compare_drivers:
    st.header("Pit Stop Laps by Driver")
    st.plotly_chart(pit_stop_delta_chart(
        laps_df, compare_drivers), use_container_width=True)
else:
    st.info("Select at least one driver in the sidebar to see pit stop laps.")
