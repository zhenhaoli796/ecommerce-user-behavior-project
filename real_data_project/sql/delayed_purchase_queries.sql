-- delayed purchase analysis sql queries
-- dataset: user_behavior_100k.csv
-- database: sqlite

select
    user_id,
    item_id,
    min(datetime) as first_interest_time
from user_behavior
where behavior_type in ('pv', 'fav', 'cart')
group by user_id, item_id
limit 20;



-- 2. 首次兴趣后 1 天内是否购买
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
)
select
    fi.user_id,
    fi.item_id,
    fi.first_interest_time,
    case
        when count(ub.user_id) > 0 then 1
        else 0
        end as buy_within_1d
from first_interest fi
         left join user_behavior ub
                   on fi.user_id = ub.user_id
                       and fi.item_id = ub.item_id
                       and ub.behavior_type = 'buy'
                       and ub.datetime > fi.first_interest_time
                       and ub.datetime <= datetime(fi.first_interest_time, '+1 day')
group by
    fi.user_id,
    fi.item_id,
    fi.first_interest_time
limit 20;

-- 3. 首次兴趣后 1/3/7 天内是否购买
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
)
select
    fi.user_id,
    fi.item_id,
    fi.first_interest_time,
    case
        when sum(
                     case
                         when ub.datetime > fi.first_interest_time
                             and ub.datetime <= datetime(fi.first_interest_time, '+1 day')
                             then 1 else 0
                         end
             ) > 0 then 1 else 0
        end as buy_within_1d,
    case
        when sum(
                     case
                         when ub.datetime > fi.first_interest_time
                             and ub.datetime <= datetime(fi.first_interest_time, '+3 day')
                             then 1 else 0
                         end
             ) > 0 then 1 else 0
        end as buy_within_3d,
    case
        when sum(
                     case
                         when ub.datetime > fi.first_interest_time
                             and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
                             then 1 else 0
                         end
             ) > 0 then 1 else 0
        end as buy_within_7d
from first_interest fi
         left join user_behavior ub
                   on fi.user_id = ub.user_id
                       and fi.item_id = ub.item_id
                       and ub.behavior_type = 'buy'
                       and ub.datetime > fi.first_interest_time
                       and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
group by
    fi.user_id,
    fi.item_id,
    fi.first_interest_time
limit 20;


