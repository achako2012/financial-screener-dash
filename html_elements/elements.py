import dash_core_components as dcc
import dash_html_components as html

def title(text):
    return html.H1(
        className='headder',
        children = text
    )
    
def link(text, url):
   return html.Div(
        children=[
            dcc.Markdown(f'''
            [{text}]({url})
            ''')
        ]
    )
   
def action_elements():
    return html.Div(
        className='elements',
        children=[
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Ticket price by passengers class',
                        'value': 'fare_class'},
                    {'label': 'Age by passengers class', 'value': 'age_class'},
                ],
                value='fare_class'
            ),

            dcc.RadioItems(
                options=[
                    {'label': 'Histogram', 'value': 'hist'},
                    {'label': 'Boxplot', 'value': 'boxplot'}
                ],
                value='hist',
                id='radio-input'
            )
        ]
    )

def paragraph(text):
    return html.P(
        className='paragraph',
        children=text
    )

def input_element():
    return html.Div(
        className='inputs',
        children=[
            html.H2(
                id='display-text',
                children='Headder'
            ),
            dcc.Input(id='input-text', value='', type="text")
        ]
    )
    
