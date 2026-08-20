"""
Data functions for the deployed app. Reads from a pre-exported CSV
(see export_data.py) instead of calling FastF1 live - this avoids
depending on the hosting platform being able to reach FastF1's data
servers at runtime.
"""

import os
import pandas as pd

CSV_PATH = os.path.join('data_cache', 'abu_dhabi_2024_race_laps.csv')


def load_laps_data():
    """Loads the pre-exported laps CSV as a DataFrame."""
    return pd.read_csv(CSV_PATH)


def get_driver_laps(laps_df, driver_code):
    """One driver's laps: lap number, lap time (seconds), compound, stint."""
    driver_laps = laps_df[laps_df['Driver'] == driver_code]
    return driver_laps[['LapNumber', 'LapTimeSeconds', 'Compound', 'Stint', 'Driver']]


def get_pit_stops(laps_df, driver_code):
    """Laps where the driver entered or exited the pits."""
    driver_laps = laps_df[laps_df['Driver'] == driver_code]
    pit_laps = driver_laps[driver_laps['IsPitIn'] | driver_laps['IsPitOut']]
    return pit_laps[['LapNumber', 'IsPitIn', 'IsPitOut', 'Compound', 'Stint']]


def get_tyre_stints(laps_df, driver_code):
    """Summary of each tyre stint: compound, start lap, end lap, length."""
    driver_laps = laps_df[laps_df['Driver'] == driver_code]

    stints = (
        driver_laps.groupby('Stint')
        .agg(
            Compound=('Compound', 'first'),
            StartLap=('LapNumber', 'min'),
            EndLap=('LapNumber', 'max'),
        )
        .reset_index()
    )
    stints['StintLength'] = stints['EndLap'] - stints['StartLap'] + 1

    return stints
