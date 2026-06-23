import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from google_sheet import get_sheet
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

st.title("Basketball Shooting Chart")

spots = [
    "Left Corner 3", "Left Wing", "Top Key",
    "Right Wing", "Right Corner 3",
    "Left Block", "Paint", "Right Block", "Free Throw"
]

shot_types = ["2PT", "3PT", "FT"]

if "players" not in st.session_state:
    st.session_state.players = []

if "shots_df" not in st.session_state:
    st.session_state.shots_df = pd.DataFrame()


def refresh_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    st.session_state.shots_df = pd.DataFrame(data)


def draw_court():
    fig = go.Figure()

    # Outer half court
    fig.add_shape(type="rect", x0=0, y0=0, x1=50, y1=47)

    # Backboard
    fig.add_shape(type="line", x0=22, y0=4, x1=28, y1=4)

    # Hoop
    fig.add_shape(type="circle", x0=24.25, y0=4.75, x1=25.75, y1=6.25)

    # Paint
    fig.add_shape(type="rect", x0=17, y0=0, x1=33, y1=19)

    # Free throw circle
    fig.add_shape(type="circle", x0=19, y0=13, x1=31, y1=25)

    # Restricted area
    fig.add_shape(type="path", path="M 21 4.75 Q 25 9 29 4.75")

    # Three-point corners
    fig.add_shape(type="line", x0=3, y0=0, x1=3, y1=14)
    fig.add_shape(type="line", x0=47, y0=0, x1=47, y1=14)

    # Three-point arc
    fig.add_shape(type="path", path="M 3 14 Q 25 39 47 14")

    fig.update_xaxes(range=[0, 50], showgrid=False, visible=False)
    fig.update_yaxes(range=[0, 47], showgrid=False, visible=False)

    fig.update_layout(
        height=600,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )

    return fig


# ---------- LOAD DATA ----------
if st.button("Refresh Data"):
    refresh_data()
    st.success("Data refreshed.")


# ---------- ROSTER SIDEBAR ----------
st.sidebar.header("Roster Management")

if st.sidebar.button("Load Players from Sheet"):
    refresh_data()
    df_players = st.session_state.shots_df

    if not df_players.empty and "Player" in df_players.columns:
        players = sorted(df_players["Player"].dropna().unique())
        st.session_state.players = list(players)
        st.sidebar.success("Players loaded.")
    else:
        st.sidebar.warning("No players found.")

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


# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs([
    "🏀 Record Shots",
    "👤 Player Stats",
    "📊 Team Stats"
])


# ---------- TAB 1: RECORD SHOTS ----------
with tab1:
    st.header("Record Shot")

    practice_date = st.date_input("Practice Date")

    if len(st.session_state.players) == 0:
        st.info("Add or load players before recording shots.")
    else:
        player = st.selectbox("Player", st.session_state.players)
        shot_type = st.selectbox("Shot Type", shot_types)
        result = st.radio("Result", ["Made", "Missed"], horizontal=True)
        st.subheader("Click Shot Location")

        court_img = Image.open("court.png")

        col1, col2, col3 = st.columns([1, 4, 1])

        with col2:
            value = streamlit_image_coordinates(
                court_img,
                width=450,
                key="court_click"
            )

        if value is not None:
            x_coord = value["x"]
            y_coord = value["y"]

            st.session_state.shot_x = x_coord
            st.session_state.shot_y = y_coord

            st.success(f"Selected shot: X={x_coord}, Y={y_coord}")
        else:
            st.info("Click the court to choose a shot location.")

        # st.subheader("Shot Location on Court")

        # x_coord = st.slider("Left / Right Court Position", 0.0, 50.0, 25.0, 0.5)
        # y_coord = st.slider("Distance from Baseline", 0.0, 47.0, 10.0, 0.5)

        # fig = draw_court()

        # fig.add_trace(go.Scatter(
        #     x=[x_coord],
        #     y=[y_coord],
        #     mode="markers",
        #     marker=dict(size=14),
        #     name="Selected Shot"
        # ))

        # st.plotly_chart(fig, use_container_width=True)

        if st.button("Submit Shot"):
            sheet = get_sheet()

            row = [
                str(practice_date),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                player,
                shot_type,
                "Court Click",
                result,
                st.session_state.shot_x,
                st.session_state.shot_y
            ]

            sheet.append_row(row)
            refresh_data()

            st.success(
                f"{player}: {result} {shot_type} recorded at "
                f"X={x_coord}, Y={y_coord}."
            )


