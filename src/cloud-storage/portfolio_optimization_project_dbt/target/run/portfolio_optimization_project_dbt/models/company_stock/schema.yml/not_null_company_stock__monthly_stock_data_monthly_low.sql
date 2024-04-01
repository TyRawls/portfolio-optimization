select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select monthly_low
from "company_stock"."public"."company_stock__monthly_stock_data"
where monthly_low is null



      
    ) dbt_internal_test