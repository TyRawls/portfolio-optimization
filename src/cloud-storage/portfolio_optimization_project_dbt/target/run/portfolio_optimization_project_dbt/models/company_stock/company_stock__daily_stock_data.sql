
  
    

  create  table "company_stock"."public"."company_stock__daily_stock_data__dbt_tmp"
  
  
    as
  
  (
    

with source_daily_stock_data as (
	select * from "company_stock"."public"."daily_stock_data"
),

final as (
    SELECT * from source_daily_stock_data
)

select * from final
  );
  