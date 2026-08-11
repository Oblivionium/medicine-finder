from pathlib import Path

import pandas as pd

from src.cleaning import clean_composition


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "medicine_data.csv"
)


from src.data import df

df["cleaned_composition"] = (
    df["active_ingredients"].apply(clean_composition)
)


def find_alternatives(medicine_name, limit=5):
    medicine = df[
        df["brand_name"].str.lower() == medicine_name.lower()
    ]

    if medicine.empty:
        return None

    selected_price = medicine.iloc[0]["price_inr"]
    composition = medicine.iloc[0]["cleaned_composition"]

    alternatives = df[
        (df["cleaned_composition"] == composition)
        & (df["price_inr"] < selected_price)
        & (
            df["brand_name"].str.lower()
            != medicine_name.lower()
        )
    ]

    alternatives = (
        alternatives
        .sort_values("price_inr")
        .drop_duplicates(
            subset=[
                "brand_name",
                "manufacturer",
                "dosage_form",
                "primary_strength"
            ]
        )
        .head(limit)
    )

    return alternatives[
        [
            "brand_name",
            "manufacturer",
            "price_inr"
        ]
    ]