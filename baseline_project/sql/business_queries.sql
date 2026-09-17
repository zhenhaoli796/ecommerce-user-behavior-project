-- 1. 每日活跃用户数 dau
select
    date(event_time) as dt,
    count(distinct user_id) as dau
from user_behavior
group by date(event_time)
order by dt;


-- 2. 行为类型分布
select
    behavior_type,
    count(*) as behavior_count,
    count(distinct user_id) as user_count
from user_behavior
group by behavior_type
order by behavior_count desc;


-- 3. 商品浏览次数与购买次数
select
    item_id,
    sum(case when behavior_type = 'view' then 1 else 0 end) as view_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count
from user_behavior
group by item_id;


-- 4. 商品购买转化率
select
    item_id,
    sum(case when behavior_type = 'view' then 1 else 0 end) as view_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    1.0 * sum(case when behavior_type = 'buy' then 1 else 0 end)
        / nullif(sum(case when behavior_type = 'view' then 1 else 0 end), 0) as conversion_rate
from user_behavior
group by item_id
having sum(case when behavior_type = 'view' then 1 else 0 end) >= 10
order by conversion_rate desc;


-- 5. 类目购买转化率
select
    category_id,
    sum(case when behavior_type = 'view' then 1 else 0 end) as view_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    1.0 * sum(case when behavior_type = 'buy' then 1 else 0 end)
        / nullif(sum(case when behavior_type = 'view' then 1 else 0 end), 0) as conversion_rate
from user_behavior
group by category_id
having sum(case when behavior_type = 'view' then 1 else 0 end) >= 10
order by conversion_rate desc;


-- 6. 用户行为汇总
select
    user_id,
    sum(case when behavior_type = 'view' then 1 else 0 end) as view_count,
    sum(case when behavior_type = 'fav' then 1 else 0 end) as fav_count,
    sum(case when behavior_type = 'cart' then 1 else 0 end) as cart_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    count(*) as total_behavior_count
from user_behavior
group by user_id
order by total_behavior_count desc;


-- 7. 复购用户
select
    user_id,
    count(*) as buy_count,
    count(distinct item_id) as bought_item_count
from user_behavior
where behavior_type = 'buy'
group by user_id
having count(*) >= 2
order by buy_count desc;


-- 8. 每个类目购买次数 top 3 商品
select *
from (
         select
             category_id,
             item_id,
             count(*) as buy_count,
             row_number() over (
                 partition by category_id
                 order by count(*) desc
                 ) as rn
         from user_behavior
         where behavior_type = 'buy'
         group by category_id, item_id
     ) t
where rn <= 3;


-- 9. 用户最近一次行为
select *
from (
         select
             user_id,
             item_id,
             category_id,
             behavior_type,
             event_time,
             row_number() over (
                 partition by user_id
                 order by event_time desc
                 ) as rn
         from user_behavior
     ) t
where rn = 1;


-- 10. 构建用户-商品特征表
select
    user_id,
    item_id,
    sum(case when behavior_type = 'view' then 1 else 0 end) as view_count,
    sum(case when behavior_type = 'fav' then 1 else 0 end) as fav_count,
    sum(case when behavior_type = 'cart' then 1 else 0 end) as cart_count,
    sum(case when behavior_type = 'buy' then 1 else 0 end) as buy_count,
    case
        when sum(case when behavior_type = 'buy' then 1 else 0 end) > 0 then 1
        else 0
        end as label
from user_behavior
group by user_id, item_id;