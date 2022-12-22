from . import helpers

def is_number(in_value):
    try:
        float(in_value)
        return True
    except ValueError:
        return False
    
    
def print_something(text):
    return helpers.print_word(text)