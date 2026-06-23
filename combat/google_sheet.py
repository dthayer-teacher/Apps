import requests
import streamlit as st

APPS_SCRIPT_URL = st.secrets["google"]["apps_script_url"]


class SheetWrapper:
    def append_row(self, row):
        payload = {
            "practice_date": row[0],
            "timestamp": row[1],
            "player": row[2],
            "shot_type": row[3],
            "spot": row[4],
            "result": row[5],
            "x": row[6],
            "y": row[7],
        }

        response = requests.post(APPS_SCRIPT_URL, json=payload)

        if response.status_code != 200:
            raise Exception(
                f"Apps Script POST failed: {response.status_code} - "
                f"{response.text[:500]}"
            )

    def get_all_records(self):
        response = requests.get(APPS_SCRIPT_URL)

        if response.status_code != 200:
            raise Exception(
                f"Apps Script GET failed: {response.status_code} - "
                f"{response.text[:500]}"
            )

        values = response.json()

        if len(values) <= 1:
            return []

        headers = values[0]
        rows = values[1:]

        return [dict(zip(headers, row)) for row in rows]


def get_sheet():
    return SheetWrapper()