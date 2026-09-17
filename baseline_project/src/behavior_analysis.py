from pathlib import Path

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    behavior_count = df["behavior_type"].value_counts().reset_index()
    behavior_count.columns = ["behavior_type", "count"]

    behavior_count["ratio"] = behavior_count["count"] / behavior_count["count"].sum()

    print("===== 行为次数与占比 =====")
    print(behavior_count)


if __name__ == "__main__":
    main()