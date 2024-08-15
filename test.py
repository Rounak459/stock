import sys
if sys.platform.startswith("win"):
    import os
    os.system('pip install pywin32')
import os
os.system('pip install --upgrade pip')

import os
os.system('pip install yfinance')

import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import requests
import datetime
from bs4 import BeautifulSoup

# Function to fetch historical stock data and calculate moving averages
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            st.error(f"No data found for symbol: {symbol}")
            return None

        # Calculate moving averages
        stock_data['100MA'] = stock_data['Close'].rolling(window=100).mean()
        stock_data['200MA'] = stock_data['Close'].rolling(window=200).mean()
        
        return stock_data
    except Exception as e:
        st.error(f"Error fetching data for symbol {symbol}: {e}")
        return None

# Function to plot line graph for closing price
def plot_closing_price(stock_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title='Closing Price Over Time',
                      xaxis_title='Date',
                      yaxis_title='Price')
    return fig

# Function to plot line graph for 100-day moving average
def plot_100ma(stock_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['100MA'], mode='lines', name='100-day MA'))
    fig.update_layout(title='100-day Moving Average Over Time',
                      xaxis_title='Date',
                      yaxis_title='Price')
    return fig

# Function to plot line graph for 200-day moving average
def plot_ma(stock_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['100MA'], mode='lines', name='100-day MA'))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['200MA'], mode='lines', name='200-day MA'))
    fig.update_layout(title='Moving Average Over Time',
                      xaxis_title='Date',
                      yaxis_title='Price')
    return fig

# Function to plot candlestick chart
def plot_candlestick(stock_data):
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'])])
    fig.update_layout(title='Candlestick Chart',
                      xaxis_title='Date',
                      yaxis_title='Price')
    return fig

# Function to display company description
def display_company_description(symbol):
    try:
        company = yf.Ticker(symbol)
        info = company.info
        st.subheader('Company Description')
        st.write(info['longBusinessSummary'])
    except:
        st.error('Could not retrieve company information.')

# Function to fetch financial statements for a company
def fetch_financial_statements(symbol):
    try:
        ticker = yf.Ticker(symbol)
        balance_sheet = ticker.balance_sheet
        income_statement = ticker.financials
        cash_flow_statement = ticker.cashflow
        return balance_sheet, income_statement, cash_flow_statement
    except Exception as e:
        st.error(f"Error fetching financial statements: {e}")
        return None, None, None

# Function to fetch fundamental data
def fetch_fundamental_data(symbol):
    try:
        company = yf.Ticker(symbol)
        info = company.info
        return info
    except Exception as e:
        print("Error fetching fundamental data:", e)
        return None

# Function to fetch latest news related to the stock symbol
def fetch_stock_news(symbol, api_key):
    url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        return news_data['articles']
    else:
        st.error('Failed to fetch news articles.')
        return []
    
    # Function to get recent view stocks (can be implemented as a list or from a database)
## Function to get recent view stocks and their prices
def get_recent_view_stocks():
    # Static list of recently viewed stocks for demonstration
    recent_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    
    # Fetch the latest price and calculate the percentage change for each stock
    recent_stocks_data = []
    for symbol in recent_symbols:
        stock = yf.Ticker(symbol)
        history = stock.history(period="2d")  # Fetch last two days of data to calculate change
        if len(history) >= 2:
            current_price = history['Close'].iloc[-1]
            previous_price = history['Close'].iloc[-2]
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100
            recent_stocks_data.append({
                "Symbol": symbol, 
                "Price": current_price, 
                "Change": price_change, 
                "Percent Change": percent_change
            })
    
    return recent_stocks_data

# Function to fetch top gainers
def get_top_gainers():
    url = "https://finance.yahoo.com/gainers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 gainers

# Function to fetch top losers
def get_top_losers():
    url = "https://finance.yahoo.com/losers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 losers

# Function to fetch most active stocks
def get_most_active():
    url = "https://finance.yahoo.com/most-active"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 most active stocks

# Function to fetch trending tickers
def get_trending_tickers():
    url = "https://finance.yahoo.com/trending-tickers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 trending tickers

# Function to fetch market data for regions, rates, and commodities
def get_market_data(region):
    # Placeholder function - replace with actual data fetching logic
    data = {
        "Europe": ["FTSE 100", "DAX", "CAC 40"],
        "US": ["Dow Jones", "S&P 500", "NASDAQ"],
        "Asia": ["Nikkei", "Hang Seng", "Shanghai Composite"]
    }
    return data.get(region, [])

# Function to fetch top stocks from different regions
def get_market_top_stocks(region):
    # URLs for different regions
    urls = {
        "US": "https://finance.yahoo.com/most-active?offset=0&count=5",
        "Europe": "https://finance.yahoo.com/screener/unsaved/360b66d7-64b8-401b-bdf2-8702657e517b?offset=0&count=5",
        "Asia": "https://finance.yahoo.com/screener/unsaved/2c6c9f43-e7e8-49d6-832f-8d66a124de3c?offset=0&count=5"
    }

    response = requests.get(urls[region])
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 stocks

