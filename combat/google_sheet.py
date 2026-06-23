import requests
import pandas as pd
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
        response.raise_for_status()

    def get_all_records(self):
        response = requests.get(APPS_SCRIPT_URL)
        response.raise_for_status()

        values = response.json()

        if len(values) <= 1:
            return []

        headers = values[0]
        rows = values[1:]

        return [dict(zip(headers, row)) for row in rows]


def get_sheet():
    return SheetWrapper()