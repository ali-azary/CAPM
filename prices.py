# import libraries
from itertools import islice
import yfinance as yf
import concurrent.futures
import pandas as pd
from yahoo_fin.stock_info import tickers_sp500

# function to get market cap for a stock
def fetch_market_cap(ticker):
    info = yf.Ticker(ticker).info
    return (ticker, info['marketCap'])

# function to get market caps and sort from high to low
def get_top_market_caps(tickers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_market_cap, ticker) for ticker in tickers]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    sorted_dict = dict(sorted(results, key=lambda x: x[1], reverse=True))
    return sorted_dict

# get s&p 500 stocks and the top 100 with highest market caps
tickers = tickers_sp500()
sorted_dict=get_top_market_caps(tickers)
top=['^GSPC']
for ticker, market_cap in islice(sorted_dict.items(), 10):
    top.append(ticker)


# download  price history 
prices=pd.DataFrame(columns=['date'])
start_date = "2017-01-01"
ticker=top[0]
data = yf.download(ticker, start=start_date)
prices['date'] = data.index
prices.set_index('date', inplace=True)
for ticker in top:
    data = yf.download(ticker, start=start_date)
    prices[ticker] = data['Close']

# clean the data and write to csv file
prices = prices.dropna(axis=1)
prices.to_csv('prices.csv')

