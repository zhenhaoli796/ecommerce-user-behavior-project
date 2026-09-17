from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
FEATURE_PATH = PROJECT_DIR / "data" / "processed" / "user_item_features.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def main():
    df = pd.read_csv(FEATURE_PATH)

    feature_cols = ["view", "cart", "fav"]
    X = df[feature_cols]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression(class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("===== 模型评估结果 =====")
    print("accuracy:", accuracy)
    print("precision:", precision)
    print("recall:", recall)
    print("f1:", f1)

    metrics_df = pd.DataFrame({
        "model": ["logistic_regression"],
        "accuracy": [accuracy],
        "precision": [precision],
        "recall": [recall],
        "f1": [f1]
    })

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    metrics_path = PROCESSED_DATA_DIR / "model_metrics.csv"
    metrics_df.to_csv(metrics_path, index=False, encoding="utf-8-sig")

    print("\n模型评估结果已保存：")
    print(metrics_path)


if __name__ == "__main__":
    main()