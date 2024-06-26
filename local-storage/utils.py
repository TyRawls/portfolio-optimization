"""
File: utils.py (local deployment)
Author: Ty Rawls
Date: 2024-03-07
Description: This application interfaces with the yFinance and Financial Marketing Prep (FMP) APIs to retrieve stock data, 
subsequently storing it in an staging folder for onward transmission to the PostgreSQL database.
"""

import os
import ssl
import json
import psycopg2
import subprocess
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import date


def create_directories(directory):
    # Create directories for the storage of stock price and company info data.
    info_dir       = directory + '/stock-info'
    price_dir      = directory + '/stock-price'
    info_staging   = info_dir + '/staging'
    price_staging  = price_dir + '/staging'
    info_archived  = info_dir + '/archived'
    price_archived = price_dir + '/archived'
    
    Path(info_dir).mkdir(parents=True, exist_ok=True)
    Path(info_dir).mkdir(parents=True, exist_ok=True)
    Path(info_staging).mkdir(parents=True, exist_ok=True)
    Path(price_staging).mkdir(parents=True, exist_ok=True)
    Path(info_archived).mkdir(parents=True, exist_ok=True)
    Path(price_archived).mkdir(parents=True, exist_ok=True)
    
    return info_dir, price_dir, info_staging, price_staging, info_archived, price_archived

def read_stock_database(interval='daily'):      
  # Connect to the the local PostgreSQL database
    conn = psycopg2.connect(
        dbname   = os.environ.get('LOCAL_DBNAME'),
        user     = os.environ.get('LOCAL_USER'),
        password = os.environ.get('LOCAL_PASS'),
        host     = os.environ.get('LOCAL_HOST'),
        port     = os.environ.get('LOCAL_PORT'),  # Default PostgreSQL port 
        connect_timeout = 30                      # Set timeout to 30 seconds
    )

    # Create a cursor object to execute queries
    cur = conn.cursor()
    
    # Define schema for the company info DataFrame.
    info_schema = {
              'ticker': 'str',
        'company_name': 'str',
            'exchange': 'str',
                 'ceo': 'str',
              'sector': 'str',
            'industry': 'str',
          'market_cap': 'int64',
         'ingested_at': 'datetime64[ns]',
    }
    
    # Set column names for company info
    info_cols = ['ticker', 'company_name', 'exchange', 'ceo', 'sector', 'industry', 'market_cap', 'ingested_at']

    # Query company info table, fetch all rows from the result set, and create DataFrame
    cur.execute('SELECT * FROM company_info')
    rows = cur.fetchall()
    info_df = pd.DataFrame(rows, columns=info_cols).astype(info_schema)
    
    if interval == 'daily':
        # Define schema for the stock price DataFrame.
        price_schema = {
                   'date': 'datetime64[ns]',
                 'ticker': 'str',
                   'open': 'float64',
                   'high': 'float64',
                    'low': 'float64',
                  'close': 'float64',
                 'volume': 'int64',
            'ingested_at': 'datetime64[ns]',
        }
        
        # Set column names for stock price data
        price_cols = ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume', 'ingested_at']
        
        # Query daily stock table, fetch all rows from the result set, and create DataFrame
        cur.execute('SELECT * FROM daily_stock_data')
        
    elif interval == 'weekly':
        # Define schema for the stock price DataFrame.
        price_schema = {
                       'week': 'int64',
            'week_start_date': 'datetime64[ns]',
              'week_end_date': 'datetime64[ns]',
               'days_in_week': 'int64',
                     'ticker': 'str',
                'weekly_open': 'float64',
                'weekly_high': 'float64',
                 'weekly_low': 'float64',
               'weekly_close': 'float64',
              'weekly_volume': 'int64',
        }
        
        # Set column names for stock price data
        price_cols = ['week', 'week_start_date', 'week_end_date', 'days_in_week', 
                      'ticker', 'weekly_open', 'weekly_high', 'weekly_low', 
                      'weekly_close', 'weekly_volume']
        
        # Query weekly stock table, fetch all rows from the result set, and create DataFrame
        cur.execute('SELECT * FROM company_stock__weekly_stock_data')

    elif interval == 'monthly':
        # Define schema for the stock price DataFrame.
        price_schema = {
                       'month': 'int64',
            'month_start_date': 'datetime64[ns]',
              'month_end_date': 'datetime64[ns]',
               'days_in_month': 'int64',
                      'ticker': 'str',
                'monthly_open': 'float64',
                'monthly_high': 'float64',
                 'monthly_low': 'float64',
               'monthly_close': 'float64',
              'monthly_volume': 'int64',
        }
        
        # Set column names for stock price data
        price_cols = ['month', 'month_start_date', 'month_end_date', 'days_in_month', 
                      'ticker', 'monthly_open', 'monthly_high', 'monthly_low', 
                      'monthly_close', 'monthly_volume']
        
        # Query weekly stock table
        cur.execute('SELECT * FROM company_stock__monthly_stock_data')
  
    elif interval == 'quarterly':
        # Define schema for the stock price DataFrame.
        price_schema = {
                       'quarter': 'int64',
            'quarter_start_date': 'datetime64[ns]',
              'quarter_end_date': 'datetime64[ns]',
               'days_in_quarter': 'int64',
                        'ticker': 'str',
                'quarterly_open': 'float64',
                'quarterly_high': 'float64',
                 'quarterly_low': 'float64',
               'quarterly_close': 'float64',
              'quarterly_volume': 'int64',
        }
        
        # Set column names for stock price data
        price_cols = ['quarter', 'quarter_start_date', 'quarter_end_date', 'days_in_quarter', 
                      'ticker', 'quarterly_open', 'quarterly_high', 'quarterly_low', 
                      'quarterly_close', 'quarterly_volume']
        
        # Query weekly stock table
        cur.execute('SELECT * FROM company_stock__quarterly_stock_data')    
        
    elif interval == 'yearly':
        # Define schema for the stock price DataFrame.
        price_schema = {
                       'year': 'int64',
            'year_start_date': 'datetime64[ns]',
              'year_end_date': 'datetime64[ns]',
               'days_in_year': 'int64',
                     'ticker': 'str',
                'yearly_open': 'float64',
                'yearly_high': 'float64',
                 'yearly_low': 'float64',
               'yearly_close': 'float64',
              'yearly_volume': 'int64',
        }
        
        # Set column names for stock price data
        price_cols = ['year', 'year_start_date', 'year_end_date', 'days_in_year', 
                      'ticker', 'yearly_open', 'yearly_high', 'yearly_low', 
                      'yearly_close', 'yearly_volume']
        
        # Query weekly stock table
        cur.execute('SELECT * FROM company_stock__yearly_stock_data')          
  
    # Fetch all rows from the result set, and create DataFrame
    rows = cur.fetchall()
    price_df = pd.DataFrame(rows, columns=price_cols).astype(price_schema)    
        
    # Close the cursor and connection
    cur.close()
    conn.close()
    
    return info_df, price_df

