select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quarterly_open
from "company_stock"."public"."company_stock__quarterly_stock_data"
where quarterly_open is null



      
    ) dbt_internal_test