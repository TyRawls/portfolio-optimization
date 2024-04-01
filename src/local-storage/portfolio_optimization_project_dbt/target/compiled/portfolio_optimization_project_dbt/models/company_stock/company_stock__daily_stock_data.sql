

with source_daily_stock_data as (
	select * from "company_stock"."public"."daily_stock_data"
),

final as (
    SELECT * from source_daily_stock_data
)

select * from final