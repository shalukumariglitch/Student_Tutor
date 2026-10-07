def recommend_tutors(df, subject, max_fee=None, min_rating=0):
    result = df.copy()

    if subject and subject != "Any":
        result = result[result["subject"].str.lower() == subject.lower()]

    if max_fee is not None:
        result = result[result["hourly_fee"] <= max_fee]

    result = result[result["rating"] >= min_rating]

    if result.empty:
        return result

    # Weighted recommendation score:
    # rating has highest importance; lower fee gets a small bonus.
    max_price = max(float(result["hourly_fee"].max()), 1)
    result = result.copy()
    result["recommendation_score"] = (
        result["rating"] * 0.85 +
        (1 - result["hourly_fee"] / max_price) * 0.15
    )

    return result.sort_values(
        ["recommendation_score", "rating"],
        ascending=False
    )
