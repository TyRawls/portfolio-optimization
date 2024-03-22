# File: db_init.sh (cloud deployment)
# Author: Ty Rawls
# Date: 2024-03-07
# Description: Creates the 'company_stock' database as well as the 'company_info' and 
# 'daily_stock_price' tables. This procedure is initialized by the 'get_historical_stock_data' 
# function located in 'utils.py'.

echo
echo "-------- PROCESS STARTED: CREATING DATABASE --------"
echo

echo "PROCESS: Defining database connection parameters"
# Obtain the database connection parameters from the environment variables
source ~/.zshrc 

echo "PROCESS: Creating database and tables, if they do not exist"
# Create database and tables, if it does not exist
export PGPASSWORD=$PASS
createdb -h $HOST -p $PORT -U $USER $DBNAME                   # Create 'company_stock' database
psql -h $HOST -p $PORT -U $USER -d $DBNAME -f stock_data.sql  # Create 'company_info' and 'daily_stock_price' tables

unset $PASS
unset PGPASSWORD

echo
echo "-------- PROCESS COMPLETED: CREATED DATABASE --------"
echo