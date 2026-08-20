# F1 Race Performance & Strategy Analysis

An interactive dashboard analyzing real Formula 1 race data — lap times, tyre strategy,
and pit stop timing — built for the 2024 Abu Dhabi Grand Prix (season finale).

**[Live demo →](#)** *(add your deployed Streamlit link here)*

## What it does

- **Lap Time Evolution** — see any driver's pace unfold lap by lap across the race
- **Lap Time Comparison** — overlay multiple drivers to spot who was faster and where
- **Tyre Stint Timeline** — visualize tyre strategy (compound choice and stint length)
- **Pit Stop Laps** — compare which lap each driver pitted on, revealing undercut/overcut
  strategy battles

Pick any driver from the sidebar and the charts update live.

## Stack

- [FastF1](https://github.com/theOehrly/Fast-F1) — official F1 timing data
- pandas — data cleaning and wrangling
- Plotly — interactive charts
- Streamlit — web app framework

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

- `data.py` — functions to load session data and extract laps, pit stops, and tyre stints
- `charts.py` — Plotly chart builders
- `app.py` — Streamlit app tying it all together

## Author

Built by [Ayush](https://strongayush.github.io) · [GitHub](https://github.com/strongayush)