select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select month_start_date
from "company_stock"."public"."company_stock__monthly_stock_data"
where month_start_date is null



      
    ) dbt_internal_test