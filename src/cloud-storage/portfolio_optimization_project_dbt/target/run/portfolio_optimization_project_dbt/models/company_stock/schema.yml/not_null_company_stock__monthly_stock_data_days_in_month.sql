select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select days_in_month
from "company_stock"."public"."company_stock__monthly_stock_data"
where days_in_month is null



      
    ) dbt_internal_test