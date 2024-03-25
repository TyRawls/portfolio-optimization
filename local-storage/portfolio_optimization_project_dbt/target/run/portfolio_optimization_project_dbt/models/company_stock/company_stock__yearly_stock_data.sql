
  
    

  create  table "company_stock"."public"."company_stock__yearly_stock_data__dbt_tmp"
  
  
    as
  
  (
    /*
    Create a Common Table Expression (CTE) for getting the 
    average yearly stock price for each ticker.
*/



with yearly_stock_data as (
	select date_trunc('year', date)::date as yearly_date,
	       min(date) as year_start_date,
	       max(date) as year_end_date,
		   count(date) as days_in_year, 
		   ticker,
		   avg(open) as yearly_open,	
		   avg(high) as yearly_high,	
		   avg(low) as yearly_low,	
		   avg(close) as yearly_close,
	       sum(volume) as yearly_volume
	from "company_stock"."public"."company_stock__daily_stock_data"
	group by yearly_date,
			 ticker
	order by yearly_date,
			 ticker
),

final as (
	select extract(year from yearly_date) as year,
		year_start_date,
		year_end_date,
		days_in_year,
		ticker,
		round(yearly_open::numeric, 3) as yearly_open,
		round(yearly_high::numeric, 3) as yearly_high,
		round(yearly_low::numeric, 3) as yearly_low,
		round(yearly_close::numeric, 3) as yearly_close,
		yearly_volume
	from yearly_stock_data
)

select * from final
  );
  