from pathlib import Path

import joblib
import numpy as np
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "medicine_price_model.joblib"
)

model = joblib.load(MODEL_PATH)


def extract_strength(strength):
    if pd.isna(strength):
        return np.nan

    match = str(strength).strip()

    value = pd.Series([match]).str.extract(
        r"(\d+(?:\.\d+)?)"
    )[0].iloc[0]

    if pd.isna(value):
        return np.nan

    return float(value)


def predict_price(
    dosage_form,
    pack_size,
    pack_unit,
    primary_ingredient,
    primary_strength,
    therapeutic_class,
    num_active_ingredients
):
    strength_value = extract_strength(primary_strength)

    log_pack_size = (
        np.log1p(pack_size)
        if not pd.isna(pack_size)
        else np.nan
    )

    input_data = pd.DataFrame([{
        "dosage_form": dosage_form,
        "pack_size": pack_size,
        "log_pack_size": log_pack_size,
        "pack_unit": pack_unit,
        "primary_ingredient": primary_ingredient,
        "primary_strength": primary_strength,
        "strength_value": strength_value,
        "therapeutic_class": therapeutic_class,
        "num_active_ingredients": num_active_ingredients
    }])

    prediction = model.predict(input_data)[0]

    return max(0, float(prediction))