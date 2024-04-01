select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select weekly_open
from "company_stock"."public"."company_stock__weekly_stock_data"
where weekly_open is null



      
    ) dbt_internal_test