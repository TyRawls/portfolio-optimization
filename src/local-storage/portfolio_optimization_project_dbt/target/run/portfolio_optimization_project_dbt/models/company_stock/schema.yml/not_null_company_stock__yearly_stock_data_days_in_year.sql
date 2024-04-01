select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select days_in_year
from "company_stock"."public"."company_stock__yearly_stock_data"
where days_in_year is null



      
    ) dbt_internal_test