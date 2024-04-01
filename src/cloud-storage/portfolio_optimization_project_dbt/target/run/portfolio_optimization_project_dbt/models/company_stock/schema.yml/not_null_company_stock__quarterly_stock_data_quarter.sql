select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quarter
from "company_stock"."public"."company_stock__quarterly_stock_data"
where quarter is null



      
    ) dbt_internal_test