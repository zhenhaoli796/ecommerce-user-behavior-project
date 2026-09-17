from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    print("===== 数据前 5 行 =====")
    print(df.head())

    print("\n===== 数据规模 =====")
    print(df.shape)

    print("\n===== 字段类型 =====")
    print(df.dtypes)

    print("\n===== 缺失值统计 =====")
    print(df.isnull().sum())

    print("\n===== 行为类型分布 =====")
    print(df["behavior_type"].value_counts())

    print("\n===== 核心数量统计 =====")
    print("用户数：", df["user_id"].nunique())
    print("商品数：", df["item_id"].nunique())
    print("类别数：", df["category_id"].nunique())


if __name__ == "__main__":
    main()