from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "medicine_data.csv"
)

df = pd.read_csv(DATA_PATH)

df["brand_name_search"] = (
    df["brand_name"]
    .fillna("")
    .str.lower()
    .str.strip()
)