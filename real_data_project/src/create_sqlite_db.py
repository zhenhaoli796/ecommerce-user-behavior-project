from pathlib import Path

import pandas as pd
import sqlite3


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
SAMPLE_DATA_PATH = PROJECT_DIR / "data" / "sample" / "user_behavior_100k.csv"
DB_PATH = PROJECT_DIR / "data" / "processed" / "user_behavior.db"




def main():
    df = pd.read_csv(SAMPLE_DATA_PATH)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "user_behavior",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("===== 样本数据预览 =====")
    print(df.head())

    print("\n===== 数据规模 =====")
    print(df.shape)

    print("\n===== SQLite 数据库已创建 =====")
    print(DB_PATH)


if __name__ == "__main__":
    main()