import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

r = requests.get(url)

soup = BeautifulSoup(r.content)

table = soup.find_all('table')[1]
revenue_data = []

for row in table.tbody.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    revenue_data.append([ele for ele in cols if ele])

revenue_df = pd.DataFrame(revenue_data, columns=['Date', 'Revenue'])

revenue_df = revenue_df.drop([0, 1]).reset_index(drop=True)

revenue_df['Date'] = pd.to_datetime(revenue_df['Date'])
revenue_df.set_index('Date', inplace=True)


last_year_revenue = revenue_df.last('365D') 

print(last_year_revenue.head(10))