select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select year
from "company_stock"."public"."company_stock__yearly_stock_data"
where year is null



      
    ) dbt_internal_test