dfrom django import template
import simplejson as json
import datetime
from knockout_modeler.ko import ko, koData, koModel, get_fields

register = template.Library()

def knockout(values):
    """
    Knockoutify a QuerySet!
    """

    modelClass = values[0].__class__
    if hasattr(modelClass, "knockout_fields"):
        field_names = values[0].knockout_fields()
    else:
        try:
            fields = model.to_dict().keys()
        except Exception, e:
            fields = model._meta.fields

    return ko(values, field_names)

def knockout_data(values):
    """

    """

    modelClass = values[0].__class__
    if hasattr(modelClass, "knockout_fields"):
        field_names = values[0].knockout_fields()
    else:
        field_names = values[0].to_dict().keys()

    return koData(values, field_names)

def knockout_model(values):
    """

    """

    modelClass = values[0].__class__
    if hasattr(modelClass, "knockout_fields"):
        field_names = values[0].knockout_fields()
    else:
        try:
            fields = model.to_dict().keys()
        except Exception, e:
            fields = model._meta.fields

    return koModel(modelClass, field_names)

register.filter(knockout)
register.filter(knockout_data)
register.filter(knockout_model)