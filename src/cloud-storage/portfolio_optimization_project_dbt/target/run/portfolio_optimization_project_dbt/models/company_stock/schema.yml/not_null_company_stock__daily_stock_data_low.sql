select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select low
from "company_stock"."public"."company_stock__daily_stock_data"
where low is null



      
    ) dbt_internal_test