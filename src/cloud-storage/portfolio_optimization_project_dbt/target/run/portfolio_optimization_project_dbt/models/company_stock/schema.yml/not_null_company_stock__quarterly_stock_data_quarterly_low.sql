select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quarterly_low
from "company_stock"."public"."company_stock__quarterly_stock_data"
where quarterly_low is null



      
    ) dbt_internal_test