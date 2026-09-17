# E-commerce User Behavior Analysis and Recommendation System

## 项目简介

本项目基于电商用户行为数据，围绕用户行为分析、购买预测和商品推荐三个方向展开。

项目首先使用 pandas 对用户浏览、收藏、加购、购买等行为进行探索性分析，统计行为分布、每日活跃用户数、商品转化率、类目转化率和用户活跃度。随后整理 SQL 指标分析脚本，将常见业务指标转换为数据库查询语句。接着构建用户-商品维度的机器学习特征，并使用逻辑回归模型预测用户是否会购买某个商品。最后实现热门商品推荐和基于物品协同过滤的个性化推荐 baseline。

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
- SQL
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
│   └── business_queries.sql
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
├── .gitignore
├── requirements.txt
└── README.md
```

## 当前实现内容

### 1. 用户行为分析

已完成以下分析：

- 行为类型分布
- 每日活跃用户数 DAU
- 商品购买转化率
- 类目购买转化率
- 用户活跃度分层

### 2. SQL 指标分析

项目在 `sql/business_queries.sql` 中整理了常见业务指标查询，包括：

- 每日活跃用户数 DAU
- 行为类型分布
- 商品浏览次数与购买次数
- 商品购买转化率
- 类目购买转化率
- 用户行为汇总
- 复购用户分析
- 每个类目购买次数 TopN 商品
- 用户最近一次行为
- 用户-商品特征表构建

这些 SQL 查询与 pandas 分析逻辑相对应，用于展示将业务指标分析迁移到数据库场景下的能力。

### 3. 购买预测模型

将用户-商品交互数据构造成机器学习样本，使用以下特征预测用户是否购买商品：

- 浏览次数 view
- 收藏次数 fav
- 加购次数 cart

第一版模型使用逻辑回归作为 baseline，并保存模型评估结果。

### 4. 推荐系统

实现了两类推荐 baseline：

- 热门商品推荐：根据全站用户行为计算商品热度；
- ItemCF 个性化推荐：根据商品共现关系计算物品相似度，并为多个用户生成 TopN 推荐结果。

## 模型结果

逻辑回归 baseline 在模拟数据上的结果如下：

| 指标      | 数值   |
| --------- | ------ |
| Accuracy  | 0.9945 |
| Precision | 1.0000 |
| Recall    | 0.9167 |
| F1        | 0.9565 |

注意：当前数据为模拟数据，模型结果偏高不能直接代表真实业务效果。后续需要使用真实数据集，并通过时间窗口方式构造训练集和测试集，以降低数据泄漏风险。

## 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

生成模拟数据：

```bash
python src/generate_sample_data.py
```

数据检查：

```bash
python src/explore_data.py
```

构建用户-商品特征：

```bash
python src/build_features.py
```

训练购买预测模型：

```bash
python src/train_model.py
```

生成热门商品推荐：

```bash
python src/popular_recommendation.py
```

生成 ItemCF 个性化推荐：

```bash
python src/item_cf_recommendation.py
```

## 项目收获

通过本项目，我完成了从用户行为数据分析到机器学习建模、再到推荐系统 baseline 的完整流程，重点练习了：

- 使用 pandas 进行数据清洗、分组统计和指标分析；
- 使用 SQL 编写常见业务指标查询；
- 从业务问题出发设计分析指标；
- 构建用户-商品维度的机器学习特征；
- 使用逻辑回归完成二分类购买预测；
- 实现热门推荐和基于物品相似度的协同过滤推荐；
- 将分析过程整理为可复现的项目文档。

## 后续优化方向

1. 使用真实公开电商行为数据集替换模拟数据；
2. 按时间窗口构造训练集和测试集，避免数据泄漏；
3. 增加用户画像、商品热度、类目偏好等特征；
4. 尝试随机森林、LightGBM 等模型并进行对比；
5. 增加推荐效果评估指标，例如 Precision@K、Recall@K；
6. 增加可视化图表和完整分析报告。