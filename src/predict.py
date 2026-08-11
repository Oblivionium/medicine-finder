from pathlib import Path

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "medicine_price_model.joblib"
)

model = joblib.load(MODEL_PATH)


def predict_price(
    dosage_form,
    pack_size,
    pack_unit,
    primary_ingredient,
    primary_strength,
    therapeutic_class,
    num_active_ingredients
):
    input_data = pd.DataFrame([{
        "dosage_form": dosage_form,
        "pack_size": pack_size,
        "pack_unit": pack_unit,
        "primary_ingredient": primary_ingredient,
        "primary_strength": primary_strength,
        "therapeutic_class": therapeutic_class,
        "num_active_ingredients": num_active_ingredients
    }])

    input_data["strength_value"] = (
        input_data["primary_strength"]
        .astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)")[0]
        .astype(float)
    )

    input_data["log_pack_size"] = np.log1p(
        input_data["pack_size"]
    )

    prediction = model.predict(input_data)[0]

    return max(0, float(prediction))