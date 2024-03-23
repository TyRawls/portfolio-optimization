"""
File: lambda_function.py (cloud deployment)
Author: Ty Rawls
Date: 2024-03-07
Description: When new stock data arrives in the AWS S3 bucket, it triggers AWS Lambda to send 
the data to AWS RDS (PostgreSQL).
"""

import io
import os
import csv
import boto3
import psycopg2

# Initialize the S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(f'Printing event info: {event}')
    
    # Retrieve S3 bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Display bucket name and key from event
    print(f'S3 Bucket Name: {bucket}')
    print(f'S3 Key (Filename): {key}')

    # Connect to AWS RDS - PostgreSQL instance
    conn = psycopg2.connect(
        dbname   = os.environ.get('DBNAME'),
        user     = os.environ.get('USER'),
        password = os.environ.get('PASS'),
        host     = os.environ.get('HOST'),
        port     = os.environ.get('PORT'),  # Default PostgreSQL port
        connect_timeout = 30                # Set timeout to 30 seconds
    )
    # Create a cursor object to execute queries
    cursor = conn.cursor()
    
    # Download file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    csv_reader = csv.reader(io.StringIO(data))
    next(csv_reader) # Skip the header row
    
    # If new data has been pushed to the 'stock-info' folder in the S3 bucket, 
    # then insert data into the 'company_info' table in the database
    if 'stock-info' in key:
        for row in csv_reader:
            # Construct the SQL INSERT statement for the 'company_info' table
            insert_query = 'INSERT INTO company_info (ticker, company_name, exchange, ceo, sector, industry, market_cap) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            
            # Execute the INSERT statement with the current row data
            cursor.execute(insert_query, row)
    else:
        print('This event does not contain data for the company_info table.')
            
      
    # If new data has been pushed to the 'stock-price' folder in the S3 bucket,     
    # then insert data into the 'daily_stock_price' table in the database
    if 'stock-price' in key:
        for row in csv_reader:
            # Construct the SQL INSERT statement for the 'daily_stock_info' table
            insert_query = 'INSERT INTO daily_stock_data (date, ticker, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            
            # Execute the INSERT statement with the current row data
            cursor.execute(insert_query, row)
    else:
        print('This event does not contain data for the daily_stock_data table.')

           
    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()