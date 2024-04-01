select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select month
from "company_stock"."public"."company_stock__monthly_stock_data"
where month is null



      
    ) dbt_internal_test