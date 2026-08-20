"""
Checkpoint 1: Raw data pull
Goal: prove FastF1 can load a real session and give us lap data.
Nothing fancy yet - just load, cache, and print.
"""

import fastf1

# FastF1 caches downloaded data locally so you don't re-download
# every time you run the script. Create a folder called 'cache'
# in your project directory before running this.
fastf1.Cache.enable_cache('cache')

# Pick a session: (year, event name or round number, session type)
# session types: 'FP1', 'FP2', 'FP3', 'Q' (qualifying), 'R' (race), 'S' (sprint)
session = fastf1.get_session(2024, 'Abu Dhabi', 'R')

# This actually downloads/loads the timing data - can take 10-30s first time
session.load()

# session.laps is a pandas DataFrame - every lap, every driver
laps = session.laps

print(f"Session: {session.event['EventName']} - {session.name}")
print(f"Total laps recorded: {len(laps)}")
print(f"Drivers: {laps['Driver'].unique()}")
print("\nFirst 5 rows:")
print(laps[['Driver', 'LapNumber', 'LapTime', 'Compound', 'Stint']].head())
