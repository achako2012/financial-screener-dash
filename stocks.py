from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta
import plotly.express as px

app = Dash()

app.layout = html.Div([
    
    dcc.Dropdown(["btcusd", "ethusd", "xrpusd"], id="coin-select", value="btcusd"),
    dcc.Dropdown(["60", "3600", "86400"], id="timeframe-select", value="60"),
    dcc.Dropdown(["20", "50", "100"], id="num-bars-select", value="20"),
    
    dcc.Graph(id="candles"),
    dcc.Graph(id="indicator"),
    
    dcc.Interval(id="interval", interval = 2000),
])

@app.callback(
    Output("candles", "figure"),
    Output("indicator", "figure"),
    Input("interval", "n_intervals"),
    Input("coin-select", "value"),
    Input("timeframe-select", "value"),
    Input("num-bars-select", "value"),
)

def update_figure(n_intervals, coin_pair, timeframe, num_bars):
    url = f"https://www.bitstamp.net/api/v2/ohlc/{coin_pair}/"
    
    params = {
        "step": timeframe,
        "limit": int(num_bars) + 14,
    }
    
    data = requests.get(url, params).json()["data"]["ohlc"]
    data = pd.DataFrame(data)
    data.timestamp = pd.to_datetime(data.timestamp, unit = "s")
    
    data['rsi'] = ta.rsi(data.close.astype(float))
    
    data = data.iloc[14:]
    
    candles = go.Figure(
        data = [
            go.Candlestick(
                x = data.timestamp,
                open = data.open,
                high = data.high,
                low = data.low,
                close = data.close
            )
        ]
    )
    
    candles.update_layout(xaxis_rangeslider_visible=False, height=500)
    
    indicator = px.line(x=data.timestamp, y=data.rsi, height=300)
    
    print(data)
    
    return candles, indicator

if __name__ == '__main__':
    app.run_server(debug=True)