# ---------- TAB 2: PLAYER STATS ----------
with tab2:
    st.header("Player Statistics")

    df = st.session_state.shots_df.copy()

    if df.empty:
        st.info("Click Refresh Data to load stats.")
    else:
        st.subheader("Filters")

        player_options = ["All Players"] + sorted(df["Player"].dropna().unique())
        selected_player = st.selectbox(
            "Select Player",
            player_options,
            key="player_stats_filter"
        )

        date_options = ["All Dates"] + sorted(df["Practice Date"].dropna().unique())
        selected_date = st.selectbox(
            "Select Practice Date",
            date_options,
            key="player_date_filter"
        )

        if selected_player != "All Players":
            df = df[df["Player"] == selected_player]

        if selected_date != "All Dates":
            df = df[df["Practice Date"] == selected_date]

        total_attempts = len(df)
        total_makes = len(df[df["Result"] == "Made"])
        fg_pct = 0 if total_attempts == 0 else round(total_makes / total_attempts * 100, 1)

        three_df = df[df["Shot Type"] == "3PT"]
        three_attempts = len(three_df)
        three_makes = len(three_df[three_df["Result"] == "Made"])
        three_pct = 0 if three_attempts == 0 else round(three_makes / three_attempts * 100, 1)

        ft_df = df[df["Shot Type"] == "FT"]
        ft_attempts = len(ft_df)
        ft_makes = len(ft_df[ft_df["Result"] == "Made"])
        ft_pct = 0 if ft_attempts == 0 else round(ft_makes / ft_attempts * 100, 1)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Makes / Attempts", f"{total_makes}/{total_attempts}")
        col2.metric("FG%", f"{fg_pct}%")
        col3.metric("3PT%", f"{three_pct}%")
        col4.metric("FT%", f"{ft_pct}%")

        st.subheader("Shot Log")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Player Report",
            csv,
            "player_shooting_report.csv",
            "text/csv"
        )

        st.subheader("Shot Type Stats")

        type_stats = (
            df.groupby(["Player", "Shot Type"])
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        type_stats["Shot %"] = round(
            type_stats["Makes"] / type_stats["Attempts"] * 100,
            1
        )

        st.dataframe(type_stats, use_container_width=True)

        st.subheader("Location Stats")

        location_stats = (
            df.groupby(["Player", "Shot Type"])
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        location_stats["Shot %"] = round(
            location_stats["Makes"] / location_stats["Attempts"] * 100,
            1
        )

        st.dataframe(location_stats, use_container_width=True)


# ---------- TAB 3: TEAM STATS ----------
with tab3:
    st.header("Team Statistics")

    df = st.session_state.shots_df.copy()

    if df.empty:
        st.info("Click Refresh Data to load team stats.")
    else:
        st.subheader("Filters")

        date_options = ["All Dates"] + sorted(df["Practice Date"].dropna().unique())
        selected_team_date = st.selectbox(
            "Select Practice Date",
            date_options,
            key="team_date_filter"
        )

        if selected_team_date != "All Dates":
            df = df[df["Practice Date"] == selected_team_date]

        total_attempts = len(df)
        total_makes = len(df[df["Result"] == "Made"])
        fg_pct = 0 if total_attempts == 0 else round(total_makes / total_attempts * 100, 1)

        three_df = df[df["Shot Type"] == "3PT"]
        three_attempts = len(three_df)
        three_makes = len(three_df[three_df["Result"] == "Made"])
        three_pct = 0 if three_attempts == 0 else round(three_makes / three_attempts * 100, 1)

        ft_df = df[df["Shot Type"] == "FT"]
        ft_attempts = len(ft_df)
        ft_makes = len(ft_df[ft_df["Result"] == "Made"])
        ft_pct = 0 if ft_attempts == 0 else round(ft_makes / ft_attempts * 100, 1)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Team Makes / Attempts", f"{total_makes}/{total_attempts}")
        col2.metric("Team FG%", f"{fg_pct}%")
        col3.metric("Team 3PT%", f"{three_pct}%")
        col4.metric("Team FT%", f"{ft_pct}%")

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Team Report",
            csv,
            "team_shooting_report.csv",
            "text/csv"
        )

        st.subheader("Leaderboard")

        overall_stats = (
            df.groupby("Player")
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        overall_stats["FG%"] = round(
            overall_stats["Makes"] / overall_stats["Attempts"] * 100,
            1
        )

        overall_stats = overall_stats.sort_values("FG%", ascending=False)

        st.dataframe(overall_stats, use_container_width=True)

        st.subheader("FG% Chart")
        st.bar_chart(overall_stats.set_index("Player")["FG%"])

        st.subheader("Team Shot Type Stats")

        team_type_stats = (
            df.groupby("Shot Type")
            .agg(
                Attempts=("Result", "count"),
                Makes=("Result", lambda x: (x == "Made").sum())
            )
            .reset_index()
        )

        team_type_stats["Shot %"] = round(
            team_type_stats["Makes"] / team_type_stats["Attempts"] * 100,
            1
        )

        st.dataframe(team_type_stats, use_container_width=True)