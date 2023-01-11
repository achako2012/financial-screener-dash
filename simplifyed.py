import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas_ta as ta
import plotly.express as px


def clear_table(table_name):
    # skip first row with ad link
    data = pd.read_csv('data/{}.csv'.format(table_name), skiprows=1)

    # delete unnecassery columns
    data.drop(['unix', 'Volume {}'.format(table_name[:3]),
              'Volume {}'.format(table_name[3:6])], axis=1, inplace=True)

    # reverse data frames
    data = data.iloc[::-1]

    # remove unnecessary data. we need only date starts on 2019
    data = data[data['date'] > '2018-31-12']

    return data


def clear_data(array):
    data = {}

    for elem in array:
        data[elem] = clear_table(elem)

    return data


data = clear_data([
    "BTCEUR_1h",
    "BTCEUR_d",
    "BTCUSD_1h",
    "BTCUSD_d",
    "ETHBTC_1h",
    "ETHBTC_d",
    "ETHEUR_1h",
    "ETHEUR_d"
])


app = Dash()
server = app.server
app.title = "PF-ICA2"


def create_dropdown(title, options, id, value):

    return html.Div([
        html.P(title),
        dcc.Dropdown(options, id=id, value=value)
    ], style={"width": "100%"})


def create_radiobutton(options, id, value):
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
    html.H1("Financial data screener"),

    html. H3(
        "It's a demo project of plotly dash possobilityes, only for study prospects."),

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
            [
                {'label': 'Candles', 'value': 'candles'},
                {'label': 'OHLC', 'value': 'ohlc'},
                {'label': 'Line', 'value': 'line'}
            ],
            "chart_type",
            "candles"
        ),

        create_radiobutton(
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
])


def get_filter_data(coin_pair, timeframe, select_year):
    # we need to chouse which data frame we'll use
    if coin_pair == 'btceur':
        df = data["BTCEUR_1h"], data["BTCEUR_d"]
    elif coin_pair == 'btcusd':
        df = data["BTCUSD_1h"], data["BTCUSD_d"]
    elif coin_pair == 'ethbtc':
        df = data["ETHBTC_1h"], data["ETHBTC_d"]
    else:
        df = data["ETHEUR_1h"], data["ETHEUR_d"]

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

    indicator.update_layout(height=250, template=template, yaxis={
                            'title': ""}, xaxis={'title': ""})

    return figure, message, indicator


if __name__ == '__main__':
    app.run_server()
