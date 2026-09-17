from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    category_behavior = (
        df.groupby(["category_id", "behavior_type"])
        .size()
        .reset_index(name="count")
    )

    category_behavior_pivot = category_behavior.pivot_table(
        index="category_id",
        columns="behavior_type",
        values="count",
        fill_value=0
    ).reset_index()

    category_behavior_pivot.columns.name = None

    if "view" not in category_behavior_pivot.columns:
        category_behavior_pivot["view"] = 0

    if "buy" not in category_behavior_pivot.columns:
        category_behavior_pivot["buy"] = 0

    category_behavior_pivot["conversion_rate"] = (
        category_behavior_pivot["buy"] / category_behavior_pivot["view"]
    )

    category_behavior_pivot = category_behavior_pivot[
        category_behavior_pivot["view"] >= 10
    ]

    category_behavior_pivot = category_behavior_pivot.sort_values(
        by="conversion_rate",
        ascending=False
    )

    print("===== 类目转化率 =====")
    print(category_behavior_pivot)


if __name__ == "__main__":
    main()