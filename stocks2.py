import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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

# print(btceur_1h.iloc[0])

app = Dash()

app.layout = html.Div([

    dcc.Dropdown([20, 40, 60, 100], id="candles_length", value=20),
    dcc.Dropdown(["btceur", "btcusd", "ethbtc", "etheur"],
                 id="coin_pair", value="btceur"),
    dcc.Dropdown(["day", "hour"], id="timeframe", value="hour"),

    dcc.Graph(id="candles"),

])


@app.callback(
    Output("candles", "figure"),
    Input("candles_length", "value"),
    Input("coin_pair", "value"),
    Input("timeframe", "value"),
)
def update_figure(candles_length, coin_pair, timeframe):
    
    # we need to chouse which data frame we'll use
    if coin_pair == 'btceur':
        data = btceur_1h, btceur_d
    elif coin_pair == 'btcusd':
        data = btcusd_1h, btcusd_d
    elif coin_pair == 'ethbtc':
        data = ethbtc_1h, ethbtc_d
    else:
        data = etheur_1h, etheur_d
        
    # Since we have 2 timeframes for each data frame we need to chose which one we take
    if timeframe == 'hour':
        data = data[0]
    else:
        data = data[1]
    
    # Here we choose the length of data frame
    data = data.iloc[:candles_length]

    candles = go.Figure(
        data=[
            go.Candlestick(
                x=data.date,
                open=data.open,
                high=data.high,
                low=data.low,
                close=data.close
            )
        ]
    )

    candles.update_layout(xaxis_rangeslider_visible=False, height=500)

    return candles


if __name__ == '__main__':
    app.run_server(debug=True)
