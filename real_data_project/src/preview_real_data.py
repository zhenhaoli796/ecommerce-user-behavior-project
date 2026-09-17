from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "UserBehavior.csv"
SAMPLE_DATA_DIR = PROJECT_DIR / "data" / "sample"

column_names = [
    "user_id",
    "item_id",
    "category_id",
    "behavior_type",
    "timestamp",
]

def main():
    df = pd.read_csv(
        RAW_DATA_PATH,
        names=column_names,
        nrows=100000
    )

    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    df["date"] = df["datetime"].dt.date

    print("\n===== 行为类型分布 =====")
    print(df["behavior_type"].value_counts())
    SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    sample_output_path = SAMPLE_DATA_DIR / "user_behavior_100k.csv"
    df.to_csv(sample_output_path, index=False, encoding="utf-8-sig")

    print("\n===== 样本数据已保存 =====")
    print(sample_output_path)

    print("===== 原始前 5 行数据 =====")
    print(df.head(5))


    print("\n===== 字段类型 =====")
    print(df.dtypes)

if __name__ == "__main__":
    main()