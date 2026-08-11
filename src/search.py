import re

from rapidfuzz import fuzz, process

from src.data import df


def normalize(text):
    return (
        str(text)
        .lower()
        .strip()
    )


def extract_strength(text):
    match = re.search(
        r"\d+(?:\.\d+)?",
        normalize(text)
    )

    if match:
        return float(match.group())

    return None


def get_base_name(text):
    text = normalize(text)

    # Remove strength
    text = re.sub(
        r"\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|%|iu)\b",
        "",
        text
    )

    # Remove common dosage forms
    text = re.sub(
        r"\b(tablet|tablets|capsule|capsules|"
        r"injection|syrup|solution|cream|gel|"
        r"ointment|drops|spray|inhaler|"
        r"suspension|powder)\b",
        "",
        text
    )

    return " ".join(text.split())


df["brand_name_search"] = (
    df["brand_name"]
    .fillna("")
    .map(normalize)
)

df["base_name"] = (
    df["brand_name"]
    .map(get_base_name)
)


BASE_NAMES = (
    df["base_name"]
    .drop_duplicates()
    .tolist()
)


def search_medicines(query, limit=8):
    query = normalize(query)

    if not query:
        return []

    query_strength = extract_strength(query)
    query_base = get_base_name(query)

    # Exact base-name matches
    matches = df[
        df["base_name"] == query_base
    ].copy()

    # If no exact base-name match, fuzzy-match
    if matches.empty:

        fuzzy_matches = process.extract(
            query_base,
            BASE_NAMES,
            scorer=fuzz.ratio,
            limit=5
        )

        fuzzy_matches = [
            (name, score)
            for name, score, _ in fuzzy_matches
            if score >= 80
        ]

        if not fuzzy_matches:
            return []

        best_name, best_score = fuzzy_matches[0]

        # Don't return weak fuzzy matches
        if best_score < 80:
            return []

        matches = df[
            df["base_name"] == best_name
        ].copy()

    # Rank requested strength first
    if query_strength is not None:

        matches["strength_value"] = (
            matches["primary_strength"]
            .fillna("")
            .map(extract_strength)
        )

        matches["strength_match"] = (
            matches["strength_value"]
            == query_strength
        )

        matches = matches.sort_values(
            by="strength_match",
            ascending=False
        )

    matches = matches.drop_duplicates(
        subset=[
            "brand_name",
            "manufacturer",
            "dosage_form",
            "primary_strength"
        ]
    )

    return [
        {
            "brand_name": medicine["brand_name"],
            "manufacturer": medicine["manufacturer"],
            "dosage_form": medicine["dosage_form"],
            "primary_strength": medicine["primary_strength"],
            "price_inr": medicine["price_inr"]
        }
        for _, medicine in matches.head(limit).iterrows()
    ]