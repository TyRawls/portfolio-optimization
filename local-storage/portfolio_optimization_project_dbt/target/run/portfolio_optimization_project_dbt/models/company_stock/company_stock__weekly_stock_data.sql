
  
    

  create  table "company_stock"."public"."company_stock__weekly_stock_data__dbt_tmp"
  
  
    as
  
  (
    /*
    Create a Common Table Expression (CTE) for getting the 
    average weekly stock price for each ticker.
*/



with weekly_stock_data as (
	select date_trunc('week', date)::date as weekly_date,
	       min(date) as week_start_date,
	       max(date) as week_end_date,
		   count(date) as days_in_week,
		   ticker,
		   avg(open) as weekly_open,	
		   avg(high) as weekly_high,	
		   avg(low) as weekly_low,	
		   avg(close) as weekly_close,
	       sum(volume) as weekly_volume
	from "company_stock"."public"."company_stock__daily_stock_data"
	group by weekly_date,
			 ticker
	order by weekly_date,
			 ticker
),

final as (
	select extract(week from weekly_date) as week,
	   week_start_date,
       week_end_date,
	   days_in_week,
	   ticker,
	   round(weekly_open::numeric, 3) as weekly_open,
	   round(weekly_high::numeric, 3) as weekly_high,
	   round(weekly_low::numeric, 3) as weekly_low,
	   round(weekly_close::numeric, 3) as weekly_close,
	   weekly_volume
	from weekly_stock_data
)

select * from final
  );
  