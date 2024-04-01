select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quarterly_volume
from "company_stock"."public"."company_stock__quarterly_stock_data"
where quarterly_volume is null



      
    ) dbt_internal_test