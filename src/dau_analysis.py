from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    df["event_time"] = pd.to_datetime(df["event_time"])
    df["date"] = df["event_time"].dt.date

    dau = df.groupby("date").agg({"user_id":'nunique'}).reset_index()
    dau.columns = ["date", "dau"]

    print("===== 每日活跃用户数 DAU =====")
    print(dau)


if __name__ == "__main__":
    main()