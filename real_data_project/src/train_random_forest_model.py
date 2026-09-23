from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


PROJECT_DIR = Path(__file__).resolve().parents[1]
FEATURE_DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "purchase_features_3d.csv"
)
METRICS_OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed" / "random_forest_metrics_3d.csv"
)
IMPORTANCE_OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "random_forest_feature_importances_3d.csv"
)

VALIDATION_START = pd.Timestamp("2017-11-28 00:00:00")
TEST_START = pd.Timestamp("2017-11-29 00:00:00")
THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def create_model():
    return RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )


def evaluate_at_threshold(y_true, probabilities, threshold):
    predictions = (probabilities >= threshold).astype(int)
    return {
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(
            y_true, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_true, predictions, zero_division=0
        ),
        "f1": f1_score(y_true, predictions, zero_division=0),
    }


def main():
    feature_df = pd.read_csv(FEATURE_DATA_PATH)
    feature_df["first_interest_time"] = pd.to_datetime(
        feature_df["first_interest_time"]
    )

    metadata_columns = {
        "candidate_id",
        "user_id",
        "item_id",
        "category_id",
        "first_interest_time",
        "label",
    }
    feature_columns = [
        column
        for column in feature_df.columns
        if column not in metadata_columns
    ]

    train_df = feature_df.loc[
        feature_df["first_interest_time"] < TEST_START
    ].copy()
    test_df = feature_df.loc[
        feature_df["first_interest_time"] >= TEST_START
    ].copy()

    model_train_df = train_df.loc[
        train_df["first_interest_time"] < VALIDATION_START
    ].copy()
    validation_df = train_df.loc[
        train_df["first_interest_time"] >= VALIDATION_START
    ].copy()

    print("\n===== feature count =====")
    print(len(feature_columns))

    for name, subset in [
        ("model train", model_train_df),
        ("validation", validation_df),
        ("test", test_df),
    ]:
        print(f"\n===== {name} shape and purchase rate =====")
        print(subset.shape)
        print(round(subset["label"].mean(), 4))

    validation_model = create_model()
    validation_model.fit(
        model_train_df[feature_columns],
        model_train_df["label"],
    )
    validation_probabilities = validation_model.predict_proba(
        validation_df[feature_columns]
    )[:, 1]

    threshold_results = []
    for threshold in THRESHOLDS:
        result = evaluate_at_threshold(
            validation_df["label"],
            validation_probabilities,
            threshold,
        )
        result["threshold"] = threshold
        threshold_results.append(result)

    threshold_results = pd.DataFrame(threshold_results)
    best_threshold = threshold_results.loc[
        threshold_results["f1"].idxmax(), "threshold"
    ]

    print("\n===== validation threshold results =====")
    print(
        threshold_results[
            ["threshold", "precision", "recall", "f1"]
        ].round(4)
    )
    print("\n===== selected threshold by validation F1 =====")
    print(best_threshold)

    final_model = create_model()
    final_model.fit(
        train_df[feature_columns],
        train_df["label"],
    )

    test_probabilities = final_model.predict_proba(
        test_df[feature_columns]
    )[:, 1]
    test_predictions = (
        test_probabilities >= best_threshold
    ).astype(int)

    test_metrics = evaluate_at_threshold(
        test_df["label"],
        test_probabilities,
        best_threshold,
    )
    test_metrics["roc_auc"] = roc_auc_score(
        test_df["label"], test_probabilities
    )
    test_metrics["pr_auc"] = average_precision_score(
        test_df["label"], test_probabilities
    )
    test_metrics["selected_threshold"] = best_threshold

    print("\n===== final test metrics =====")
    print(pd.Series(test_metrics).round(4))
    print("\n===== final test confusion matrix =====")
    print(confusion_matrix(test_df["label"], test_predictions))

    pd.DataFrame([test_metrics]).to_csv(
        METRICS_OUTPUT_PATH, index=False
    )

    importances = pd.DataFrame({
        "feature": feature_columns,
        "importance": final_model.feature_importances_,
    }).sort_values("importance", ascending=False)

    importances.to_csv(IMPORTANCE_OUTPUT_PATH, index=False)

    print("\n===== top feature importances =====")
    print(importances.head(15))
    print("\n===== metrics saved path =====")
    print(METRICS_OUTPUT_PATH)
    print("\n===== importances saved path =====")
    print(IMPORTANCE_OUTPUT_PATH)


if __name__ == "__main__":
    main()