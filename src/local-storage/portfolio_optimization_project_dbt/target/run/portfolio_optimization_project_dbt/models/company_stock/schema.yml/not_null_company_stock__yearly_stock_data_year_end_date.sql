select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select year_end_date
from "company_stock"."public"."company_stock__yearly_stock_data"
where year_end_date is null



      
    ) dbt_internal_test