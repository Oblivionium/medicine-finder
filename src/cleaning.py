import pandas as pd
import ast

def clean_composition(text):
    if pd.isna(text):
        return ""

    try:
        ingredients = ast.literal_eval(text)

        result = []

        for ing in ingredients:
            name = str(ing.get("name") or "").strip().lower()
            strength = str(ing.get("strength") or "unknown").strip().lower()

            if not name:
                continue

            result.append(f"{name}_{strength}")

        result.sort()

        return " ".join(result)

    except (ValueError, SyntaxError, TypeError):
        return ""

def clean_dataframe(df):
    df = df.copy()

    df["cleaned_composition"] = (
        df["active_ingredients"].apply(clean_composition)
    )

    df = df[df["price_inr"] > 0]

    return df