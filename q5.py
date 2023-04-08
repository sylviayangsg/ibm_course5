import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="1y")

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

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

fig.add_trace(
    go.Scatter(x=tesla_data.index, y=tesla_data['Close'], name="Close"),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=last_year_revenue.index,
           y=last_year_revenue['Revenue'], name="Revenue"),
    row=2, col=1
)

fig.update_layout(
    height=600,
    title_text="Tesla Stock and Revenue Dashboard",
    xaxis_rangeslider_visible=False,
    showlegend=True,
    legend=dict(x=0, y=1.1, orientation='h'),
    plot_bgcolor='rgb(230, 230,230)',
    yaxis=dict(title="Closing Price"),
    yaxis2=dict(title="Revenue", tickprefix="$")
)

fig.show()
