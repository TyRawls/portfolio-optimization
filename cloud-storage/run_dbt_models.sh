# File: run_dbt_models.sh (cloud deployment)
# Author: Ty Rawls
# Date: 2024-03-21
# Description: Updates the dbt models in AWS RDS (PostgreSQL), ensuring that the data remains current 
# and accurately reflects the latest market information. This procedure is initialized by the 'fetch' 
# function located in 'app.py'.

echo
echo "-------- PROCESS STARTED: UPDATING DBT MODELS --------"
echo

# Create and update dbt models in the database    
cd portfolio_optimization_project_dbt # Change to dbt project directory
dbt debug                             # Check to ensure connections are setup properly
dbt clean                             # Delete the dbt_packages and target directories
dbt run                               # Run dbt models
dbt test                              # Test models

echo
echo "-------- PROCESS COMPLETED: UPDATED DBT MODELS --------"
echo