-- 4. 首次兴趣后 1/3/7 天累计购买率
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
),
     purchase_label as (
         select
             fi.user_id,
             fi.item_id,
             fi.first_interest_time,
             case
                 when sum(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+1 day')
                                      then 1 else 0
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_1d,
             case
                 when sum(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+3 day')
                                      then 1 else 0
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_3d,
             case
                 when sum(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
                                      then 1 else 0
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_7d
         from first_interest fi
                  left join user_behavior ub
                            on fi.user_id = ub.user_id
                                and fi.item_id = ub.item_id
                                and ub.behavior_type = 'buy'
                                and ub.datetime > fi.first_interest_time
                                and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
         group by
             fi.user_id,
             fi.item_id,
             fi.first_interest_time
     )
select
    count(*) as sample_count,
    sum(buy_within_1d) as buy_1d_count,
    round(1.0 * sum(buy_within_1d) / count(*), 4) as buy_1d_rate,
    sum(buy_within_3d) as buy_3d_count,
    round(1.0 * sum(buy_within_3d) / count(*), 4) as buy_3d_rate,
    sum(buy_within_7d) as buy_7d_count,
    round(1.0 * sum(buy_within_7d) / count(*), 4) as buy_7d_rate
from purchase_label;



-- 5. 首次兴趣后 3 天购买率，保证观察窗口完整
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
),
     valid_interest as (
         select
             *
         from first_interest
         where first_interest_time <= '2017-11-30 23:59:59'
     ),
     purchase_label as (
         select
             vi.user_id,
             vi.item_id,
             vi.first_interest_time,
             case
                 when count(ub.user_id) > 0 then 1
                 else 0
                 end as buy_within_3d
         from valid_interest vi
                  left join user_behavior ub
                            on vi.user_id = ub.user_id
                                and vi.item_id = ub.item_id
                                and ub.behavior_type = 'buy'
                                and ub.datetime > vi.first_interest_time
                                and ub.datetime <= datetime(vi.first_interest_time, '+3 day')
         group by
             vi.user_id,
             vi.item_id,
             vi.first_interest_time
     )
select
    count(*) as sample_count,
    sum(buy_within_3d) as buy_3d_count,
    round(1.0 * sum(buy_within_3d) / count(*), 4) as buy_3d_rate
from purchase_label;


-- 6. 首次兴趣后 1/3/7 天购买率，保证观察窗口完整
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
),
     purchase_label as (
         select
             fi.user_id,
             fi.item_id,
             fi.first_interest_time,
             case
                 when count(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+1 day')
                                      then 1
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_1d,
             case
                 when count(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+3 day')
                                      then 1
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_3d,
             case
                 when count(
                              case
                                  when ub.datetime > fi.first_interest_time
                                      and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
                                      then 1
                                  end
                      ) > 0 then 1 else 0
                 end as buy_within_7d
         from first_interest fi
                  left join user_behavior ub
                            on fi.user_id = ub.user_id
                                and fi.item_id = ub.item_id
                                and ub.behavior_type = 'buy'
                                and ub.datetime > fi.first_interest_time
                                and ub.datetime <= datetime(fi.first_interest_time, '+7 day')
         group by
             fi.user_id,
             fi.item_id,
             fi.first_interest_time
     )
select
    '1d' as window,
    count(*) as sample_count,
    sum(buy_within_1d) as buy_count,
    round(1.0 * sum(buy_within_1d) / count(*), 4) as buy_rate
from purchase_label
where first_interest_time <= '2017-12-02 23:59:59'

union all

select
    '3d' as window,
    count(*) as sample_count,
    sum(buy_within_3d) as buy_count,
    round(1.0 * sum(buy_within_3d) / count(*), 4) as buy_rate
from purchase_label
where first_interest_time <= '2017-11-30 23:59:59'

union all

select
    '7d' as window,
    count(*) as sample_count,
    sum(buy_within_7d) as buy_count,
    round(1.0 * sum(buy_within_7d) / count(*), 4) as buy_rate
from purchase_label
where first_interest_time <= '2017-11-26 23:59:59';


-- 7. 不同首次兴趣行为的 3 天购买率
with first_interest as (
    select
        user_id,
        item_id,
        datetime as first_interest_time,
        behavior_type as first_behavior_type
    from (
             select
                 user_id,
                 item_id,
                 datetime,
                 behavior_type,
                 row_number() over (
                     partition by user_id, item_id
                     order by datetime
                     ) as rn
             from user_behavior
             where behavior_type in ('pv', 'fav', 'cart')
         ) t
    where rn = 1
),
     valid_interest as (
         select *
         from first_interest
         where first_interest_time <= '2017-11-30 23:59:59'
     ),
     purchase_label as (
         select
             vi.user_id,
             vi.item_id,
             vi.first_interest_time,
             vi.first_behavior_type,
             case
                 when count(ub.user_id) > 0 then 1
                 else 0
                 end as buy_within_3d
         from valid_interest vi
                  left join user_behavior ub
                            on vi.user_id = ub.user_id
                                and vi.item_id = ub.item_id
                                and ub.behavior_type = 'buy'
                                and ub.datetime > vi.first_interest_time
                                and ub.datetime <= datetime(vi.first_interest_time, '+3 day')
         group by
             vi.user_id,
             vi.item_id,
             vi.first_interest_time,
             vi.first_behavior_type
     )
select
    first_behavior_type,
    count(*) as sample_count,
    sum(buy_within_3d) as buy_count,
    round(1.0 * sum(buy_within_3d) / count(*), 4) as buy_rate
from purchase_label
group by first_behavior_type
order by buy_rate desc;


-- 8. 首次兴趣到首次购买的延迟天数分布
with first_interest as (
    select
        user_id,
        item_id,
        min(datetime) as first_interest_time
    from user_behavior
    where behavior_type in ('pv', 'fav', 'cart')
    group by user_id, item_id
),
     first_purchase as (
         select
             fi.user_id,
             fi.item_id,
             fi.first_interest_time,
             min(ub.datetime) as first_buy_time
         from first_interest fi
                  join user_behavior ub
                       on fi.user_id = ub.user_id
                           and fi.item_id = ub.item_id
                           and ub.behavior_type = 'buy'
                           and ub.datetime > fi.first_interest_time
         group by
             fi.user_id,
             fi.item_id,
             fi.first_interest_time
     ),
     purchase_delay as (
         select
             user_id,
             item_id,
             first_interest_time,
             first_buy_time,
             julianday(first_buy_time) - julianday(first_interest_time) as delay_days
         from first_purchase
     )
select
    case
        when delay_days <= 1 then '0-1d'
        when delay_days <= 3 then '1-3d'
        when delay_days <= 7 then '3-7d'
        else '7d+'
        end as delay_bucket,
    count(*) as buy_count
from purchase_delay
group by delay_bucket
order by
    case delay_bucket
        when '0-1d' then 1
        when '1-3d' then 2
        when '3-7d' then 3
        else 4
        end;






