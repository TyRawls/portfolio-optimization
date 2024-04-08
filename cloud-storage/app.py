"""
File: app.py (cloud deployment)
Author: Ty Rawls
Date: 2024-03-22
Description: This application interfaces with the yFinance and Financial Marketing Prep (FMP) APIs to retrieve stock data, 
subsequently storing it in an AWS S3 bucket for onward transmission to AWS RDS via AWS Lambda. Upon entry into the 
database, it triggers updates to the dbt models, ensuring that the data remains current and accurately reflects the latest 
market information. It also initates the Mean Variance Optimization (MVO) function to optimize a portfolio based upon the 
portfolio settings provided.
"""

import time
import subprocess
import pandas as pd
import streamlit as st
from utils import get_historical_stock_data
from portfolio_optimizer import optimize


@st.cache_data
def optimize_portfolio():
    # Display porfolio parameters chosen by the user
    st.write('\n')
    st.write('\n')
    st.write('Risk-Free Rate:', risk_free_rate)
    st.write('Shorting Allowed:', allow_shorting)
    st.write('Portfolio Optimization:', f"<h7 style='color: green;'>{strategy}</h7>", unsafe_allow_html=True)

    # Optimize the portfolio based upon the portfolio settings provided
    ret, rsk, tkrs, wts, fig = optimize(tickers, risk_free_rate, allow_shorting, maximize_returns)

    # Display the expected return, risk, and asset allocation percentage for each ticker
    st.write('Expected Return:', f"<h7 style='color: green;'>{ret*100:.2f}%</h7>", unsafe_allow_html=True)
    st.write('Risk:', f"<h7 style='color: green;'>{rsk*100:.2f}%</h7>", unsafe_allow_html=True)
    st.write('\n')
    st.write('<h7>--------------------------<br>Asset Allocation<br>--------------------------</h7>', unsafe_allow_html=True)
    for i in range(len(tkrs)):
        st.write(f'<h7>{tkrs[i]} : {wts[i]*100:.2f}%</h7>', unsafe_allow_html=True)
    
    # Display plot
    st.plotly_chart(fig)
  

def fetch():
    try:
        # Retrieve stock data 
        get_historical_stock_data(tickers)

        # Output a message if the database upload is successsful
        st.write("<h7 style='color: green;'>Database Upload Successful! :smile: :tada:</h7>", unsafe_allow_html=True) 

        # Run and update dbt models in the database
        time.sleep(10)  # Set a delay of 10 seconds
        subprocess.run(['bash', 'run_dbt_models.sh'], check=True)    
    except:
        # Output a message if the database upload failed
        st.write("<h7 style='color: red;'>Database Upload Failed! :cry:</h7>", unsafe_allow_html=True)

# Set title of application
st.markdown(
    '<h2 style="text-align: center;">Stock Data Ingestor & Portfolio Optimizer</h2>',
    unsafe_allow_html=True
)

# Horizontal divider used to underline the title
st.header('', divider='rainbow')

# Set user input prompts for ticker input
tickers = st.text_input('Please enter stock ticker(s) (Note: Separate each ticker with a comma and a single space):')
tickers = tickers.upper()

# Dropdown menu options
shorting_options = [False, True]
optimization_options = ['Maximize Returns', 'Minimize Risk']

# Sidebar portfolio input settings
st.sidebar.header('Database Settings')
db_checkbox_value = st.sidebar.checkbox('Update database ONLY')
st.write('\n')
st.sidebar.header('Portfolio Settings')
risk_free_rate = round(st.sidebar.number_input('Risk-Free Rate:', value=0.00), 2)
allow_shorting = st.sidebar.selectbox('Shorting Allowed:', shorting_options)
strategy = st.sidebar.selectbox('Portfolio Optimization:', optimization_options)

if strategy == 'Maximize Returns':
    maximize_returns = True
else:
    maximize_returns = False
    
# Routine for getting user ticker input manually
if st.button('Run - Manual Input'):
    if tickers.strip():
        # Display stock tickers
        st.write('\n')
        st.write('Tickers:', f"<h7 style='color: orange;'>{tickers}</h7>", unsafe_allow_html=True)

        # Retrieve stock data and store into the the database
        fetch()        
        
        if not db_checkbox_value:
            # Use stock data to create an optimized portfolio based on portfolio settings     
            optimize_portfolio()  
    else:
        # Output a message if the user failed to enter nay stock tickers
        st.write("<h7 style='color: red;'>No tickers detected. Please enter stock tickers.</h7>", unsafe_allow_html=True)

# Text divider
st.markdown(
    '<h3 style="text-align: center;"> - OR - </h3>',
    unsafe_allow_html=True
)

# File uploader for CSV files
file = st.file_uploader('Upload CSV', type=['csv'])

# Routine for getting user input via a CSV file
if st.button('Run - CSV File'):
    if file is not None:
        # Read CSV file and convert the 'ticker' column into a list
        df = pd.read_csv(file)
        tickers = df['ticker'].tolist()
        
        # Display the list of tickers from the CSV file
        st.write('\n')
        tickers_str = ', '.join(map(str, tickers))
        st.write('Tickers:', f"<h7 style='color: orange;'>{tickers_str}</h7>", unsafe_allow_html=True)

        # Retrieve stock data and store into the the database
        fetch()  

        if not db_checkbox_value:
            # Use stock data to create an optimized portfolio based on portfolio settings     
            optimize_portfolio() 
    else:
        # If there's no CSV file, display message informing user to upload a CSV file
        st.write("<h7 style='color: red;'>No CSV file detected. Please upload a CSV file.</h7>", unsafe_allow_html=True)