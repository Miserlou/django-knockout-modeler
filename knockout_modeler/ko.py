from django.template.loader import render_to_string
import simplejson as json
import datetime

def get_fields(model):

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
        return []

def koModel(model, field_names=None, data=None):

    try:
        if type(model) == str:
            modelName = model
        else:
            modelName = model.__name__

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
        return ''

def koBindings(model):

    try:
        if type(model) == str:
            modelName = model
        else:
            modelName = model.__class__.__name__

        modelBindingsString = "ko.applyBindings(new " + modelName + "ViewModel(), $('#" + modelName.lower() + "s')[0]);"
        return modelBindingsString

    except Exception, e:
        return ''

def koData(queryset, field_names, name=None):

    try:
        modelName = queryset[0].__class__.__name__    
        modelNameData = []

        if field_names:
            fields = field_names
        else:
            fields = get_fields(model)

        for obj in queryset:
            temp_dict = dict()
            for field in fields:
                try:
                    temp_dict[field] = getattr(obj, str(field))
                except Exception, e:
                    continue
            modelNameData.append(temp_dict)

        if name:
            modelNameString = name
        else:
            modelNameString = modelName + "Data"

        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
        return "var " + modelNameString + " = " + json.dumps(modelNameData, default=dthandler) + ';'
    except Exception, e:
        return ''

def ko(queryset, field_names):

    try:
        koDataString = koData(queryset, field_names)
        koModelString = koModel(queryset[0].__class__.__name__, field_names, data=True)
        koBindingsString = koBindings(queryset[0])

        koString = koDataString + '\n' + koModelString + '\n' + koBindingsString

        return koString
    except Exception, e:
        return ''
