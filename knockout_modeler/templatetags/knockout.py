from django import template
import simplejson as json
import datetime
from knockout_modeler.ko import ko, koData, koModel, koBindings, get_fields

register = template.Library()

def knockout(values):
    """
    Knockoutify a QuerySet!
    """

    if not values:
        return ''
        
    field_names = get_fields(values[0])
    return ko(values, field_names)

def knockout_data(values, name=None):
    """

    """
    if not values:
        return ''

    field_names = get_fields(values[0])
    return koData(values, field_names, name)

def knockout_model(values):
    """

    """
    if not values:
        return ''

    modelClass = values[0].__class__
    field_names = get_fields(values[0])
    return koModel(modelClass, field_names)

def knockout_bindings(values):
    """

    """
    if not values:
        return ''

    return koBindings(values[0])

register.filter(knockout)
register.filter(knockout_data)
register.filter(knockout_model)
register.filter(knockout_bindings)