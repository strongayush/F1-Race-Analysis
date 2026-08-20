"""
Checkpoint 2: Clean, reusable data functions
Goal: wrap raw FastF1 access into functions we can call from
anywhere (charts.py, the Streamlit app) without repeating logic.

Test this file on its own first (see bottom) before touching
Streamlit or charts.
"""

import fastf1
import pandas as pd
import os

# Create the cache folder if it doesn't exist yet - locally you made
# this by hand, but it's gitignored so it won't exist on a fresh
# deploy (like Streamlit Cloud). This makes the app work either way.
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')


def load_session(year, event, session_type):
    """
    Loads and returns a FastF1 session object.
    event can be a name ('Abu Dhabi') or round number.
    session_type: 'FP1','FP2','FP3','Q','S','R'
    """
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session


def get_driver_laps(session, driver_code):
    """
    Returns a clean DataFrame of one driver's laps:
    lap number, lap time (in seconds, not timedelta), compound, stint.
    driver_code: 3-letter code, e.g. 'VER', 'HAM'
    """
    laps = session.laps.pick_drivers(driver_code).copy()

    # Convert LapTime from timedelta to seconds (float) - much easier
    # to plot and compare than raw timedelta objects
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # Drop laps with no recorded time (in/out laps, red flags etc.)
    laps = laps.dropna(subset=['LapTimeSeconds'])

    return laps[['LapNumber', 'LapTimeSeconds', 'Compound', 'Stint', 'Driver']]


def get_all_drivers_laps(session):
    """
    Returns cleaned lap data for every driver in the session at once.
    Useful for comparison charts across drivers.
    """
    laps = session.laps.copy()
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
    laps = laps.dropna(subset=['LapTimeSeconds'])
    return laps[['Driver', 'LapNumber', 'LapTimeSeconds', 'Compound', 'Stint']]


def get_pit_stops(session, driver_code):
    """
    Returns pit stop laps for a driver: the lap number where they pitted
    and how long the stop took (PitInTime -> PitOutTime gap).
    """
    laps = session.laps.pick_drivers(driver_code).copy()

    # A pit stop lap has a recorded PitInTime or PitOutTime
    pit_laps = laps[laps['PitInTime'].notna(
    ) | laps['PitOutTime'].notna()].copy()

    return pit_laps[['LapNumber', 'PitInTime', 'PitOutTime', 'Compound', 'Stint']]


def get_tyre_stints(session, driver_code):
    """
    Returns a summary of each stint: which compound, start lap, end lap,
    and how many laps it lasted. Good for a stint timeline chart.
    """
    laps = session.laps.pick_drivers(driver_code).copy()
    laps = laps.dropna(subset=['LapNumber'])

    stints = (
        laps.groupby('Stint')
        .agg(
            Compound=('Compound', 'first'),
            StartLap=('LapNumber', 'min'),
            EndLap=('LapNumber', 'max'),
        )
        .reset_index()
    )
    stints['StintLength'] = stints['EndLap'] - stints['StartLap'] + 1

    return stints


if __name__ == '__main__':
    # Quick manual test - run this file directly with:
    #   python data.py
    # to confirm each function works before building charts on top of them.

    session = load_session(2024, 'Abu Dhabi', 'R')

    print("\n--- get_driver_laps('VER') ---")
    print(get_driver_laps(session, 'VER').head())

    print("\n--- get_pit_stops('VER') ---")
    print(get_pit_stops(session, 'VER'))

    print("\n--- get_tyre_stints('VER') ---")
    print(get_tyre_stints(session, 'VER'))
