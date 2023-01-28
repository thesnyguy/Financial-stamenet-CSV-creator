import requests
import pandas as pd
from pandas import json_normalize

# Prompt the user for Alpha Vantage API Key
api_key = input("Enter Alpha Vantage API Key: ")

# Define a function to retrieve financial data from the Alpha Vantage API
def financial_data(ticker, function):
    base_url = 'https://www.alphavantage.co/query?'
    symbol = ticker
    url = base_url + 'function=' + function + '&symbol=' + symbol + '&apikey=' + api_key
    response = requests.get(url)
    data = response.json()
    return data

# Prompt the user for a ticker symbol and a list of finance type functions to retrieve data for
ticker = input("Enter a Ticker symbol: ")
functions = ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']

# Loop through functions and retrieve financial data
for function in functions:
    data = financial_data(ticker, function)
    if 'Error Message' in data:
        print(f"{function} - {data['Error Message']}")
    else:
        print(f"{function} data retrieved")
        
        # Normalize annual and quarterly reports data into Pandas DataFrames
        annual_df = json_normalize(data['annualReports'])
        if 'date' in annual_df.columns:
            annual_df.set_index("date", inplace=True)
        annual_df.sort_index(inplace=True)
        
        quarterly_df = json_normalize(data['quarterlyReports'])
        if 'date' in quarterly_df.columns:
            quarterly_df.set_index("date", inplace=True)
        quarterly_df.sort_index(inplace=True)
        
        combined_df = pd.concat([annual_df, pd.Series([""]), quarterly_df])
        combined_df = combined_df.transpose()
        combined_df.to_csv(f"{ticker}_{function}.csv", index=True)
        print(f'Data written to {ticker}_{function}.csv')
    
input("Press Enter to quit the program...")
