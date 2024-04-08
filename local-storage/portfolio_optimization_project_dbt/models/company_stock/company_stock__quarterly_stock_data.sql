/*
    Create a Common Table Expression (CTE) for getting the 
    average quarterly stock price for each ticker.
*/

{{ config(materialized='table') }}

with quarterly_stock_data as (
	select date_trunc('quarter', date)::date as quarterly_date,
	       min(date) as quarter_start_date,
	       max(date) as quarter_end_date,
		   count(date) as days_in_quarter, 
		   ticker,
		   avg(open) as quarterly_open,	
		   avg(high) as quarterly_high,	
		   avg(low) as quarterly_low,	
		   avg(close) as quarterly_close,
	       sum(volume) as quarterly_volume
	from {{ ref('company_stock__daily_stock_data') }}
	group by quarterly_date,
			 ticker
	order by quarterly_date,
			 ticker
),

final as (
	select extract(quarter from quarterly_date) as quarter,
		quarter_start_date,
		quarter_end_date,
		days_in_quarter,
		ticker,
		round(quarterly_open::numeric, 3) as quarterly_open,
		round(quarterly_high::numeric, 3) as quarterly_high,
		round(quarterly_low::numeric, 3) as quarterly_low,
		round(quarterly_close::numeric, 3) as quarterly_close,
		quarterly_volume
	from quarterly_stock_data
)

select * from final
