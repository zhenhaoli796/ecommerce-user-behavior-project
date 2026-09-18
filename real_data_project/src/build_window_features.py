from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
SAMPLE_DATA_PATH = PROJECT_DIR / "data" / "sample" / "user_behavior_100k.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

FEATURE_START_DATE = "2017-11-25"
FEATURE_END_DATE = "2017-12-02"
LABEL_DATE = "2017-12-03"

def load_data():
    df = pd.read_csv(SAMPLE_DATA_PATH)

    feature_df = df[
        (df["date"] >= FEATURE_START_DATE)
        & (df["date"] <= FEATURE_END_DATE)
    ]

    label_df = df[df["date"] == LABEL_DATE]

    return feature_df, label_df


def build_labels(label_df):
    labels = (
        label_df[label_df["behavior_type"] == "buy"]
        [["user_id", "item_id"]]
        .drop_duplicates()
        .copy()
    )

    labels["label"] = 1

    return labels

def build_candidates(feature_df):
    interacted_pairs = (
        feature_df[["user_id", "item_id"]]
        .drop_duplicates()
        .copy()
    )

    bought_pairs = (
        feature_df[feature_df["behavior_type"] == "buy"]
        [["user_id", "item_id"]]
        .drop_duplicates()
        .copy()
    )

    candidates = interacted_pairs.merge(
        bought_pairs,
        on=["user_id", "item_id"],
        how="left",
        indicator=True
    )

    candidates = candidates[candidates["_merge"] == "left_only"]

    candidates = candidates[["user_id", "item_id"]].copy()

    return candidates

def attach_labels(candidates, labels):
    samples = candidates.merge(
        labels,
        on=["user_id", "item_id"],
        how="left"
    )

    samples["label"] = samples["label"].fillna(0).astype(int)

    return samples


def main():
    feature_df, label_df = load_data()

    print("===== feature window shape =====")
    print(feature_df.shape)

    print("\n===== label window shape =====")
    print(label_df.shape)

    labels = build_labels(label_df)

    print("\n===== positive labels shape =====")
    print(labels.shape)

    print("\n===== labels preview =====")
    print(labels.head())

    candidates = build_candidates(feature_df)

    print("\n===== candidates shape =====")
    print(candidates.shape)

    print("\n===== candidates preview =====")
    print(candidates.head())

    samples = attach_labels(candidates, labels)

    print("\n===== samples shape =====")
    print(samples.shape)

    print("\n===== label distribution =====")
    print(samples["label"].value_counts())
if __name__ == "__main__":
    main()





