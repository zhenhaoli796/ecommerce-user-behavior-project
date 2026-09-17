from pathlib import Path
from itertools import combinations
from collections import defaultdict

import pandas as pd


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project")
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "user_behavior_sample.csv"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


BEHAVIOR_WEIGHT = {
    "view": 1,
    "fav": 2,
    "cart": 3,
    "buy": 5
}


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    df["behavior_weight"] = df["behavior_type"].map(BEHAVIOR_WEIGHT)

    user_item_score = (
        df.groupby(["user_id", "item_id"])["behavior_weight"]
        .sum()
        .reset_index(name="score")
    )

    user_items = (
        user_item_score.groupby("user_id")["item_id"]
        .apply(list)
        .to_dict()
    )

    co_occurrence = defaultdict(lambda: defaultdict(int))
    item_count = defaultdict(int)

    for items in user_items.values():
        unique_items = list(set(items))

        for item in unique_items:
            item_count[item] += 1

        for item_a, item_b in combinations(unique_items, 2):
            co_occurrence[item_a][item_b] += 1
            co_occurrence[item_b][item_a] += 1

    item_similarity = defaultdict(dict)

    for item_a, related_items in co_occurrence.items():
        for item_b, co_count in related_items.items():
            similarity = co_count / (item_count[item_a] * item_count[item_b]) ** 0.5
            item_similarity[item_a][item_b] = similarity

    recommend_rows = []

    target_users = user_item_score["user_id"].drop_duplicates().head(20)

    for target_user in target_users:
        interacted_items = set(
            user_item_score[user_item_score["user_id"] == target_user]["item_id"]
        )

        recommend_scores = defaultdict(float)

        for item in interacted_items:
            similar_items = item_similarity.get(item, {})

            for similar_item, similarity in similar_items.items():
                if similar_item in interacted_items:
                    continue

                recommend_scores[similar_item] += similarity

        user_recommend_result = (
            pd.DataFrame([
                {"user_id": target_user, "item_id": item, "recommend_score": score}
                for item, score in recommend_scores.items()
            ])
            .sort_values(by="recommend_score", ascending=False)
            .head(10)
        )

        recommend_rows.append(user_recommend_result)

    recommend_result = pd.concat(recommend_rows, ignore_index=True)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / "item_cf_recommendations.csv"
    recommend_result.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("===== 多用户个性化推荐结果 =====")
    print(recommend_result)

    print("\n物品协同过滤推荐结果已保存：")
    print(output_path)


if __name__ == "__main__":
    main()