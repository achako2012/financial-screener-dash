import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
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

# Reverse data frames
btceur_1h = btceur_1h.iloc[::-1]
btceur_d = btceur_d.iloc[::-1]
btcusd_1h = btcusd_1h.iloc[::-1]
btcusd_d = btcusd_d.iloc[::-1]
ethbtc_1h = ethbtc_1h.iloc[::-1]
ethbtc_d = ethbtc_d.iloc[::-1]
etheur_1h = etheur_1h.iloc[::-1]
etheur_d = etheur_d.iloc[::-1]

# Remove unnecessary data. we need only date starts on 2019
btceur_1h = btceur_1h[btceur_1h['date'] > '2018-31-12']
btceur_d = btceur_d[btceur_d['date'] > '2018-31-12']
btcusd_1h = btcusd_1h[btcusd_1h['date'] > '2018-31-12']
btcusd_d = btcusd_d[btcusd_d['date'] > '2018-31-12']
ethbtc_1h = ethbtc_1h[ethbtc_1h['date'] > '2018-31-12']
ethbtc_d = ethbtc_d[ethbtc_d['date'] > '2018-31-12']
etheur_1h = etheur_1h[etheur_1h['date'] > '2018-31-12']
etheur_d = etheur_d[etheur_d['date'] > '2018-31-12']

app = Dash()
server = app.server
app.title = "PF-ICA2"

# Create elements part


def create_dropdown(title, options, id, value):

    return html.Div([
        html.P(title),
        dcc.Dropdown(options, id=id, value=value)
    ], style={"width": "100%"})


def create_radiobutton(title, options, id, value):

    return html.Div([
        dcc.RadioItems(options, id=id, value=value)
    ])


def create_slider():

    return html.Div([
        html.P(id="current_range", children='You current range is:',
               style={"margin": "20px 0px 0px 0px"}),

        # Slider with initaila values
        html.Div([
            dcc.RangeSlider(0, 30, 1, value=[
                0, 1000], marks=None, id="range_slider")
        ], id="range_slider_container"),
    ], style={"width": "80%", "margin": "auto"})


app.layout = html.Div([

    html.H1("This project is a demo of plotly dash possobilityes, only for study prospects."),

    html.Div([
        create_dropdown('Currency',
                        [
                            {'label': 'BTC/EUR', 'value': 'btceur'},
                            {'label': 'BTC/USD', 'value': 'btcusd'},
                            {'label': 'ETH/BTC', 'value': 'ethbtc'},
                            {'label': 'ETH/EUR', 'value': 'etheur'},
                        ],
                        'coin_pair',
                        'btceur'),

        create_dropdown('Timeframe', ["day", "hour"], "timeframe", "day"),

        create_dropdown('Select a year', [
            2022, 2021, 2020, 2019], "select_year", 2022),

    ], style={"display": "flex", "margin": "auto", "justify-content": "space-evenly", "width": "80%", "gap": "10px"}),

    create_slider(),

    html.Div([
        create_radiobutton(
            "Type",
            [
                {'label': 'Candles', 'value': 'candles'},
                {'label': 'OHLC', 'value': 'ohlc'},
                {'label': 'Line', 'value': 'line'}
            ],
            "chart_type",
            "candles"
        ),

        create_radiobutton(
            "Theme",
            [
                {'label': 'Dark', 'value': 'plotly_dark'},
                {'label': 'Light', 'value': 'plotly'}
            ],
            "template",
            "plotly"
        ),

    ], style={"display": "flex", "padding": "20px 0px", "margin": "auto", "justify-content": "space-between", "width": "80%", "gap": "10px"}),

    dcc.Graph(id="candles"),

    dcc.Graph(id="indicator"),

], style={
    "text-align": "center",
    "font-size": "large",
    "font-family": "Lato, Verdana, Arial, Tahoma"
})


def get_filter_data(coin_pair, timeframe, select_year):
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
    filtered_df = get_filter_data(coin_pair, timeframe, select_year)

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
        value=[0, int(len(filtered_df))],
        id="range_slider")


@app.callback(
    Output("candles", "figure"),
    Output("current_range", "children"),
    Output("indicator", "figure"),
    Input("coin_pair", "value"),
    Input("timeframe", "value"),
    Input("range_slider", "value"),
    Input("chart_type", "value"),
    Input("select_year", "value"),
    Input("template", "value")
)
def update_figure(coin_pair, timeframe, range_slider, chart_type, select_year, template):

    filtered_df = get_filter_data(coin_pair, timeframe, select_year)

    # Here we choose the length of data frame
    ranged_df = filtered_df.iloc[range_slider[0]:range_slider[1]]

    message = "You current range is: {} - {}".format(ranged_df.iloc[0]['date'].split(
        " ")[0], ranged_df.iloc[-1]['date'].split(" ")[0])

    if chart_type == 'candles':
        figure = go.Figure(
            data=[
                go.Candlestick(
                    x=ranged_df['date'],
                    open=ranged_df['open'],
                    high=ranged_df['high'],
                    low=ranged_df['low'],
                    close=ranged_df['close']
                )
            ]
        )
    elif chart_type == 'ohlc':
        figure = go.Figure(
            data=[
                go.Ohlc(
                    x=ranged_df.date,
                    open=ranged_df.open,
                    high=ranged_df.high,
                    low=ranged_df.low,
                    close=ranged_df.close
                )
            ]
        )
    else:
        figure = go.Figure(
            [go.Scatter(x=ranged_df.date, y=ranged_df.high)])

    figure.update_layout(xaxis_rangeslider_visible=False,
                         height=500, template=template)

    # Indicator starts here
    ranged_df['rsi'] = ta.rsi(ranged_df.close.astype('float'))

    # Indicator starts after 14th candle
    ranged_df = ranged_df.iloc[14:]

    indicator = px.line(x=ranged_df.date, y=ranged_df['rsi'])

    indicator.update_layout(height=250, template=template, yaxis={'title': ""}, xaxis={'title': ""})

    return figure, message, indicator


if __name__ == '__main__':
    app.run_server()
