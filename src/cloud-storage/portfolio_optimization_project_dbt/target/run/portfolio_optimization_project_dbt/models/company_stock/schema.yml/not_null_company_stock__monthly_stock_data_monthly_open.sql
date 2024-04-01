select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select monthly_open
from "company_stock"."public"."company_stock__monthly_stock_data"
where monthly_open is null



      
    ) dbt_internal_test