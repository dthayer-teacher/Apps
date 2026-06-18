import streamlit as st
import pandas as pd
from datetime import datetime
from google_sheet import get_sheet

st.title("Basketball Shooting Chart")

spots = [
    "Left Corner 3", "Left Wing", "Top Key",
    "Right Wing", "Right Corner 3",
    "Left Block", "Paint", "Right Block", "Free Throw"
]

if "players" not in st.session_state:
    st.session_state.players = []

# ---------- ROSTER ----------
st.sidebar.header("Roster Management")

new_player = st.sidebar.text_input("Add Player Name")

if st.sidebar.button("Add Player"):
    name = new_player.strip()

    if name == "":
        st.sidebar.warning("Enter a player name.")
    elif name in st.session_state.players:
        st.sidebar.warning("Player already exists.")
    else:
        st.session_state.players.append(name)
        st.sidebar.success(f"{name} added.")

st.sidebar.subheader("Current Roster")

if len(st.session_state.players) == 0:
    st.sidebar.info("No players added yet.")
else:
    for p in st.session_state.players:
        st.sidebar.write(f"- {p}")

# ---------- RECORD SHOT ----------
st.header("Record Shot")

practice_date = st.date_input("Practice Date")

if len(st.session_state.players) == 0:
    st.info("Add a player before recording shots.")
else:
    player = st.selectbox("Player", st.session_state.players)
    spot = st.selectbox("Shot Location", spots)
    result = st.radio("Result", ["Made", "Missed"], horizontal=True)

    if st.button("Submit Shot"):
        sheet = get_sheet()

        row = [
            str(practice_date),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            player,
            spot,
            result
        ]

        sheet.append_row(row)

        st.success(f"{player}: {result} from {spot} recorded.")

st.divider()

# ---------- RESULTS ----------
st.header("Shot Log and Stats")

if st.button("Load Results"):
    sheet = get_sheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No shots recorded yet.")
    else:
        st.subheader("Shot Log")
        st.dataframe(df, use_container_width=True)

        st.subheader("Team Leaderboard")

        stats = (
            df.groupby("Player")
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        stats["FG%"] = round(stats["Makes"] / stats["Attempts"] * 100, 1)
        stats = stats.sort_values("FG%", ascending=False)

        st.dataframe(stats, use_container_width=True)

        st.subheader("Location Stats")

        location_stats = (
            df.groupby(["Player", "Spot"])
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        location_stats["FG%"] = round(
            location_stats["Makes"] / location_stats["Attempts"] * 100,
            1
        )

        st.dataframe(location_stats, use_container_width=True)