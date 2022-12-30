from . import helpers
import dash_html_components as html

def is_number(in_value):
    try:
        float(in_value)
        return True
    except ValueError:
        return False
    
    
def print_something(text):
    return helpers.print_word(text)

def title(children):
    return html.H1(
        className='headder',
        children = children
    )