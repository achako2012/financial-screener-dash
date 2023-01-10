from dash import dcc
import dash_html_components as html


def create_slider():
    return html.Div([
        html.P(id="current_range", children='You current range is:'),

        # Slider with default values
        html.Div([
            dcc.RangeSlider(0, 30, 1, value=[
                0, 1000], marks=None, id="range_slider")
        ], id="range_slider_container"),
    ])


def create_dropdown(title, options, id, value):
    return html.Div([
        html.P(title),
        dcc.Dropdown(options, id=id, value=value)
    ], className='dropdown-container')

def create_radiobutton(options, id, value):
    return html.Div([
        dcc.RadioItems(options, id=id, value=value)
    ])