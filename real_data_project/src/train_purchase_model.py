from pathlib import Path

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
FEATURE_DATA_PATH = PROJECT_DIR / "data" / "processed" / "purchase_features_3d.csv"

TEST_START = pd.Timestamp("2017-11-29 00:00:00")
VALIDATION_START = pd.Timestamp("2017-11-28 00:00:00")

def load_feature_data():
    feature_df = pd.read_csv(FEATURE_DATA_PATH)
    feature_df["first_interest_time"] = pd.to_datetime(
        feature_df["first_interest_time"]
    )
    return feature_df


feature_df = load_feature_data()

metadata_columns = [
    "candidate_id",
    "user_id",
    "item_id",
    "category_id",
    "first_interest_time",
    "label",
]

feature_columns = [
    column
    for column in feature_df.columns
    if column not in metadata_columns
]

train_df = feature_df[
    feature_df["first_interest_time"] < TEST_START
].copy()

test_df = feature_df[
    feature_df["first_interest_time"] >= TEST_START
].copy()
model_train_df = train_df[
    train_df["first_interest_time"] < VALIDATION_START
].copy()

validation_df = train_df[
    train_df["first_interest_time"] >= VALIDATION_START
].copy()

print("\n===== model train shape and purchase rate =====")
print(model_train_df.shape)
print(model_train_df["label"].mean().round(4))

print("\n===== validation shape and purchase rate =====")
print(validation_df.shape)
print(validation_df["label"].mean().round(4))

print("===== feature count =====")
print(len(feature_columns))

print("\n===== train shape and purchase rate =====")
print(train_df.shape)
print(train_df["label"].mean().round(4))

print("\n===== test shape and purchase rate =====")
print(test_df.shape)
print(test_df["label"].mean().round(4))

X_train = train_df[feature_columns]
y_train = train_df["label"]

X_test = test_df[feature_columns]
y_test = test_df["label"]

model = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        (
            "logistic_regression",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            ),
        ),
    ]
)

model.fit(X_train, y_train)

print("\n===== model training completed =====")
print(model)

y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, zero_division=0),
    "recall": recall_score(y_test, y_pred, zero_division=0),
    "f1": f1_score(y_test, y_pred, zero_division=0),
    "roc_auc": roc_auc_score(y_test, y_probability),
    "pr_auc": average_precision_score(y_test, y_probability),
}

print("\n===== test metrics =====")
print(pd.Series(metrics).round(4))

print("\n===== confusion matrix =====")
print(confusion_matrix(y_test, y_pred))