from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_DIR / "data" / "sample" / "user_behavior_100k.csv"
OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "purchase_features_3d.csv"

MODELING_START = pd.Timestamp("2017-11-25 00:00:00")
MODELING_END = pd.Timestamp("2017-12-03 23:59:59")
LABEL_WINDOW = pd.Timedelta(days=3)
BEHAVIORS = ["pv", "fav", "cart", "buy"]


def load_data():
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.loc[
        df["datetime"].between(MODELING_START, MODELING_END)
    ].copy()


def build_candidates(df):
    interest = df.loc[
        df["behavior_type"].isin(["pv", "fav", "cart"])
    ].copy()

    first_interest = (
        interest.sort_values("datetime", kind="stable")
        .drop_duplicates(["user_id", "item_id"], keep="first")
        .rename(columns={
            "datetime": "first_interest_time",
            "behavior_type": "first_behavior_type",
        })
        [[
            "user_id", "item_id", "category_id",
            "first_interest_time", "first_behavior_type",
        ]]
        .reset_index(drop=True)
    )

    print("\n===== first interest shape =====")
    print(first_interest.shape)

    # Only keep samples with a complete three-day observation window.
    cutoff = MODELING_END - LABEL_WINDOW
    candidates = first_interest.loc[
        first_interest["first_interest_time"] <= cutoff
    ].copy()
    candidates.insert(0, "candidate_id", candidates.index)
    return candidates.reset_index(drop=True)


def attach_labels(candidates, df):
    buys = df.loc[
        df["behavior_type"].eq("buy"),
        ["user_id", "item_id", "datetime"],
    ].rename(columns={"datetime": "buy_time"})

    matched = candidates.merge(
        buys, on=["user_id", "item_id"], how="left"
    )
    within_window = (
        (matched["buy_time"] > matched["first_interest_time"])
        & (
            matched["buy_time"]
            <= matched["first_interest_time"] + LABEL_WINDOW
        )
    )
    positive_ids = matched.loc[within_window, "candidate_id"].unique()

    samples = candidates.copy()
    samples["label"] = samples["candidate_id"].isin(positive_ids).astype(int)
    return samples


def build_basic_features(samples):
    features = samples.copy()
    features["hour"] = features["first_interest_time"].dt.hour
    features["weekday"] = features["first_interest_time"].dt.dayofweek
    features["is_weekend"] = (features["weekday"] >= 5).astype(int)

    features["first_behavior_type"] = pd.Categorical(
        features["first_behavior_type"],
        categories=["cart", "fav", "pv"],
    )
    return pd.get_dummies(
        features, columns=["first_behavior_type"], dtype=int
    )


def add_history_features(features, df, entity):
    entity_id = f"{entity}_id"
    history = features[
        ["candidate_id", entity_id, "first_interest_time"]
    ].merge(
        df[[entity_id, "behavior_type", "datetime"]],
        on=entity_id,
        how="left",
    )

    # Exclude the current event and every event after prediction time.
    history = history.loc[
        history["datetime"] < history["first_interest_time"]
    ]

    counts = (
        history.groupby(["candidate_id", "behavior_type"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=BEHAVIORS, fill_value=0)
    )
    count_columns = [
        f"{entity}_history_{behavior}_count"
        for behavior in BEHAVIORS
    ]
    counts.columns = count_columns

    features = features.merge(
        counts, left_on="candidate_id", right_index=True, how="left"
    )
    features[count_columns] = features[count_columns].fillna(0).astype(int)
    features[f"{entity}_history_behavior_count"] = (
        features[count_columns].sum(axis=1)
    )

    if entity == "user":
        features["user_has_bought_before"] = (
            features["user_history_buy_count"] > 0
        ).astype(int)

    return features


def main():
    df = load_data()
    candidates = build_candidates(df)
    samples = attach_labels(candidates, df)

    print("\n===== label distribution =====")
    print(samples["label"].value_counts())
    print("\n===== 3-day purchase rate =====")
    print(samples["label"].mean())

    features = build_basic_features(samples)
    for entity in ["user", "item", "category"]:
        features = add_history_features(features, df, entity)
        print(f"\n===== {entity} history features completed =====")

    assert features["candidate_id"].is_unique
    assert not features.isna().any().any()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT_PATH, index=False)

    print("\n===== model dataset shape =====")
    print(features.shape)
    print("\n===== missing values =====")
    print(features.isna().sum().sum())
    print("\n===== saved path =====")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()