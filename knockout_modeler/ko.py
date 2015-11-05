from django.template.loader import render_to_string
import cgi
try:
    import simplejson as json
except ImportError, e:
    import json
import datetime

import logging
logger = logging.getLogger(__name__)

def get_fields(model):
    """
    Returns a Model's knockout_fields,
    or the default set of field names.
    """

    try:
        if hasattr(model, "knockout_fields"):
            fields = model.knockout_fields()
        else:
            try:
                fields = model.to_dict().keys()
            except Exception, e:
                fields = model._meta.get_all_field_names()

        return fields

    # Crash proofing
    except Exception, e:
        logger.exception(e)
        return []

def ko_model(model, field_names=None, data=None):
    """
    Given a model, returns the Knockout Model and the Knockout ViewModel.
    Takes optional field names and data.
    """

    try:
        if type(model) == str:
            modelName = model
        else:
            modelName = model.__class__.__name__

        if field_names:
            fields = field_names
        else:
            fields = get_fields(model)

        if hasattr(model, "comparator"):
            comparator = str(model.comparator())
        else:
            comparator = 'id' 

        modelViewString = render_to_string("knockout_modeler/model.html", {'modelName': modelName, 'fields': fields, 'data': data, 'comparator': comparator} )

        return modelViewString
    except Exception, e:
        logger.exception(e)
        return ''

def ko_bindings(model):
    """
    Given a model, returns the Knockout data bindings.
    """

    try:
        if type(model) == str:
            modelName = model
        else:
            modelName = model.__class__.__name__

        modelBindingsString = "ko.applyBindings(new " + modelName + "ViewModel(), $('#" + modelName.lower() + "s')[0]);"
        return modelBindingsString

    except Exception, e:
        logger.error(e)
        return ''

def ko_json(queryset, field_names=None, name=None, safe=False):
    """
    Given a QuerySet, return just the serialized representation
    based on the knockout_fields. Useful for middleware/APIs.

    Convenience method around ko_data.

    """
    return ko_data(queryset, field_names, name, safe, return_json=True)

def ko_data(queryset, field_names=None, name=None, safe=False, return_json=False):
    """
    Given a QuerySet, return just the serialized representation
    based on the knockout_fields as JavaScript.

    """

    try:
        modelName = queryset[0].__class__.__name__    
        modelNameData = []

        if field_names is not None:
            fields = field_names
        else:
            fields = get_fields(queryset[0])

        for obj in queryset:
            temp_dict = dict()
            for field in fields:
                try:
                    attribute = getattr(obj, str(field))

                    if not safe:
                        if isinstance(attribute, basestring):
                            attribute = cgi.escape(attribute)

                    temp_dict[field] = attribute
                except Exception, e:
                    continue
            modelNameData.append(temp_dict)

        if name:
            modelNameString = name
        else:
            modelNameString = modelName + "Data"

        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
        dumped_json = json.dumps(modelNameData, default=dthandler)
        if return_json:
            return dumped_json
        return "var " + modelNameString + " = " + dumped_json + ';'
    except Exception, e:
        logger.exception(e)
        return ''

def ko(queryset, field_names=None):
    """
    Converts a Django QuerySet into a complete Knockout implementation.
    """

    try:
        koDataString = ko_data(queryset, field_names)
        koModelString = ko_model(queryset[0].__class__.__name__, field_names, data=True)
        koBindingsString = ko_bindings(queryset[0])

        koString = koDataString + '\n' + koModelString + '\n' + koBindingsString

        return koString
    except Exception, e:
        logger.error(e)
        return ''
