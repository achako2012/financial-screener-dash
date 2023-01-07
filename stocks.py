import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# TODO:
# 1. Create Indicator charts
# 2. Styling the code

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

# Reverse data frames
btceur_1h = btceur_1h.iloc[::-1]
btceur_d = btceur_d.iloc[::-1]
btcusd_1h = btcusd_1h.iloc[::-1]
btcusd_d = btcusd_d.iloc[::-1]
ethbtc_1h = ethbtc_1h.iloc[::-1]
ethbtc_d = ethbtc_d.iloc[::-1]
etheur_1h = etheur_1h.iloc[::-1]
etheur_d = etheur_d.iloc[::-1]

app = Dash()

app.layout = html.Div([

    dcc.Dropdown(options=[
        {'label': 'BTC/EUR', 'value': 'btceur'},
        {'label': 'BTC/USD', 'value': 'btcusd'},
        {'label': 'ETH/BTC', 'value': 'ethbtc'},
        {'label': 'ETH/EUR', 'value': 'etheur'},
    ],
        id="coin_pair",
        value="btceur"),

    dcc.Dropdown(["day", "hour"], id="timeframe", value="day"),

    dcc.Dropdown([2022, 2021, 2020, 2019], id="select_year", value=2022),

    dcc.RadioItems(options=[
        {'label': 'Candles', 'value': 'candles'},
        {'label': 'OHLC', 'value': 'ohlc'},
        {'label': 'Line', 'value': 'line'}
    ],
        value="candles",
        id="chart_type"),

    html.Div(id="current_range", children='Your current range is:'),

    html.Div([
        dcc.RangeSlider(0, 30, 1, value=[
                        5, 15], marks=None, id="range_slider")
    ], id="range_slider_container"),

    dcc.Graph(id="candles"),
])


def filter_data(coin_pair, timeframe, select_year):
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

    filtered_df = df.loc[(df['date'] > '{}-12-31 00:00:00'.format(select_year-1))
                         & (df['date'] < '{}-01-01 00:00:00'.format(select_year+1))]

    return filtered_df


@app.callback(
    Output("range_slider_container", "children"),
    Input("coin_pair", "value"),
    Input("timeframe", "value"),
    Input("select_year", "value"),
)
def update_slider(coin_pair, timeframe, select_year):
    filtered_df = filter_data(coin_pair, timeframe, select_year)

    return dcc.RangeSlider(
        min=0,
        max=int(len(filtered_df)),
        step=1,
        marks={
            0: {'label': filtered_df.iloc[0].date.split(" ")[0]},
            int(len(filtered_df))*0.25: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.25)].date.split(" ")[0]},
            int(len(filtered_df))*0.5: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.5)].date.split(" ")[0]},
            int(len(filtered_df))*0.75: {'label': filtered_df.iloc[int((len(filtered_df) - 1)*0.75)].date.split(" ")[0]},
            int(len(filtered_df)): {'label': filtered_df.iloc[int(len(filtered_df))-1].date.split(" ")[0]}
        },
        value=[0, 800],
        id="range_slider")


@app.callback(
    Output("candles", "figure"),
    Output("current_range", "children"),
    Input("coin_pair", "value"),
    Input("timeframe", "value"),
    Input("range_slider", "value"),
    Input("chart_type", "value"),
    Input("select_year", "value")
)
def update_figure(coin_pair, timeframe, range_slider, chart_type, select_year):

    filtered_df = filter_data(coin_pair, timeframe, select_year)

    # Here we choose the length of data frame
    filtered_df = filtered_df.iloc[range_slider[0]:range_slider[1]]

    message = "You current range is: {} - {}".format(filtered_df.iloc[0]['date'].split(
        " ")[0], filtered_df.iloc[-1]['date'].split(" ")[0])

    if chart_type == 'candles':
        figure = go.Figure(
            data=[
                go.Candlestick(
                    x=filtered_df['date'],
                    open=filtered_df['open'],
                    high=filtered_df['high'],
                    low=filtered_df['low'],
                    close=filtered_df['close']
                )
            ]
        )
    elif chart_type == 'ohlc':
        figure = go.Figure(
            data=[
                go.Ohlc(
                    x=filtered_df.date,
                    open=filtered_df.open,
                    high=filtered_df.high,
                    low=filtered_df.low,
                    close=filtered_df.close
                )
            ]
        )
    else:
        figure = go.Figure(
            [go.Scatter(x=filtered_df.date, y=filtered_df.high)])

    figure.update_layout(xaxis_rangeslider_visible=False, height=500)

    return figure, message


if __name__ == '__main__':
    app.run_server(debug=True)
