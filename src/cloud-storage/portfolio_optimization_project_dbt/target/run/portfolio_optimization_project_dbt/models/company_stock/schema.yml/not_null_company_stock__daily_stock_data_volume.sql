select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select volume
from "company_stock"."public"."company_stock__daily_stock_data"
where volume is null



      
    ) dbt_internal_test