def get_info(ticker):
    # This function untilizes the Financial Modeling Prep (FMP) API to obtain 
    # company information about each stock ticker. Limited to 250 requests per day.    
    try:
        # For Python 3.0 and later
        from urllib.request import urlopen
    except ImportError:
        # Fall back to Python 2's urllib2
        from urllib2 import urlopen
    
    # Function to get company info
    def get_jsonparsed_data(url): 
        response = urlopen(url, context=ssl.create_default_context())
        data = response.read().decode("utf-8")
        return json.loads(data)
    
    # Set URL with API key to retrieve company info
    url = os.environ.get('FMP_API_URL') + ticker + os.environ.get('FMP_API_KEY')
    company_info = get_jsonparsed_data(url)
    
    return company_info


def get_last_ingested(directory, ticker):
    filenames = [] # Create an empty list
    
    # Get all filenames in the specified folder.
    for filename in os.listdir(directory):
        # Locate filenames that have the ticker.
        if ('_' + ticker + '_') in filename:
            # Add the filename to the list.
            filenames.append(filename)
    
    if filenames != []: 
        # Return the filenames if they exist for a specified ticker
        return filenames
    else:       
        return None


def get_historical_stock_data(tickers):
    # Get today's date (yyyymmdd).
    date_today = str(date.today()).replace("-", "")

    try:
        # Split tickers into a list.
        tickers_list = tickers.split(', ')
    except AttributeError:
        tickers_list = tickers
    
    # Create the final column format for the stock data.
    price_cols = ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']
    
    # Get current directory
    directory = os.getcwd() 
    
    try:
        # Pull all company info and stock data from the database, then convert them into a DataFrame
        info_df_db_all, price_df_db_all = read_stock_database()
        print('Successfully read data from the database.')
    except:
        print('Failed to read data from the database because it may not exist.\n'
              'Attempting to create database and tables now.')
        subprocess.run(['bash', 'db_init.sh'], check=True)
        print('Sucessfully created database and tables.')
        info_df_db_all, price_df_db_all = read_stock_database()

    # Create directories for the storage of stock price and company info data
    info_dir, price_dir, info_staging, price_staging, info_archived, price_archived = create_directories(directory)
    
    # Define schema for stock price and company info DataFrame.
    info_schema = {
              'ticker': 'str',
        'company_name': 'str',
            'exchange': 'str',
                  'ceo': 'str',
              'sector': 'str',
            'industry': 'str',
          'market_cap': 'int64',
    }
        
    price_schema = {
                'date': 'datetime64[ns]',
              'ticker': 'str',
                'open': 'float64',
                'high': 'float64',
                'low': 'float64',
              'close': 'float64',
              'volume': 'int64',
    }
        
    print('-------- PROCESS STARTED: SAVING FILES LOCALLY --------')
          
    for ticker in tickers_list:
        # Get stock price and company info data (DataFrame).
        ticker = ticker.lower()
        price_df_api = yf.download(ticker, rounding=True, period='10y')
        info = get_info(ticker)
        
        info_data = {
                  'ticker': [info[0]['symbol']],
            'company_name': [info[0]['companyName']],
                'exchange': [info[0]['exchangeShortName']],
                     'ceo': [info[0]['ceo']],
                  'sector': [info[0]['sector']],
                'industry': [info[0]['industry']],
              'market_cap': [info[0]['mktCap']]
        }
        
        info_df_api = pd.DataFrame(info_data).astype(info_schema)
        
        # The Date column is initially set as the index column when pulling from 
        # the yfinance API. This will move the current index (Date) into a 
        # column and reset the index to the default integer index.
        price_df_api.reset_index(inplace=True)
        
        # Removed the Adj Close column.
        # Note: This column was removed because with each pull from the API, the 
        # value was different which caused issues when comparing files that 
        # should be identical.
        price_df_api.drop('Adj Close', axis=1, inplace=True)
        
        # Add new column with ticker symbol and rearrange columns to make 
        # ticker the second column.
        price_df_api['ticker'] = ticker.upper()
        price_df_api.columns = price_df_api.columns.str.lower()
        
        price_df_api = price_df_api[price_cols]
        price_df_api = price_df_api.astype(price_schema)
        
        # Check to see if the ticker exists in the database
        if any(info_df_db_all['ticker'] == ticker.upper()):
            # If the ticker exists in the database, then filter to only show 
            # data from that ticker and drop the 'ingested_at' column
            print(f'{ticker.upper()} exists in the database. Retrieving data.')
            info_df_db = info_df_db_all[info_df_db_all['ticker'] == ticker.upper()].drop('ingested_at', axis=1)
            price_df_db = price_df_db_all[price_df_db_all['ticker'] == ticker.upper()].drop('ingested_at', axis=1)
            
            # Combine the ticker data from the database with the data pulled from 
            # the APIs. Compare them to only include data that is not already stored 
            # in the database.
            # Drop duplicate dates using 'df.drop_duplicates(subset=['date'])'
            info_df_merged = pd.merge(info_df_db, info_df_api, how='outer', indicator=True)
            info_df_api_new = info_df_merged[info_df_merged['_merge'] == 'right_only'].drop('_merge', axis=1)
            price_df_merged = pd.merge(price_df_db, price_df_api, how='outer', indicator=True)
            price_df_api_new = price_df_merged[price_df_merged['_merge'] == 'right_only'].drop('_merge', axis=1)
            
            try:
                # Search for duplicate dates in the price data
                dup_date = price_df_merged[price_df_merged.duplicated(subset=['date'])]['date'].iloc[0]
                
                # If there's a duplicate date, then exclude that row
                if dup_date:
                    price_df_api_new = price_df_api_new[price_df_api_new['date'] != dup_date]
            except:
                None
                
        else:
            print(f'{ticker.upper()} does not exists in the database.')
            info_df_api_new = info_df_api
            price_df_api_new = price_df_api     
            
        # If the new stock info DataFrame is not empty, then save as a CSV file to the staging folder
        if info_df_api_new.size != 0:
            counter = 0 # Counter index for filename

            # Set default filename and get the last ingested filenames from the archived folder for a specified ticker
            info_filename = 'api_' + date_today + '_' + ticker + '_info_' + str(counter) + '.csv'
            info_filenames = get_last_ingested(info_archived, ticker)
            
            try:
                # If the filename already exists, create a unique filename
                while info_filename in info_filenames:
                    counter += 1
                    info_filename = 'api_' + date_today + '_' + ticker + '_info_' + str(counter) + '.csv'
            except TypeError as e:
                print(f"{ticker.upper()} does not exist in the 'stock-info' folder: {e}")
            
            # Save stock info data to the staging folder as a CSV
            info_df_api_new.to_csv(info_staging + '/' + info_filename, index=False) 
            print(f"File saved in the 'stock-info/staging' folder as '{info_filename}'.")
        else:
            print(f'There is no new company info data for {ticker.upper()}.')
            
        # If the new stock price DataFrame is not empty, then save as a CSV file to the staging folder
        if price_df_api_new.size != 0:
            counter = 0 # Counter index for filename

            # Set default filename and get the last ingested filenames from the archived folder for a specified ticker
            price_filename = 'api_' + date_today + '_' + ticker + '_price_' + str(counter) + '.csv'
            price_filenames = get_last_ingested(price_archived, ticker)
            
            try:
                # If the filename already exists, create a unique filename
                while price_filename in price_filenames:
                    counter += 1
                    price_filename = 'api_' + date_today + '_' + ticker + '_price_' + str(counter) + '.csv'
            except TypeError as e:
                print(f"{ticker.upper()} does not exist in the 'stock-price' folder: {e}")
            
            # Save stock price data to the staging folder as a CSV
            price_df_api_new.to_csv(price_staging + '/' + price_filename, index=False) 
            print(f"File saved in the 'stock-price/staging' folder as '{price_filename}'.")
        else:
            print(f'There is no new stock price data for {ticker.upper()}.') 
                
    print('-------- PROCESS COMPLETED: SAVED FILES LOCALLY --------')

