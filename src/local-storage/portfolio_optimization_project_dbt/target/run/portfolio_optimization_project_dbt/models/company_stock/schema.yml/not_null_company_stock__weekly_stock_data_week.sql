select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select week
from "company_stock"."public"."company_stock__weekly_stock_data"
where week is null



      
    ) dbt_internal_test