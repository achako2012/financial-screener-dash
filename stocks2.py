import pandas as pd

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go
import pandas_ta as ta
import plotly.express as px

# Clean data

# we need to skip first row with link
btceur_1h = pd.read_csv('data/BTCEUR_1h.csv', skiprows=1)
btceur_d = pd.read_csv('data/BTCEUR_d.csv', skiprows=1)
btcusd_1h = pd.read_csv('data/BTCUSD_1h.csv', skiprows=1)
btcusd_d = pd.read_csv('data/BTCUSD_d.csv', skiprows=1)
ethbtc_1h = pd.read_csv('data/ETHBTC_1h.csv', skiprows=1)
ethbtc_d = pd.read_csv('data/ETHBTC_d.csv', skiprows=1)
etheur_1h = pd.read_csv('data/ETHEUR_1h.csv', skiprows=1)
etheur_d = pd.read_csv('data/ETHEUR_d.csv', skiprows=1)

# Delete unnecassery columns
btceur_1h.drop(['unix', 'Volume BTC', 'Volume EUR'], axis=1, inplace=True)
btceur_d.drop(['unix', 'Volume BTC', 'Volume EUR'], axis=1, inplace=True)
btcusd_1h.drop(['unix', 'Volume BTC', 'Volume USD'], axis=1, inplace=True)
btcusd_d.drop(['unix', 'Volume BTC', 'Volume USD'], axis=1, inplace=True)
ethbtc_1h.drop(['unix', 'Volume ETH', 'Volume BTC'], axis=1, inplace=True)
ethbtc_d.drop(['unix', 'Volume ETH', 'Volume BTC'], axis=1, inplace=True)
etheur_1h.drop(['unix', 'Volume ETH', 'Volume EUR'], axis=1, inplace=True)
etheur_d.drop(['unix', 'Volume ETH', 'Volume EUR'], axis=1, inplace=True)

# print (btceur_1h['open'].isnull().sum())
# print (btceur_1h['close'].isnull().sum())
# print (btceur_1h['high'].isnull().sum())
# print (btceur_1h['low'].isnull().sum())

# print(btceur_1h.iloc[0])


app = Dash()

app.layout = html.Div([
    
    dcc.Dropdown(["btcusd", "ethusd", "xrpusd"], id="coin-select", value="btcusd"),
    
     dcc.Graph(id="candles"),
    
])

@app.callback(
    Output("candles", "figure"),
    Input("coin-select", "value"),
)

def update_figure(coin_pair):
     
    print(coin_pair)
    # data = requests.get(url, params).json()["data"]["ohlc"]
    # data = pd.DataFrame(data)
    
    # data.timestamp = pd.to_datetime(data.timestamp, unit = "s")
    
    data = btceur_1h.iloc[:10]
    
    candles = go.Figure(
        data = [
            go.Candlestick(
                x = data.date,
                open = data.open,
                high = data.high,
                low = data.low,
                close = data.close
            )
        ]
    )
    
    candles.update_layout(xaxis_rangeslider_visible=False, height=500)
    
    return candles


if __name__ == '__main__':
    app.run_server(debug=True)
