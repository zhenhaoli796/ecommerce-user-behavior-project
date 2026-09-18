from pathlib import Path
import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
SAMPLE_DATA_PATH = PROJECT_DIR / "data" / "sample" / "user_behavior_100k.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"
def load_data():
    df = pd.read_csv(SAMPLE_DATA_PATH)

    df = df[
        (df["date"] >= "2017-11-25")
        & (df["date"] <= "2017-12-03")
    ]
    # print(df.info())
    return df

def analyze_behavior_distribution(df):
    behavior_dist = (
        df["behavior_type"]
        .value_counts()
        .reset_index()
    )

    behavior_dist.columns = ["behavior_type", "behavior_count"]
    behavior_dist["behavior_ratio"] = (
        behavior_dist["behavior_count"] / behavior_dist["behavior_count"].sum()
    ).round(4)

    print("===== 行为分布 =====")
    print(behavior_dist)
    return behavior_dist

def analyze_daily_metrics(df):
    daily_behavior = (
        df.groupby("date")
        .size()
        .reset_index(name="behavior_count")
    )

    # print(daily_behavior)
    daily_dau = (
        df.groupby("date")["user_id"]
        .nunique()
        .reset_index(name="dau")
    )

    buy_df = df[df["behavior_type"] == "buy"]

    daily_buy_users = (
        buy_df.groupby("date")["user_id"]
        .nunique()
        .reset_index(name="buy_users")
    )

    daily_buy_count = (
        buy_df.groupby("date")
        .size()
        .reset_index(name="buy_count")
    )
#     print(daily_dau)

    daily_metrics = (
        daily_behavior
        .merge(daily_dau, on="date", how="left")
        .merge(daily_buy_users, on="date", how="left")
        .merge(daily_buy_count, on="date", how="left")
    )

    daily_metrics[["buy_users", "buy_count"]] = daily_metrics[
        ["buy_users", "buy_count"]
    ].fillna(0).astype(int)

    daily_metrics["buy_user_rate"] = (
            daily_metrics["buy_users"] / daily_metrics["dau"]
    ).round(4)

    print("\n===== 每日核心指标 =====")
    print(daily_metrics)
    return daily_metrics

def main():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    behavior_dist = analyze_behavior_distribution(df)
    daily_metrics = analyze_daily_metrics(df)

    behavior_dist.to_csv(
        PROCESSED_DATA_DIR / "behavior_distribution.csv",
        index=False,
        encoding="utf-8-sig"
    )

    daily_metrics.to_csv(
        PROCESSED_DATA_DIR / "daily_metrics.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== pandas eda results saved =====")
if __name__ == "__main__":
    main()

















