-- models/orders.sql
select
    order_id,
    customer,
    amount,
    processed
from {{ ref('raw_orders') }}