from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    user_item_behavior = (
        df.groupby(["user_id", "item_id", "behavior_type"])
        .size()
        .reset_index(name="count")
    )

    feature_df = user_item_behavior.pivot_table(
        index=["user_id", "item_id"],
        columns="behavior_type",
        values="count",
        fill_value=0
    ).reset_index()

    feature_df.columns.name = None

    for col in ["view", "cart", "fav", "buy"]:
        if col not in feature_df.columns:
            feature_df[col] = 0

    feature_df["label"] = (feature_df["buy"] > 0).astype(int)

    feature_df = feature_df[
        ["user_id", "item_id", "view", "cart", "fav", "buy", "label"]
    ]

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / "user_item_features.csv"
    feature_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("===== 用户-商品特征表 =====")
    print(feature_df.head(10))

    print("\n特征表保存成功：")
    print(output_path)

    print("\n===== label 分布 =====")
    print(feature_df["label"].value_counts())


if __name__ == "__main__":
    main()