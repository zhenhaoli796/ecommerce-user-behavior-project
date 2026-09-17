# E-commerce User Behavior Analysis Project

## 项目简介

本仓库用于记录电商用户行为分析项目的完整迭代过程。项目从一个小规模 baseline 版本开始，逐步升级到基于真实用户行为数据的分析、建模和推荐系统项目。

仓库分为两个阶段：

1. `baseline_project`：使用模拟数据跑通完整流程，包括用户行为分析、SQL 指标练习、购买预测模型和推荐系统 baseline。
2. `real_data_project`：后续升级版本，计划使用真实用户行为数据，重点完善 SQL 实操、时间窗口特征工程、模型对比和推荐效果评估。

## 仓库结构

- `baseline_project/`：第一阶段基础版项目
- `real_data_project/`：第二阶段真实数据升级版项目
- `.gitignore`：Git 忽略规则
- `requirements.txt`：项目依赖
- `README.md`：仓库总说明

## 阶段一：Baseline Project

`baseline_project` 是项目的第一阶段，主要目标是跑通完整项目流程。

已完成内容包括：

- 使用模拟数据构建用户行为日志；
- 使用 pandas 完成行为分布、DAU、商品转化率、类目转化率和用户活跃度分析；
- 使用 SQL 整理常见业务指标查询；
- 构建用户-商品维度特征，并使用逻辑回归完成购买预测 baseline；
- 实现热门商品推荐和基于物品协同过滤的个性化推荐 baseline；
- 整理项目 README、分析文档和可复现运行流程。

更多说明见：`baseline_project/README.md`

## 阶段二：Real Data Project

`real_data_project` 是后续升级阶段，计划使用真实电商用户行为数据进行分析和建模。

计划升级内容包括：

- 接入真实用户行为数据；
- 使用 pandas 和 SQL 双线完成业务指标分析；
- 使用 SQLite 进行本地 SQL 实操；
- 使用时间窗口构建购买预测样本，避免数据泄漏；
- 增加用户特征、商品特征、类目特征和用户-商品交互特征；
- 对比 Logistic Regression、Random Forest、Gradient Boosting 等模型；
- 对推荐系统进行离线评估，例如 Precision@K、Recall@K 和 HitRate@K；
- 增加可视化图表和完整分析报告。

## 技术栈

- Python
- pandas
- numpy
- scikit-learn
- SQL / SQLite
- 推荐系统 baseline
- Git / GitHub

## 后续计划

下一步将在 `real_data_project` 中继续开发真实数据版本，并保留 `baseline_project` 作为第一阶段 baseline。