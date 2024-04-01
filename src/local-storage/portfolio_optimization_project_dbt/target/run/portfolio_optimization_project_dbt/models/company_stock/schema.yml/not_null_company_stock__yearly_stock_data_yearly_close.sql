select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select yearly_close
from "company_stock"."public"."company_stock__yearly_stock_data"
where yearly_close is null



      
    ) dbt_internal_test