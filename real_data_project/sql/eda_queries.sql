-- real data eda sql queries
-- dataset: user_behavior_100k.csv
-- database: sqlite

-- real data eda sql queries
-- dataset: user_behavior_100k.csv
-- database: sqlite


-- 1. 行为分布
select
    behavior_type,
    count(*) as behavior_count
from user_behavior
group by behavior_type
order by behavior_count desc;


-- 2. dau
select
    date,
    count(distinct user_id) as dau
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by date
order by date;


-- 3. 每日核心指标
select
    date,
    count(*) as behavior_count,
    count(distinct user_id) as dau,
    count(distinct case when behavior_type = 'buy' then user_id end) as buy_users,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by date
order by date;


-- 4. 每日购买用户转化率
select
    date,
    count(distinct user_id) as dau,
    count(distinct case when behavior_type = 'buy' then user_id end) as buy_users,
    round(
            1.0 * count(distinct case when behavior_type = 'buy' then user_id end)
                / count(distinct user_id),
            4
    ) as buy_user_rate
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by date
order by date;


-- 5. 行为漏斗
select
    behavior_type,
    count(*) as behavior_count,
    round(1.0 * count(*) / sum(count(*)) over (), 4) as behavior_ratio
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by behavior_type
order by behavior_count desc;


-- 6. 商品转化率
select
    item_id,
    sum(case when behavior_type = 'pv' then 1 else 0 end) as pv_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    round(
            1.0 * sum(case when behavior_type = 'buy' then 1 else 0 end)
                / nullif(sum(case when behavior_type = 'pv' then 1 else 0 end), 0),
            4
    ) as buy_rate
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by item_id
having pv_count >= 20
order by buy_rate desc
limit 20;


-- 7. 类目转化率
select
    category_id,
    sum(case when behavior_type = 'pv' then 1 else 0 end) as pv_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    round(
            1.0 * sum(case when behavior_type = 'buy' then 1 else 0 end)
                / nullif(sum(case when behavior_type = 'pv' then 1 else 0 end), 0),
            4
    ) as buy_rate
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by category_id
having pv_count >= 50
order by buy_rate desc
limit 20;


-- 8. 用户行为汇总
select
    user_id,
    sum(case when behavior_type = 'pv' then 1 else 0 end) as pv_count,
    sum(case when behavior_type = 'fav' then 1 else 0 end) as fav_count,
    sum(case when behavior_type = 'cart' then 1 else 0 end) as cart_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    count(*) as total_behavior_count,
    count(distinct date) as active_days
from user_behavior
where date between '2017-11-25' and '2017-12-03'
group by user_id
order by total_behavior_count desc
limit 20;


-- 9. 用户活跃度分层
with user_summary as (
    select
        user_id,
        sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
        count(*) as total_behavior_count,
        count(distinct date) as active_days
    from user_behavior
    where date between '2017-11-25' and '2017-12-03'
    group by user_id
),
     user_level as (
         select
             user_id,
             buy_count,
             total_behavior_count,
             active_days,
             case
                 when total_behavior_count >= 100 then 'high_active'
                 when total_behavior_count >= 30 then 'middle_active'
                 else 'low_active'
                 end as active_level
         from user_summary
     )
select
    active_level,
    count(*) as user_count,
    round(avg(total_behavior_count), 2) as avg_behavior_count,
    round(avg(active_days), 2) as avg_active_days,
    sum(case when buy_count > 0 then 1 else 0 end) as buy_user_count,
    round(
            1.0 * sum(case when buy_count > 0 then 1 else 0 end) / count(*),
            4
    ) as buy_user_rate
from user_level
group by active_level
order by buy_user_rate desc;

