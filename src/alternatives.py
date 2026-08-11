from pathlib import Path

import pandas as pd

from src.cleaning import clean_composition


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "medicine_data.csv"
)


df = pd.read_csv(DATA_PATH)

df["cleaned_composition"] = (
    df["active_ingredients"].apply(clean_composition)
)


def find_alternatives(medicine_name):
    medicine = df[
        df["brand_name"].str.lower() == medicine_name.lower()
    ]

    if medicine.empty:
        return None

    composition = medicine.iloc[0]["cleaned_composition"]

    alternatives = df[
        df["cleaned_composition"] == composition
    ]

    return (
        alternatives
        .sort_values(by="price_inr")
        [
            [
                "brand_name",
                "manufacturer",
                "price_inr"
            ]
        ]
    )