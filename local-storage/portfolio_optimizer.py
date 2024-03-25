"""
File: portfolio_optimizer.py (cloud deployment)
Author: Ty Rawls
Date: 2024-03-17
Description: Retrieves information from the database and conducts Mean Variance Optimization (MVO) to enhance 
a portfolio according to the specified portfolio settings received through the Streamlit application.
"""

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from utils import read_stock_database
from scipy.optimize import minimize, LinearConstraint


def create_returns_dataframe(df, tickers):
    # Create a DataFrame with the stock returns for each stock ticker
    data = {}
    returns_grouped = df.groupby('ticker')['returns']
    
    for ticker in tickers:
        data[ticker] = returns_grouped.get_group(ticker).reset_index(drop=True)
        
    return pd.DataFrame(data)


# Objective functions for performing mean variance optimization (MVO)
def portfolio_return(weights, returns):
    return np.dot(returns, weights)

def portfolio_volatility(weights, returns):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))


# Perform mean variance optimization (MVO) to obtain optimal asset weights
def mean_variance_optimization(num_simulations, returns, mean_returns, risk_free_rate=0.0, 
                               allow_shorting=False, maximize_returns=True):
    num_assets = returns.shape[1]

    def objective_function(weights):
        if maximize_returns:  
            # Maximize returns: minimize negative returns
            return -((portfolio_return(weights, mean_returns) - risk_free_rate) / portfolio_volatility(weights, returns))
        else:
            # Minimize risk
            return portfolio_volatility(weights, returns)  
        
    if maximize_returns:
        # Set method and contraints for maximizing returns
        method='SLSQP'
        
        # Define optimization constraints: Sum of weights must be 1.
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  
    else:
        # Set method and contraints for minimizing risk
        method='trust-constr'
        
        # Set the constraint that the sum of weights equals 1.
        constraint_matrix = np.ones((1, num_assets))
        constraints = LinearConstraint(constraint_matrix, [1], [1])        
        
    if allow_shorting:
        # Allow shorting by setting bounds to (-1, 1)
        bounds = tuple((-1, 1) for _ in range(num_assets))  
    else:
        # Disallow shorting by setting bounds to (0, 1)
        bounds = tuple((0, 1) for _ in range(num_assets))
          
    # Initialize variables
    port_returns         = np.zeros(num_simulations)
    port_risks           = np.zeros(num_simulations)
    sharpe_ratios        = np.zeros(num_simulations)
    optimal_weights_list = np.zeros((num_simulations, num_assets))

    for i in range(num_simulations):
        # Generate random initial weights
        weights = np.random.rand(num_assets)
        weights /= np.sum(weights)  # Normalize to ensure the sum is 1

        # Expected portfolio return
        port_returns[i] = portfolio_return(weights, mean_returns)
    
        # Expected portfolio risk (standard deviation)
        port_risks[i] = portfolio_volatility(weights, returns)
        
        # Sharpe Ratio
        sharpe_ratios[i] = (port_returns[i] - risk_free_rate) / port_risks[i]
        
        # Perform optimization
        result = minimize(objective_function, weights, method=method, 
                          bounds=bounds, constraints=constraints)
        optimal_weights_list[i, :] = result.x

    return port_returns, port_risks, sharpe_ratios, optimal_weights_list


# Displays the asset allocation results of the MVO
def asset_allocation(tickers, maximize_returns, allow_shorting, 
                     max_sharpe_ratio_return, max_sharpe_ratio_risk, max_sharpe_ratio_weights,
                     min_port_risk_Y, min_port_risk_X, min_port_risk_weights):
    # Maximize return with shorting disallowed
    if maximize_returns and not allow_shorting:        
        return max_sharpe_ratio_return, max_sharpe_ratio_risk, tickers, max_sharpe_ratio_weights
            
    # Maximize return with shorting allowed
    elif maximize_returns and allow_shorting:
        return max_sharpe_ratio_return, max_sharpe_ratio_risk, tickers, max_sharpe_ratio_weights
    
    # Minimize risk with shorting disallowed
    elif not maximize_returns and not allow_shorting:
        return min_port_risk_Y, min_port_risk_X, tickers, min_port_risk_weights
          
    # Minimize risk with shorting allowed
    elif not maximize_returns and allow_shorting:
        return min_port_risk_Y, min_port_risk_X, tickers, min_port_risk_weights
    

