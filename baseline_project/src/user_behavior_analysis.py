from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    df["event_time"] = pd.to_datetime(df["event_time"])
    df["date"] = df["event_time"].dt.date

    user_behavior = (
        df.groupby(["user_id", "behavior_type"])
        .size()
        .reset_index(name="count")
    )

    user_behavior_pivot = user_behavior.pivot_table(
        index="user_id",
        columns="behavior_type",
        values="count",
        fill_value=0
    ).reset_index()

    user_behavior_pivot.columns.name = None

    for col in ["view", "cart", "fav", "buy"]:
        if col not in user_behavior_pivot.columns:
            user_behavior_pivot[col] = 0

    user_active_days = (
        df.groupby("user_id")["date"]
        .nunique()
        .reset_index(name="active_days")
    )

    user_summary = user_behavior_pivot.merge(
        user_active_days,
        on="user_id",
        how="left"
    )

    user_summary["total_behavior"] = (
        user_summary["view"]
        + user_summary["cart"]
        + user_summary["fav"]
        + user_summary["buy"]
    )

    user_summary["user_level"] = pd.cut(
        user_summary["total_behavior"],
        bins=[0, 5, 15, 9999],
        labels=["low_active", "middle_active", "high_active"]
    )

    user_summary = user_summary.sort_values(
        by="total_behavior",
        ascending=False
    )

    print("===== 用户行为汇总 Top 10 =====")
    print(user_summary.head(10))

    print("\n===== 用户活跃等级分布 =====")
    print(user_summary["user_level"].value_counts())


if __name__ == "__main__":
    main()