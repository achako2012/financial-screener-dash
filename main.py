import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from html_elements import title, link, action_elements, paragraph, input_element

titanic = pd.read_excel('data/titanic.xls')

app = dash.Dash()

app.layout = html.Div(children=[
    
    title('Dash'),
    
    link('Titanic data', 'https://www.kaggle.com/c/titanic/data'),
    
    action_elements(),
    
    paragraph('Data description here'),
    
    input_element(),
    
    

    # html.Div(
    #     children=[
    #         dcc.Markdown('''
    #         [Titanic data](https://www.kaggle.com/c/titanic/data)
    #         '''),
    #     ],
    # ),

    # html.Div(
    #     className='elements',
    #     children=[
    #         dcc.Dropdown(
    #             id='dropdown',
    #             options=[
    #                 {'label': 'Ticket price by passengers class',
    #                     'value': 'fare_class'},
    #                 {'label': 'Age by passengers class', 'value': 'age_class'},
    #             ],
    #             value='fare_class'
    #         ),

    #         dcc.RadioItems(
    #             options=[
    #                 {'label': 'Histogram', 'value': 'hist'},
    #                 {'label': 'Boxplot', 'value': 'boxplot'}
    #             ],
    #             value='hist',
    #             id='radio-input'
    #         ),
    #     ]
    # ),

    # html.P(
    #     className='paragraph',
    #     children='Data description here'
    # ),

    # html.Div(
    #     className='inputs',
    #     children=[
    #         html.H2(
    #             id='display-text',
    #             children='Headder'
    #         ),
    #         dcc.Input(id='input-text', value='', type="text"),

    #     ]
    # ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Bar(x=[1, 2, 3], y=[4, 1, 2], name='Cherbourg'),
                go.Bar(x=[1, 2, 3], y=[2, 4, 5], name='Queenstown'),
                go.Bar(x=[1, 2, 3], y=[3, 2, 3], name='Southampton')
            ],
            'layout': {
                'title': 'Port of embarkation',
                'xaxis': {
                    'title': 'passenger class'
                },
                'yaxis': {
                    'title': 'number of passangers'
                }
            }
        }
    )

])

@app.callback(
    Output(component_id='display-text', component_property='children'),
    [Input(component_id='input-text', component_property='value')]
)
def update_output_h2(input_value):
    return 'Today\'s news: {}'.format(input_value)

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [
        Input(component_id='dropdown', component_property='value'),
        Input(component_id='radio-input', component_property='value')
    ]
)
def update(plot_type_1, plot_type_2):
    if plot_type_2 == 'hist':
        display = go.Histogram
    else:
        display = go.Box

    if plot_type_1 == 'fare_class':
        title = "Ticket price based on passenger's class"
        plot_function = display
        first = titanic[titanic.pclass == 1].fare
        second = titanic[titanic.pclass == 2].fare
        third = titanic[titanic.pclass == 3].fare
    else:
        title = "Passangers age based on passenger's class"
        plot_function = display
        first = titanic[titanic.pclass == 1].age
        second = titanic[titanic.pclass == 2].age
        third = titanic[titanic.pclass == 3].age

    trace1 = plot_function(x=first, opacity=0.75, name='First class')
    trace2 = plot_function(x=second, opacity=0.75, name='Second class')
    trace3 = plot_function(x=third, opacity=0.75, name='Third class')

    data = [trace1, trace2, trace3]

    figure = {
        'data': data,
        'layout': {
            'title': title,
        },

    }
    return figure


if __name__ == '__main__':
    app.run_server()
