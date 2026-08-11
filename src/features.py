import numpy as np

features = [
    "dosage_form",
    "pack_size",
    "log_pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "strength_value",
    "therapeutic_class",
    "num_active_ingredients"
]

def add_features(df):
    df = df.copy()

    df["strength_value"] = (
        df["primary_strength"]
        .astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)")[0]
        .astype(float)
    )

    df["log_pack_size"] = np.log1p(df["pack_size"])

    return df


def get_model_features(df):
    return df[features].copy()