
  
    

  create  table "company_stock"."public"."company_stock__monthly_stock_data__dbt_tmp"
  
  
    as
  
  (
    /*
    Create a Common Table Expression (CTE) for getting the 
    average monthly stock price for each ticker.
*/



with monthly_stock_data as (
	select date_trunc('month', date)::date as monthly_date,
	       min(date) as month_start_date,
	       max(date) as month_end_date,
		   count(date) as days_in_month, 
		   ticker,
		   avg(open) as monthly_open,	
		   avg(high) as monthly_high,	
		   avg(low) as monthly_low,	
		   avg(close) as monthly_close,
	       sum(volume) as monthly_volume
	from "company_stock"."public"."company_stock__daily_stock_data"
	group by monthly_date,
			 ticker
	order by monthly_date,
			 ticker
),

final as (
	select extract(month from monthly_date) as month,
		month_start_date,
		month_end_date,
		days_in_month,
		ticker,
		round(monthly_open::numeric, 3) as monthly_open,
		round(monthly_high::numeric, 3) as monthly_high,
		round(monthly_low::numeric, 3) as monthly_low,
		round(monthly_close::numeric, 3) as monthly_close,
		monthly_volume
	from monthly_stock_data
)

select * from final
  );
  