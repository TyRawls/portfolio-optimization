# File: push_to_db.sh (local deployment)
# Author: Ty Rawls
# Date: 2024-03-07
# Description: Takes the 'company_info' and 'daily_stock_price' data from the local staging folder and 
# stores it into the database. Once stored in the database, it moves the data from the staging folder 
# to the archived folder. Upon entry into the database, it also triggers updates to the dbt models, ensuring 
# that the data remains current and accurately reflects the latest market information.

echo
echo "-------- PROCESS STARTED: PUSHING TO DATABASE --------"
echo
echo "PROCESS: Getting company info and historical stock data to store into staging folder"

echo "PROCESS: Defining database connection parameters"
# Define the database connection parameters
source ~/.portoptrc 

echo "PROCESS: Setting staging directory variables"
# Define staging folders for company info and stock price data
info_staging="stock-info/staging"      # Company info staging directory  
info_archived="stock-info/archived"    # Company info archived directory
info_filenames=("$info_staging"/*)     # List of file names in the staging directory

price_staging="stock-price/staging"    # Stock price staging directory 
price_archived="stock-price/archived"  # Stock price archived directory
price_filenames=("$price_staging"/*)   # List of file names in the staging directory

echo "PROCESS: Setting SQL commands for pushing data into the database"
INFO_TABLE="company_info"
PRICE_TABLE="daily_stock_data"

INFO_NEW_ROW_SQL_CMD="\COPY $INFO_TABLE (ticker, company_name, exchange, ceo, sector, industry, market_cap) FROM stdin WITH CSV HEADER DELIMITER E',';"
PRICE_NEW_ROW_SQL_CMD="\COPY $PRICE_TABLE (date, ticker, open, high, low, close, volume) FROM stdin WITH CSV HEADER DELIMITER E',';" 

echo "PROCESS: Pushing data into the company_info table"
# Iterate through the list of file names in the staging folder 
# for company info data and push each file to the database.
for file in "${info_filenames[@]}"; do
    if [ -f "$file" ]; then
        # Read the CSV file line by line
        echo "Processing file: $file"
        while IFS=, read -r ticker company_name exchange ceo sector industry market_cap; do
            # Check if the primary key already exists in the database
            QUERY="SELECT COUNT(*) FROM $INFO_TABLE WHERE ticker='$ticker';"
            RESULT=$(psql -h $LOCAL_HOST -p $LOCAL_PORT -U $LOCAL_USER -d $LOCAL_DBNAME -t -c "$QUERY")
        
            # Extract the count from the result
            COUNT=$(echo $RESULT | tr -d ' ')
            
            # If the primary key exists, update the corresponding row in the database
            if [[ "$COUNT" -gt 0 ]]; then
                TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
                psql -h $LOCAL_HOST -p $LOCAL_PORT -U $LOCAL_USER -d $LOCAL_DBNAME -c "UPDATE $INFO_TABLE SET company_name='$company_name', exchange='$exchange', ceo='$ceo', sector='$sector', industry='$industry', market_cap=$market_cap, ingested_at='$TIMESTAMP' WHERE ticker='$ticker'"
            fi
        done < "$file"
        # Push to company_info table in database
        cat $file | psql -h $LOCAL_HOST -p $LOCAL_PORT -U $LOCAL_USER -d $LOCAL_DBNAME -c "$INFO_NEW_ROW_SQL_CMD"
        echo "Moving $file from $info_staging to $info_archived"
        mv $file $info_archived   
    fi
done

echo "PROCESS: Pushing data into the daily_stock_data table"
# Iterate through the list of file names in the staging folder 
# for stock price data and push each file to the database.
for file in "${price_filenames[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        # Push to daily_stock_data table in database
        cat $file | psql -h $LOCAL_HOST -p $LOCAL_PORT -U $LOCAL_USER -d $LOCAL_DBNAME -c "$PRICE_NEW_ROW_SQL_CMD" 
        echo "Moving $file to archived folder"
        mv $file $price_archived 
    fi
done

echo
echo "-------- PROCESS COMPLETED: PUSHED TO DATABASE --------"
echo
echo
echo "-------- PROCESS STARTED: UPDATING DBT MODELS --------"
echo

# Create and update dbt models in the database    
cd portfolio_optimization_project_dbt  # Change to dbt project directory
dbt clean                               # Delete the dbt_packages and target directories
dbt run                                 # Run dbt models
dbt test                                # Test models

echo
echo "-------- PROCESS COMPLETED: UPDATED DBT MODELS --------"
echo
