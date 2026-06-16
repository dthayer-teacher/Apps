import streamlit as st

st.title("Basketball Shooting Chart")

spots = [
    "Left Corner 3", "Left Wing", "Top Key",
    "Right Wing", "Right Corner 3",
    "Left Block", "Paint", "Right Block", "Free Throw"
]

if "shots" not in st.session_state:
    st.session_state.shots = {spot: {"made": 0, "attempts": 0} for spot in spots}

for spot in spots:
    made = st.session_state.shots[spot]["made"]
    attempts = st.session_state.shots[spot]["attempts"]
    pct = 0 if attempts == 0 else round(made / attempts * 100, 1)

    st.subheader(f"{spot}: {made}/{attempts} — {pct}%")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Made - {spot}"):
            st.session_state.shots[spot]["made"] += 1
            st.session_state.shots[spot]["attempts"] += 1
            st.rerun()

    with col2:
        if st.button(f"Missed - {spot}"):
            st.session_state.shots[spot]["attempts"] += 1
            st.rerun()

if st.button("Reset"):
    st.session_state.shots = {spot: {"made": 0, "attempts": 0} for spot in spots}
    st.rerun()