# Function to fetch rates and commodities data
def get_rates_and_commodities():
    url = "https://finance.yahoo.com/commodities"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df.head(5)  # Top 5 commodities



# Main function
def main():
    st.image("v1.png", width=500)
    st.title('Stock Market Analysis')

    home, pricing_data, fundamental, news = st.tabs(["Home", "Pricing Data", "Fundamental", "News"]) 

    symbol = st.sidebar.text_input('Enter Stock Symbol (e.g., AAPL)', value='')
    today = datetime.date.today()
    duration = st.sidebar.number_input('Enter the duration in days', value=0)
    start_date = st.sidebar.date_input('Enter Start Date', value=today - datetime.timedelta(days=duration))
    end_date = st.sidebar.date_input('End Date', value=today)

     ## Sidebar for additional stock market information
    st.sidebar.subheader("Recent Viewed Stocks")
    recent_stocks = get_recent_view_stocks()
    for stock in recent_stocks:
        st.sidebar.write(f"{stock['Symbol']}: ${stock['Price']:.2f} ({stock['Percent Change']:+.2f}%)")


    st.sidebar.subheader("Top Gainers")
    top_gainers = get_top_gainers()
    st.sidebar.dataframe(top_gainers)

    st.sidebar.subheader("Top Losers")
    top_losers = get_top_losers()
    st.sidebar.dataframe(top_losers)

    st.sidebar.subheader("Most Active")
    most_active = get_most_active()
    st.sidebar.dataframe(most_active)

    st.sidebar.subheader("Trending Tickers")
    trending_tickers = get_trending_tickers()
    st.sidebar.dataframe(trending_tickers)

    # Market top stocks by region
    st.sidebar.subheader("Top Stocks by Region")

    st.sidebar.write("**US Market**")
    us_stocks = get_market_top_stocks("US")
    st.sidebar.dataframe(us_stocks)

    st.sidebar.write("**European Market**")
    europe_stocks = get_market_top_stocks("Europe")
    st.sidebar.dataframe(europe_stocks)

    st.sidebar.write("**Asian Market**")
    asia_stocks = get_market_top_stocks("Asia")
    st.sidebar.dataframe(asia_stocks)

    # Rates and commodities
    st.sidebar.subheader("Rates and Commodities")
    rates_commodities = get_rates_and_commodities()
    st.sidebar.dataframe(rates_commodities)


    
    if symbol:
        stock_data = get_stock_data(symbol, start_date, end_date)
        if stock_data is not None:
            with home:
                st.subheader('Closing Price Over Time')
                closing_price_fig = plot_closing_price(stock_data)
                st.plotly_chart(closing_price_fig)
                display_company_description(symbol)

            with pricing_data:
                st.subheader('100-day Moving Average Over Time')
                ma_100_fig = plot_100ma(stock_data)
                st.plotly_chart(ma_100_fig)
                
                st.subheader('100 & 200-day Moving Average Over Time')
                ma_fig = plot_ma(stock_data)
                st.plotly_chart(ma_fig)

                st.subheader('Candlestick Chart')
                candlestick_fig = plot_candlestick(stock_data)
                st.plotly_chart(candlestick_fig)

            with fundamental:
                st.header('Price Movements')
                stock_data2 = stock_data.copy()
                stock_data2['% Change'] = stock_data['Close'].pct_change()
                stock_data2.dropna(inplace=True)
                st.write(stock_data2)
                annual_return = stock_data2['% Change'].mean() * 252 * 100
                st.write('Annual Return is: ', annual_return, '%')
                stdev = np.std(stock_data2['% Change']) * np.sqrt(252)
                st.write('Standard Deviation is:', stdev * 100, '%')
                st.write('Risk-Adjusted Return is:', annual_return / (stdev * 100))

                balance_sheet, income_statement, cash_flow_statement = fetch_financial_statements(symbol)
                if balance_sheet is not None and income_statement is not None and cash_flow_statement is not None:
                    st.subheader(f'Financial Statements for {symbol}')
                    st.write('Balance Sheet:')
                    st.write(balance_sheet)
                    st.write('Income Statement:')
                    st.write(income_statement)
                    st.write('Cash Flow Statement:')
                    st.write(cash_flow_statement)
                else:
                    st.error("Failed to fetch financial statements.")

            with news:
                st.header('Latest News')
                api_key = 'fac762d216484fe2aad76f0234aca2b5'  # Replace with your actual NewsAPI key
                news_articles = fetch_stock_news(symbol, api_key)
                for article in news_articles:
                    st.subheader(article['title'])
                    st.write(article['description'])
                    if article['urlToImage']:
                        st.image(article['urlToImage'], width=400)
                    st.write(f"[Read more]({article['url']})")
        else:
            st.error(f"Failed to retrieve data for {symbol}. Please check the stock symbol.")
    else:
        st.info("Please enter a stock symbol in the sidebar.")

if __name__ == "__main__":
    main()
