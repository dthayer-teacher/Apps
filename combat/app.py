import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
from google_sheet import get_sheet

st.title("Basketball Shooting Chart")

shot_types = ["2PT", "3PT", "FT"]

if "players" not in st.session_state:
    st.session_state.players = []

if "shots_df" not in st.session_state:
    st.session_state.shots_df = pd.DataFrame()

if "shot_x" not in st.session_state:
    st.session_state.shot_x = None

if "shot_y" not in st.session_state:
    st.session_state.shot_y = None


def refresh_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    st.session_state.shots_df = pd.DataFrame(data)


def load_court_image():
    base_dir = Path(__file__).parent
    return Image.open(base_dir / "court.png").convert("RGB")


def draw_selected_shot(court_img, result, display_width=450):
    if st.session_state.shot_x is None or st.session_state.shot_y is None:
        return court_img

    court_img = court_img.convert("RGBA")
    overlay = Image.new("RGBA", court_img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    original_width, original_height = court_img.size
    scale = original_width / display_width

    x = int(st.session_state.shot_x * scale)
    y = int(st.session_state.shot_y * scale)

    dot_color = (0, 180, 0, 170) if result == "Made" else (220, 0, 0, 170)
    radius = int(6 * scale)

    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        fill=dot_color,
        outline=(0, 0, 0, 220),
        width=max(1, int(2 * scale))
    )

    return Image.alpha_composite(court_img, overlay).convert("RGB")


def draw_shots_on_court(court_img, df, display_width=450):
    court_img = court_img.convert("RGBA")
    overlay = Image.new("RGBA", court_img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    original_width, original_height = court_img.size
    scale = original_width / display_width

    for _, row in df.iterrows():
        try:
            x = int(float(row["X"]) * scale)
            y = int(float(row["Y"]) * scale)
        except:
            continue

        dot_color = (0, 180, 0, 145) if row["Result"] == "Made" else (220, 0, 0, 145)
        radius = int(5 * scale)

        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=dot_color,
            outline=(0, 0, 0, 180),
            width=max(1, int(1.5 * scale))
        )

    # Legend
    legend_x = int(15 * scale)
    legend_y = int(15 * scale)
    r = int(5 * scale)

    draw.rectangle(
        (legend_x - 8, legend_y - 8, legend_x + int(105 * scale), legend_y + int(45 * scale)),
        fill=(255, 255, 255, 190),
        outline=(0, 0, 0, 160)
    )

    draw.ellipse(
        (legend_x, legend_y, legend_x + 2*r, legend_y + 2*r),
        fill=(0, 180, 0, 145),
        outline=(0, 0, 0, 180)
    )
    draw.text((legend_x + int(18 * scale), legend_y - 2), "Made", fill=(0, 0, 0, 255))

    draw.ellipse(
        (legend_x, legend_y + int(22 * scale), legend_x + 2*r, legend_y + int(22 * scale) + 2*r),
        fill=(220, 0, 0, 145),
        outline=(0, 0, 0, 180)
    )
    draw.text((legend_x + int(18 * scale), legend_y + int(20 * scale)), "Missed", fill=(0, 0, 0, 255))

    return Image.alpha_composite(court_img, overlay).convert("RGB")


# ---------- REFRESH ----------
if st.button("Refresh Data"):
    refresh_data()
    st.success("Data refreshed.")


# ---------- SIDEBAR ----------
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


# ---------- TAB 1 ----------
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

        DISPLAY_WIDTH = 450

        court_img = load_court_image()

        if st.session_state.shot_x is not None and st.session_state.shot_y is not None:
            court_img = draw_selected_shot(
                court_img,
                result,
                display_width=DISPLAY_WIDTH
            )

        value = streamlit_image_coordinates(
            court_img,
            width=DISPLAY_WIDTH,
            key="court_click"
        )

        if value is not None:
            old_x = st.session_state.shot_x
            old_y = st.session_state.shot_y

            new_x = value["x"]
            new_y = value["y"]

            if old_x != new_x or old_y != new_y:
                st.session_state.shot_x = new_x
                st.session_state.shot_y = new_y
                st.rerun()

        if st.session_state.shot_x is not None:
            if st.session_state.shot_x is not None:
                st.caption("Shot location selected.")
            else:
                st.info("Click the court to choose a shot location.")
            # st.success(
            #     f"Selected shot: X={st.session_state.shot_x}, "
            #     f"Y={st.session_state.shot_y}, Result={result}"
            # )
        else:
            st.info("Click the court to choose a shot location.")

        if st.button("Submit Shot"):
            st.write("Submit clicked")

            if st.session_state.shot_x is None or st.session_state.shot_y is None:
                st.warning("No shot location stored.")
            else:
                try:
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

                    # st.write("Saving row:", row)

                    sheet = get_sheet()
                    sheet.append_row(row)

                    st.success("Shot saved!")
                    # if st.button("Clear Selected Shot"):
                    #     st.session_state.shot_x = None
                    #     st.session_state.shot_y = None
                        # st.rerun()

                    # st.session_state.shot_x = None
                    # st.session_state.shot_y = None

                except Exception as e:
                    st.error("Submit Shot failed.")
                    st.exception(e)

# ---------- TAB 2 ----------
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

        st.subheader("Shot Chart")

        court_img = load_court_image()
        court_with_shots = draw_shots_on_court(
            court_img,
            df,
            display_width=450
        )

        st.image(court_with_shots, width=450)
        st.caption("Green = Made, Red = Missed")

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


# ---------- TAB 3 ----------
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

        st.subheader("Team Shot Chart")

        court_img = load_court_image()
        court_with_shots = draw_shots_on_court(
            court_img,
            df,
            display_width=450
        )

        st.image(court_with_shots, width=450)
        st.caption("Green = Made, Red = Missed")

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