from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
SAMPLE_DATA_PATH = PROJECT_DIR / "data" / "sample" / "user_behavior_100k.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def load_data():
    df = pd.read_csv(SAMPLE_DATA_PATH)

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = pd.to_datetime(df["date"])

    return df

def build_first_interest(df):
    interest_df = df[df["behavior_type"].isin(["pv", "fav", "cart"])].copy()

    interest_df = interest_df.sort_values(
        by=["user_id", "item_id", "datetime"]
    )

    first_interest = (
        interest_df
        .drop_duplicates(subset=["user_id", "item_id"], keep="first")
        [["user_id", "item_id", "datetime", "behavior_type"]]
        .copy()
    )

    first_interest = first_interest.rename(
        columns={
            "datetime": "first_interest_time",
            "behavior_type": "first_behavior_type",
        }
    )

    return first_interest


def attach_purchase_labels(first_interest, df):
    buy_df = (
        df[df["behavior_type"] == "buy"]
        [["user_id", "item_id", "datetime"]]
        .copy()
    )

    buy_df = buy_df.rename(columns={"datetime": "buy_time"})

    merged = first_interest.merge(
        buy_df,
        on=["user_id", "item_id"],
        how="left"
    )


    merged["delay_days"] = (
        merged["buy_time"] - merged["first_interest_time"]
    ).dt.total_seconds() / 86400

    label_df = (
        merged.groupby(["user_id", "item_id", "first_interest_time", "first_behavior_type"])
        .agg(
            buy_within_1d=("delay_days", lambda x: int(((x > 0) & (x <= 1)).any())),
            buy_within_3d=("delay_days", lambda x: int(((x > 0) & (x <= 3)).any())),
            buy_within_7d=("delay_days", lambda x: int(((x > 0) & (x <= 7)).any())),
        )
        .reset_index()
    )

    return label_df

def summarize_purchase_rate(label_df):
    window_rules = {
        "1d": ("buy_within_1d", pd.Timestamp("2017-12-02 23:59:59")),
        "3d": ("buy_within_3d", pd.Timestamp("2017-11-30 23:59:59")),
        "7d": ("buy_within_7d", pd.Timestamp("2017-11-26 23:59:59")),
    }

    rows = []

    for window, (label_col, max_interest_time) in window_rules.items():
        valid_df = label_df[label_df["first_interest_time"] <= max_interest_time]

        sample_count = len(valid_df)
        buy_count = valid_df[label_col].sum()
        buy_rate = round(buy_count / sample_count, 4)

        rows.append(
            {
                "window": window,
                "sample_count": sample_count,
                "buy_count": buy_count,
                "buy_rate": buy_rate,
            }
        )

    result = pd.DataFrame(rows)

    print("\n===== purchase rate by window =====")
    print(result)

    return result


def summarize_by_first_behavior(label_df):
    valid_df = label_df[
        label_df["first_interest_time"] <= pd.Timestamp("2017-11-30 23:59:59")
    ]

    result = (
        valid_df.groupby("first_behavior_type")
        .agg(
            sample_count=("item_id", "count"),
            buy_count=("buy_within_3d", "sum"),
        )
        .reset_index()
    )

    result["buy_rate"] = (
        result["buy_count"] / result["sample_count"]
    ).round(4)

    result = result.sort_values("buy_rate", ascending=False)

    print("\n===== 3d purchase rate by first behavior =====")
    print(result)

    return result

def summarize_purchase_delay(first_interest, df):
    buy_df = (
        df[df["behavior_type"] == "buy"]
        [["user_id", "item_id", "datetime"]]
        .copy()
    )

    buy_df = buy_df.rename(columns={"datetime": "buy_time"})

    merged = first_interest.merge(
        buy_df,
        on=["user_id", "item_id"],
        how="inner"
    )

    merged = merged[merged["buy_time"] > merged["first_interest_time"]].copy()

    first_purchase = (
        merged.sort_values("buy_time")
        .drop_duplicates(subset=["user_id", "item_id", "first_interest_time"], keep="first")
        .copy()
    )

    first_purchase["delay_days"] = (
        first_purchase["buy_time"] - first_purchase["first_interest_time"]
    ).dt.total_seconds() / 86400

    first_purchase["delay_bucket"] = pd.cut(
        first_purchase["delay_days"],
        bins=[0, 1, 3, 7, float("inf")],
        labels=["0-1d", "1-3d", "3-7d", "7d+"],
        right=True,
        include_lowest=True,
    )

    result = (
        first_purchase.groupby("delay_bucket", observed=True)
        .size()
        .reset_index(name="buy_count")
    )

    print("\n===== purchase delay distribution =====")
    print(result)

    return result

def main():
    df = load_data()
    first_interest = build_first_interest(df)
    label_df = attach_purchase_labels(first_interest, df)

    print("===== purchase labels preview =====")
    print(label_df.head())

    print("\n===== purchase labels shape =====")
    print(label_df.shape)

    print("\n===== label summary =====")
    print(label_df[["buy_within_1d", "buy_within_3d", "buy_within_7d"]].sum())

    purchase_rate = summarize_purchase_rate(label_df)

    behavior_rate = summarize_by_first_behavior(label_df)

    delay_dist = summarize_purchase_delay(first_interest, df)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    purchase_rate.to_csv(
        PROCESSED_DATA_DIR / "delayed_purchase_window_rates.csv",
        index=False,
        encoding="utf-8-sig"
    )

    behavior_rate.to_csv(
        PROCESSED_DATA_DIR / "delayed_purchase_behavior_rates.csv",
        index=False,
        encoding="utf-8-sig"
    )

    delay_dist.to_csv(
        PROCESSED_DATA_DIR / "purchase_delay_distribution.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== delayed purchase results saved =====")


if __name__ == "__main__":
    main()




















