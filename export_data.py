"""
Run this LOCALLY (where FastF1 can actually reach the data) to export
the session's lap data to a CSV file. The deployed app then reads
this CSV directly instead of calling FastF1 live - so it works
regardless of any network restrictions the hosting platform has.

Run once:
    python export_data.py

Then commit the resulting CSV (in data_cache/) to your repo.
"""

import os
import fastf1
import pandas as pd

os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

YEAR = 2024
EVENT = 'Abu Dhabi'
SESSION_TYPE = 'R'

session = fastf1.get_session(YEAR, EVENT, SESSION_TYPE)
session.load()

laps = session.laps.copy()
laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
laps = laps.dropna(subset=['LapTimeSeconds'])

# Keep only what our charts actually need. IsPitIn/IsPitOut are
# precomputed as plain booleans here (instead of raw timestamps)
# so the CSV round-trips cleanly through pandas without any
# datetime-parsing headaches later.
export_df = laps[['Driver', 'LapNumber',
                  'LapTimeSeconds', 'Compound', 'Stint']].copy()
export_df['IsPitIn'] = laps['PitInTime'].notna()
export_df['IsPitOut'] = laps['PitOutTime'].notna()

os.makedirs('data_cache', exist_ok=True)
output_path = os.path.join('data_cache', 'abu_dhabi_2024_race_laps.csv')
export_df.to_csv(output_path, index=False)

print(
    f"Exported {len(export_df)} laps across {export_df['Driver'].nunique()} drivers to {output_path}")
print("Commit this CSV to your repo, then push - the app will read from it directly.")
