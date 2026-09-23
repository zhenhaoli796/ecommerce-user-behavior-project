from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
FEATURE_DATA_PATH = PROJECT_DIR / "data" / "processed" / "purchase_features_3d.csv"
METRICS_OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "model_metrics_3d.csv"

TEST_START = pd.Timestamp("2017-11-29 00:00:00")
VALIDATION_START = pd.Timestamp("2017-11-28 00:00:00")

THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

COEFFICIENT_OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed" / "logistic_feature_coefficients_3d.csv"
)

def load_feature_data():
    feature_df = pd.read_csv(FEATURE_DATA_PATH)
    feature_df["first_interest_time"] = pd.to_datetime(
        feature_df["first_interest_time"]
    )
    return feature_df


def create_model():
    return Pipeline(
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


def evaluate_at_threshold(y_true, y_probability, threshold):
    y_pred = (y_probability >= threshold).astype(int)

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }


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

print("===== feature count =====")
print(len(feature_columns))

print("\n===== model train shape and purchase rate =====")
print(model_train_df.shape)
print(model_train_df["label"].mean().round(4))

print("\n===== validation shape and purchase rate =====")
print(validation_df.shape)
print(validation_df["label"].mean().round(4))

print("\n===== test shape and purchase rate =====")
print(test_df.shape)
print(test_df["label"].mean().round(4))

X_model_train = model_train_df[feature_columns]
y_model_train = model_train_df["label"]

X_validation = validation_df[feature_columns]
y_validation = validation_df["label"]

validation_model = create_model()
validation_model.fit(X_model_train, y_model_train)

validation_probability = validation_model.predict_proba(X_validation)[:, 1]

threshold_results = []

for threshold in THRESHOLDS:
    threshold_metric = evaluate_at_threshold(
        y_validation,
        validation_probability,
        threshold,
    )
    threshold_metric["threshold"] = threshold
    threshold_results.append(threshold_metric)

threshold_results = pd.DataFrame(threshold_results)

best_threshold_row = threshold_results.loc[
    threshold_results["f1"].idxmax()
]

best_threshold = best_threshold_row["threshold"]

print("\n===== validation threshold results =====")
print(
    threshold_results[
        ["threshold", "precision", "recall", "f1"]
    ].round(4)
)

print("\n===== selected threshold by validation F1 =====")
print(best_threshold)

X_train = train_df[feature_columns]
y_train = train_df["label"]

X_test = test_df[feature_columns]
y_test = test_df["label"]

final_model = create_model()
final_model.fit(X_train, y_train)

test_probability = final_model.predict_proba(X_test)[:, 1]

test_metrics = evaluate_at_threshold(
    y_test,
    test_probability,
    best_threshold,
)

test_metrics["roc_auc"] = roc_auc_score(y_test, test_probability)
test_metrics["pr_auc"] = average_precision_score(y_test, test_probability)
test_metrics["selected_threshold"] = best_threshold

test_pred = (test_probability >= best_threshold).astype(int)

print("\n===== final test metrics =====")
print(pd.Series(test_metrics).round(4))

print("\n===== final test confusion matrix =====")
print(confusion_matrix(y_test, test_pred))

pd.DataFrame([test_metrics]).to_csv(
    METRICS_OUTPUT_PATH,
    index=False,
)

print("\n===== metrics saved path =====")
print(METRICS_OUTPUT_PATH)

coefficients = pd.DataFrame(
    {
        "feature": feature_columns,
        "coefficient": final_model.named_steps[
            "logistic_regression"
        ].coef_[0],
    }
)

coefficients["abs_coefficient"] = coefficients[
    "coefficient"
].abs()

coefficients = coefficients.sort_values(
    "coefficient",
    ascending=False,
)

coefficients.to_csv(
    COEFFICIENT_OUTPUT_PATH,
    index=False,
)

print("\n===== top positive features =====")
print(coefficients.head(10)[["feature", "coefficient"]])

print("\n===== top negative features =====")
print(coefficients.tail(10)[["feature", "coefficient"]])

print("\n===== coefficients saved path =====")
print(COEFFICIENT_OUTPUT_PATH)
