"""
Checkpoint 3: Static charts (still no Streamlit)
Goal: get the actual visualizations looking right, using hardcoded
inputs. Once these look good, Checkpoint 4 just wraps them in Streamlit.
"""

import plotly.graph_objects as go
import plotly.express as px

from data import load_session, get_driver_laps, get_all_drivers_laps, get_tyre_stints, get_pit_stops


def lap_time_chart(session, driver_code):
    """
    Line chart: lap number vs lap time for one driver.
    Shows pace evolution and any spikes (traffic, pit laps, etc.)
    """
    laps = get_driver_laps(session, driver_code)

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


def compare_drivers_chart(session, driver_codes):
    """
    Line chart comparing lap times across multiple drivers.
    driver_codes: list like ['VER', 'HAM', 'LEC']
    """
    fig = go.Figure()

    for code in driver_codes:
        laps = get_driver_laps(session, code)
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


def tyre_stint_chart(session, driver_code):
    """
    Horizontal bar chart showing each tyre stint as a colored block
    across the lap range it covered.
    """
    stints = get_tyre_stints(session, driver_code)

    # Rough but recognizable F1 tyre colors
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


def pit_stop_delta_chart(session, driver_codes):
    """
    Scatter chart: one marker per actual pit stop, at the lap the
    driver entered the pits. Useful for spotting undercut/overcut
    strategy battles (who pitted first, who reacted).
    """
    fig = go.Figure()

    for code in driver_codes:
        pits = get_pit_stops(session, code)

        # get_pit_stops returns a row for PitInTime AND a separate row
        # for PitOutTime - keep only the "pit in" lap so each real
        # stop counts once, not twice.
        pit_in_laps = pits[pits['PitInTime'].notna()]['LapNumber']

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


if __name__ == '__main__':
    # Hardcoded test - Verstappen vs a couple of rivals from the same race
    session = load_session(2024, 'Abu Dhabi', 'R')

    drivers_to_compare = ['VER', 'NOR', 'LEC']

    fig1 = lap_time_chart(session, 'VER')
    fig1.write_html('chart1_lap_times_VER.html')

    fig2 = compare_drivers_chart(session, drivers_to_compare)
    fig2.write_html('chart2_comparison.html')

    fig3 = tyre_stint_chart(session, 'VER')
    fig3.write_html('chart3_tyre_stints_VER.html')

    fig4 = pit_stop_delta_chart(session, drivers_to_compare)
    fig4.write_html('chart4_pit_stops.html')

    print("Done! 4 HTML files written to your project folder.")
    print("Open each one in your browser to check how it looks:")
    print(" - chart1_lap_times_VER.html")
    print(" - chart2_comparison.html")
    print(" - chart3_tyre_stints_VER.html")
    print(" - chart4_pit_stops.html")
