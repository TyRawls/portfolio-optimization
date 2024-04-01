select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select ingested_at
from "company_stock"."public"."company_stock__daily_stock_data"
where ingested_at is null



      
    ) dbt_internal_test