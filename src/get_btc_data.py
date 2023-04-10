import yfinance as yf
import datetime

start_date = datetime.datetime(2010, 1, 1)
end_date = datetime.datetime.now()

df = yf.download('BTC-USD', start=start_date, end=end_date)
df['Return'] = df['Adj Close'].pct_change()
df = df.dropna()

# Save the data to a CSV file
df.to_csv('btc_data.csv')
