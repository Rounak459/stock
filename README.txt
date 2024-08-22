File Link:-https://nbviewer.org/github/Rounak459/stock/blob/main/test.py
Project Link:- https://stock-maket-analysis-by-rounakkhapre2402.streamlit.app/

# Stock Market Analysis Dashboard

This Streamlit-based web application provides users with comprehensive tools to analyze stock market data, including historical pricing, moving averages, financial statements, news, and market trends.

## Features

- **Stock Data Analysis**: Fetch historical stock data and calculate 100-day and 200-day moving averages.
- **Interactive Charts**: Visualize stock data using line graphs for closing prices, moving averages, and candlestick charts.
- **Company Information**: Display company descriptions and financial statements (balance sheet, income statement, cash flow).
- **Recent Stock Views**: Track and display recent stock views with their current prices and percentage changes.
- **Market Trends**: Display top gainers, losers, most active stocks, and trending tickers from the market.
- **Regional Market Data**: Show top-performing stocks from the US, Europe, and Asia markets.
- **Rates and Commodities**: Present top commodities and rate changes.
- **Latest News**: Fetch and display the latest news articles related to the entered stock symbol using the NewsAPI.

## How to Use

1. **Enter Stock Symbol**: Input the stock symbol (e.g., AAPL) in the sidebar.
2. **Set Date Range**: Select the start and end dates for fetching historical data.
3. **View Analysis**: Navigate through tabs to view pricing data, fundamental analysis, and the latest news.
4. **Market Overview**: Explore additional stock market information in the sidebar, including top gainers, losers, and more.

## Dependencies

- Python 3.x
- Streamlit
- Pandas
- NumPy
- Plotly
- yfinance
- requests
- BeautifulSoup

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo-name/stock-market-analysis-dashboard.git
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   stream lit run app.py
   ```

## API Keys

- To fetch the latest news, replace the placeholder `api_key` in the code with your actual NewsAPI key.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

This `README.txt` provides a clear overview of the application, its features, and how to use it.
