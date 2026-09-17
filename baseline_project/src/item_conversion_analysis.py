from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    item_behavior = (
        df.groupby(["item_id", "behavior_type"])
        .size()
        .reset_index(name="count")
    )

    item_behavior_pivot = item_behavior.pivot_table(
        index="item_id",
        columns="behavior_type",
        values="count",
        fill_value=0
    ).reset_index()
    item_behavior_pivot.columns.name = None

    if "view" not in item_behavior_pivot.columns:
        item_behavior_pivot["view"] = 0

    if "buy" not in item_behavior_pivot.columns:
        item_behavior_pivot["buy"] = 0

    item_behavior_pivot["conversion_rate"] = (
        item_behavior_pivot["buy"] / item_behavior_pivot["view"]
    )

    item_behavior_pivot = item_behavior_pivot[
        item_behavior_pivot["view"] > 10
    ]

    item_behavior_pivot = item_behavior_pivot.sort_values(
        by="conversion_rate",
        ascending=False
    )

    print("===== 商品转化率 Top 10 =====")
    print(item_behavior_pivot.head(10))


if __name__ == "__main__":
    main()