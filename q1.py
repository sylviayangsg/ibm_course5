import yfinance as yf

tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period="7d")

tesla_data.reset_index(inplace=True)

print(tesla_data.head(10))