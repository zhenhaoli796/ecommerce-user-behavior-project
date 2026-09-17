# E-commerce User Behavior Analysis and Recommendation System

## 项目简介

本项目基于电商用户行为数据，围绕用户行为分析、购买预测和商品推荐三个方向展开。

项目首先使用 pandas 对用户浏览、收藏、加购、购买等行为进行探索性分析，统计行为分布、每日活跃用户数、商品转化率、类目转化率和用户活跃度。随后构建用户-商品维度的机器学习特征，并使用逻辑回归模型预测用户是否会购买某个商品。最后实现热门商品推荐和基于物品协同过滤的个性化推荐 baseline。

## 项目目标

本项目主要回答以下问题：

1. 用户在平台上的整体行为分布如何？
2. 哪些商品和类目的购买转化率更高？
3. 不同用户的活跃程度是否存在差异？
4. 是否可以根据用户历史行为预测其购买倾向？
5. 是否可以根据用户行为生成商品推荐结果？

## 技术栈

- Python
- pandas
- numpy
- scikit-learn
- 逻辑回归
- Item-Based Collaborative Filtering
- Git / GitHub

## 项目结构

```text
ecommerce-user-behavior-project
├── data
│   ├── raw
│   │   └── user_behavior_sample.csv
│   └── processed
│       ├── user_item_features.csv
│       ├── model_metrics.csv
│       ├── popular_recommendations.csv
│       └── item_cf_recommendations.csv
├── docs
│   └── analysis_notes.md
├── notebooks
├── sql
├── src
│   ├── generate_sample_data.py
│   ├── explore_data.py
│   ├── behavior_analysis.py
│   ├── dau_analysis.py
│   ├── item_conversion_analysis.py
│   ├── category_conversion_analysis.py
│   ├── user_behavior_analysis.py
│   ├── build_features.py
│   ├── train_model.py
│   ├── popular_recommendation.py
│   └── item_cf_recommendation.py
└── README.md