from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


BEHAVIOR_WEIGHT = {
    "view": 1,
    "fav": 2,
    "cart": 3,
    "buy": 5
}


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    df["behavior_weight"] = df["behavior_type"].map(BEHAVIOR_WEIGHT)

    item_score = (
        df.groupby("item_id")["behavior_weight"]
        .sum()
        .reset_index(name="popularity_score")
    )

    item_score = item_score.sort_values(
        by="popularity_score",
        ascending=False
    )

    top_items = item_score.head(10)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / "popular_recommendations.csv"
    top_items.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("===== 热门商品推荐 Top 10 =====")
    print(top_items)

    print("\n热门推荐结果已保存：")
    print(output_path)


if __name__ == "__main__":
    main()