import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# TODO:
# 1. Create range option only with range slider. Delete candells length
# 2. Create html tag with current diaposone description
# 3. Create radiobutton to switch beetween line and candles
# 4. Create Indicator charts
# 5. Styling the code

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

    html.Div(children='Data description here'),
    
    html.Div([
        dcc.Slider(0, 10, 1, value=5, marks=None, id="range_slider")
    ], id="range_slider_container"),

    dcc.Graph(id="candles"),
])


@app.callback(
    Output("range_slider_container", "children"),
    Input("coin_pair", "value"),
    Input("timeframe", "value")
)
def update_slider(coin_pair, timeframe):

    # we need to chouse which data frame we'll use
    if coin_pair == 'btceur':
        df = btceur_1h, btceur_d
    elif coin_pair == 'btcusd':
        df = btcusd_1h, btcusd_d
    elif coin_pair == 'ethbtc':
        df = ethbtc_1h, ethbtc_d
    else:
        df = etheur_1h, etheur_d

    # Since we have 2 timeframes for each data frame we need to chose which one we take
    if timeframe == 'hour':
        df = df[0]
    else:
        df = df[1]

    filtered_df = df.loc[(df['date'] > '2021-12-31 00:00:00')
                         & (df['date'] < '2023-01-01 00:00:00')]

    return dcc.Slider(
        min=0,
        max=int(len(filtered_df)),
        step=1,
        value=0,
        marks={
            0: {'label': filtered_df.iloc[0].date.split(" ")[0]},
            int(len(filtered_df))*0.25: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.25)].date.split(" ")[0]},
            int(len(filtered_df))*0.5: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.5)].date.split(" ")[0]},
            int(len(filtered_df))*0.75: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.75)].date.split(" ")[0]},
            int(len(filtered_df)): {'label': filtered_df.iloc[int(len(filtered_df))-1].date.split(" ")[0]}
        },
        tooltip={"placement": "bottom", "always_visible": True},
        id="range_slider")


@app.callback(
    Output("candles", "figure"),
    Input("candles_length", "value"),
    Input("coin_pair", "value"),
    Input("timeframe", "value"),
    Input("range_slider", "value"),
)
def update_figure(candles_length, coin_pair, timeframe, range_slider):
    
    # print(range_slider)

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
    data = data.iloc[range_slider:range_slider+candles_length]

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
