from django import template
try:
    import simplejson as json
except ImportError, e:
    import json
import datetime
from knockout_modeler.ko import ko, ko_data, ko_model, ko_bindings, get_fields

register = template.Library()

def knockout(values):
    """
    Knockoutify a QuerySet!
    """

    if not values:
        return ''
        
    field_names = get_fields(values[0])
    return ko(values, field_names)

def knockout_data(values, args=None):
    """

    """
    if not values:
        return ''

    name = None
    safe = False

    if args:
        arg_list = [arg.strip() for arg in args.split(',')]
        if len(arg_list) > 1:
            safe = True
        else:
            safe = False
        name = arg_list[0]

    field_names = get_fields(values[0])
    return ko_data(values, field_names, name, safe)

def knockout_model(values):
    """

    """
    if not values:
        return ''

    field_names = get_fields(values[0])
    modelClass = values[0].__class__
    return ko_model(modelClass, field_names)

def knockout_bindings(values):
    """

    """
    if not values:
        return ''

    return ko_bindings(values[0])

register.filter(knockout)
register.filter(knockout_data)
register.filter(knockout_model)
register.filter(knockout_bindings)