def optimize(tickers, risk_free_rate, allow_shorting, maximize_returns):
    try:
        # Convert tickers to a list if it's not already in list format
        tickers = tickers.split(', ')
    except AttributeError:
        None
        
    num_simulations  = 10000   # Number of simulations
    
    # Read stock data from the database
    info_df, price_df = read_stock_database('monthly')
    
    # Create a new column with the calculated stock returns
    price_df['returns'] = price_df.groupby('ticker')['monthly_close'].pct_change()
    price_df = price_df.fillna(value=price_df['returns'].mean())
   
    # Create a Dataframe with only the returns for each ticker
    returns_df = create_returns_dataframe(price_df, tickers)

    # Calculate annualized average return for each stock
    # Annualized average return = monthly average return * 12 months
    mean_returns = np.mean(returns_df, axis=0) * 12
    covariance_matrix = returns_df.cov()
    
    # Perform MVO simulation
    port_returns, port_risks, sharpe_ratios, optimal_weights_list =\
        mean_variance_optimization(num_simulations, returns_df, mean_returns, 
                                   risk_free_rate=risk_free_rate, 
                                   allow_shorting=allow_shorting, 
                                   maximize_returns=maximize_returns)
    
    # Find the portfolio with the highest sharpe ratio
    max_sharpe_ratio_idx     = np.argmax(sharpe_ratios) 
    max_sharpe_ratio_return  = port_returns[max_sharpe_ratio_idx]
    max_sharpe_ratio_risk    = port_risks[max_sharpe_ratio_idx]
    max_sharpe_ratio_weights = optimal_weights_list[max_sharpe_ratio_idx, :]
    
    # Find the portfolio with the lowest risk (volatility)
    min_port_risk_idx     = np.argmin(port_risks) 
    min_port_risk_X       = port_risks[min_port_risk_idx]
    min_port_risk_Y       = port_returns[min_port_risk_idx]
    min_port_risk_weights = optimal_weights_list[min_port_risk_idx, :]
     
    # Points for the Capital Allocation Line (CAL)
    cal_points       = np.zeros((2, 2))     
    cal_points[0, :] = [0, risk_free_rate]  
    cal_points[1, :] = [max_sharpe_ratio_risk, max_sharpe_ratio_return]
        
    # Create traces for each set of data points
    # Plot configurations for portfolios
    portfolios = go.Scatter(
        x=port_risks,
        y=port_returns,
        mode='markers',
        marker=dict(
            color=sharpe_ratios,   
            colorscale='Viridis',  
            colorbar=dict(title='Sharpe Ratio'), 
            size=10,
            showscale=True  
        ),
        name='Portfolios',
    )

    # Plot configurations for max sharpe ratio
    max_sharpe_ratio = go.Scatter(
        x=[max_sharpe_ratio_risk],
        y=[max_sharpe_ratio_return],
        mode='markers',
        marker=dict(symbol='star', color='red', size=15,
                    line=dict(width=2, color='DarkSlateGrey')),
        name='Max Sharpe Ratio Portfolio',
    )

    # Plot configurations for the minimum portfolio risk
    min_port_risk = go.Scatter(
        x=[min_port_risk_X],
        y=[min_port_risk_Y],
        mode='markers',
        marker=dict(symbol='star', color='orange', size=15,
                    line=dict(width=2, color='DarkSlateGrey')),
        name='Minimum Risk Portfolio',
    )

    # Plot configurations for the risk-free asset
    risk_free_asset = go.Scatter(
        x=[0],
        y=[risk_free_rate],
        mode='markers',
        marker=dict(symbol='square', color='blue', size=12,
                    line=dict(width=2, color='DarkSlateGrey')),
        name='Risk-Free Asset',
    )

    # Plot configurations for the Captial Allocation Line (CAL)
    cal = go.Scatter(
        x=cal_points[:, 0],
        y=cal_points[:, 1],
        mode='lines',
        line=dict(dash='dash', color='green'),
        name='Capital Allocation Line (CAL)',
    )

    # Plot configurations for max returns per asset
    max_returns = mean_returns
    max_risks = np.sqrt(np.diagonal(covariance_matrix)) 

    max_return_per_asset = go.Scatter(
        x=max_risks,
        y=max_returns,
        mode='markers',
        text=tickers,
        textposition='top right',
        textfont=dict(size=12, color='black'), 
        marker=dict(symbol='diamond', color='lime', size=15, 
                    line=dict(width=2, color='green')),
        name='Max Return per Asset',
    )

    # Create annotations for each max return per asset
    annotations = []
    for i in range(len(tickers)):
        annotations.append(
            dict(
                x=max_risks[i],
                y=max_returns[i],
                xref='x',
                yref='y',
                text=f'<b>{tickers[i]}</b>',
                showarrow=True,
                arrowhead=2,
                ax=20,
                ay=-30,
                font=dict(
                    family='Arial',
                    color='red',  
                    size=15,    
                )
            )
        )

    # Create a figure object with the traces
    fig = go.Figure([portfolios, max_sharpe_ratio, min_port_risk, risk_free_asset, 
                     cal, max_return_per_asset], layout=dict(annotations=annotations))
    
    # Customize plot layout
    fig.update_layout(
        title=dict(text="<b>Markowitz’s Efficient Frontier Using Sharpe Ratio and Capital Allocation Line (CAL)</b>",
                   font=dict(size=20)),
        title_x=0.5,     # Center title horizontally
        xaxis_title='Portfolio Risk (Volatility)',
        yaxis_title='Portfolio Return',
        legend=dict(
            x=0.01,  # Set the horizontal position of the legend
            y=0.99,  # Set the vertical position of the legend
            bgcolor='rgba(255, 255, 255, 0.7)',   # Set the background color of the legend box
            bordercolor='rgba(0, 0, 0, 0.5)',     # Set the border color of the legend box
            borderwidth=1                         # Set the border width of the legend box
        )
    )
    
    # Get stock returns, risk, tickers, and weights    
    ret, rsk, tkrs, wts =\
          asset_allocation(tickers, maximize_returns, allow_shorting, 
                           max_sharpe_ratio_return, max_sharpe_ratio_risk, 
                           max_sharpe_ratio_weights, min_port_risk_Y, 
                           min_port_risk_X, min_port_risk_weights)
    
    return ret, rsk, tkrs, wts, fig