"""
Chart builders. Take a laps DataFrame (from data.py's load_laps_data)
instead of a live FastF1 session - the deployed app no longer talks
to FastF1 at runtime.
"""

import plotly.graph_objects as go

from data import get_driver_laps, get_pit_stops, get_tyre_stints


def lap_time_chart(laps_df, driver_code):
    """Line chart: lap number vs lap time for one driver."""
    laps = get_driver_laps(laps_df, driver_code)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=laps['LapNumber'],
        y=laps['LapTimeSeconds'],
        mode='lines+markers',
        name=driver_code,
    ))
    fig.update_layout(
        title=f"{driver_code} — Lap Time Evolution",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
    )
    return fig


def compare_drivers_chart(laps_df, driver_codes):
    """Line chart comparing lap times across multiple drivers."""
    fig = go.Figure()

    for code in driver_codes:
        laps = get_driver_laps(laps_df, code)
        fig.add_trace(go.Scatter(
            x=laps['LapNumber'],
            y=laps['LapTimeSeconds'],
            mode='lines',
            name=code,
        ))

    fig.update_layout(
        title="Lap Time Comparison",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
    )
    return fig


def tyre_stint_chart(laps_df, driver_code):
    """Horizontal bar chart showing each tyre stint as a colored block."""
    stints = get_tyre_stints(laps_df, driver_code)

    compound_colors = {
        'SOFT': '#DA291C',
        'MEDIUM': '#FFD700',
        'HARD': '#FFFFFF',
        'INTERMEDIATE': '#43B02A',
        'WET': '#0067AD',
    }

    fig = go.Figure()
    for _, row in stints.iterrows():
        fig.add_trace(go.Bar(
            x=[row['StintLength']],
            y=[driver_code],
            base=[row['StartLap']],
            orientation='h',
            name=row['Compound'],
            marker_color=compound_colors.get(row['Compound'], '#888888'),
            text=row['Compound'],
            textposition='inside',
            showlegend=False,
        ))

    fig.update_layout(
        title=f"{driver_code} — Tyre Stint Timeline",
        xaxis_title="Lap Number",
        yaxis_title="",
        barmode='stack',
    )
    return fig


def pit_stop_delta_chart(laps_df, driver_codes):
    """Scatter chart: one marker per actual pit stop (the pit-in lap)."""
    fig = go.Figure()

    for code in driver_codes:
        pits = get_pit_stops(laps_df, code)
        pit_in_laps = pits[pits['IsPitIn']]['LapNumber']

        fig.add_trace(go.Scatter(
            x=[code] * len(pit_in_laps),
            y=pit_in_laps,
            mode='markers',
            marker=dict(size=16),
            name=code,
        ))

    fig.update_layout(
        title="Pit Stop Laps by Driver",
        xaxis_title="Driver",
        yaxis_title="Lap Number",
        showlegend=False,
    )
    return fig
