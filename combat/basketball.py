import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Basketball Shooting Chart")

spots = [
    "Left Corner 3", "Left Wing", "Top Key",
    "Right Wing", "Right Corner 3",
    "Left Block", "Paint", "Right Block", "Free Throw"
]

default_players = ["Player 1", "Player 2", "Player 3"]

if "players" not in st.session_state:
    st.session_state.players = default_players

if "shots" not in st.session_state:
    st.session_state.shots = []

st.header("Add Player")

new_player = st.text_input("Player name")

if st.button("Add Player"):
    if new_player and new_player not in st.session_state.players:
        st.session_state.players.append(new_player)
        st.success(f"{new_player} added.")
    elif new_player in st.session_state.players:
        st.warning("That player already exists.")

st.divider()

st.header("Record Shot")

player = st.selectbox("Player", st.session_state.players)
spot = st.selectbox("Shot Location", spots)
result = st.radio("Result", ["Made", "Missed"], horizontal=True)

if st.button("Submit Shot"):
    st.session_state.shots.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Player": player,
        "Spot": spot,
        "Result": result
    })

    st.success(f"{player}: {result} from {spot} recorded.")

st.divider()

st.header("Stats")

if len(st.session_state.shots) == 0:
    st.info("No shots recorded yet.")
else:
    df = pd.DataFrame(st.session_state.shots)

    selected_player = st.selectbox(
        "View stats for",
        ["All Players"] + st.session_state.players
    )

    if selected_player != "All Players":
        df_view = df[df["Player"] == selected_player]
    else:
        df_view = df

    total_attempts = len(df_view)
    total_made = len(df_view[df_view["Result"] == "Made"])
    fg_pct = 0 if total_attempts == 0 else round(total_made / total_attempts * 100, 1)

    st.metric("Made / Attempts", f"{total_made}/{total_attempts}")
    st.metric("FG%", f"{fg_pct}%")

    st.subheader("By Location")

    stats = (
        df_view
        .groupby("Spot")
        .agg(
            Attempts=("Result", "count"),
            Made=("Result", lambda x: (x == "Made").sum())
        )
        .reset_index()
    )

    stats["FG%"] = round(stats["Made"] / stats["Attempts"] * 100, 1)

    st.dataframe(stats, use_container_width=True)

    st.subheader("Shot Log")
    st.dataframe(df_view, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "basketball_shots.csv",
        "text/csv"
    )

if st.button("Reset All Shots"):
    st.session_state.shots = []
    st.rerun()