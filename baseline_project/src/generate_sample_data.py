from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def generate_sample_data():
    np.random.seed(42)

    user_ids = np.arange(1, 101)
    item_ids = np.arange(1, 51)
    category_ids = np.arange(1, 11)

    behavior_types = ["view", "cart", "fav", "buy"]
    behavior_probs = [0.75, 0.10, 0.10, 0.05]

    data_size = 1000

    df = pd.DataFrame({
        "user_id": np.random.choice(user_ids, size=data_size),
        "item_id": np.random.choice(item_ids, size=data_size),
        "category_id": np.random.choice(category_ids, size=data_size),
        "behavior_type": np.random.choice(
            behavior_types,
            size=data_size,
            p=behavior_probs
        ),
        "event_time": pd.date_range(
            start="2026-01-01",
            periods=data_size,
            freq="min"
        )
    })

    return df


def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_sample_data()

    output_path = RAW_DATA_DIR / "user_behavior_sample.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("数据生成成功！")
    print(f"保存路径：{output_path}")
    print(df.head())


if __name__ == "__main__":
    main()
