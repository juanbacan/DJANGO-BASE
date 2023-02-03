from django import template
import random

register = template.Library()

def callmethod(obj, methodname):
    method = getattr(obj, methodname)
    if "__callArg" in obj.__dict__:
        # if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()


def args(obj, arg):
    if not "__callArg" in obj.__dict__:
        # if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []
    obj.__callArg.append(arg)
    return obj


def to_char(value):
    return chr(64+value)

def seconds_to_string(seconds):
    if seconds >= 3600:
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{hours}:{minutes}:{seconds}"
    else:
        minutes = seconds // 60
        seconds = seconds % 60
        
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
            
        return f"{minutes}:{seconds}"
    
def add_class(field):
    # Check if it is a checkbox
    if field.field.widget.input_type == "checkbox":
        if "class" in field.field.widget.attrs:
            field.field.widget.attrs["class"] += " form-check-input"
        else:
            field.field.widget.attrs["class"] = "form-check-input"
    # Check if it is a select
    elif field.field.widget.input_type == "select":
        if "class" in field.field.widget.attrs:
            field.field.widget.attrs["class"] += " form-select"
        else:
            field.field.widget.attrs["class"] = "form-select"
    else:
        if "class" in field.field.widget.attrs:
            field.field.widget.attrs["class"] += " form-control"
        else:
            field.field.widget.attrs["class"] = "form-control"
    return field

def num_question(page, num, questions = 5):
    return (page - 1) * questions + num
    

def get_minutes(seconds):
    minutes =  seconds // 60
    if minutes >= 10:
        return minutes
    else:
        return f"0{minutes}"

def get_seconds(seconds):
    seconds = seconds % 60
    if seconds >= 10:
        return seconds
    else:
        return f"0{seconds}"
    
@register.simple_tag
def random_number(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)
    

register.filter("call", callmethod)
register.filter("args", args)
register.filter("to_char", to_char)
register.filter("time_to_string", seconds_to_string)
register.filter("add_class", add_class)
register.filter("num_question", num_question)
register.filter("get_minutes", get_minutes)
register.filter("get_seconds", get_seconds)