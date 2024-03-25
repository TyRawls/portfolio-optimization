{{ config(materialized='table') }}

with source_daily_stock_data as (
	select * from {{ source('company_stock', 'daily_stock_data') }}
),

final as (
    SELECT * from source_daily_stock_data
)

select * from final
