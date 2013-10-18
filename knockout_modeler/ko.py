from django.template.loader import render_to_string

def koModel(model, field_names=None, data=None):

    if type(model) == str:
        modelName = model
    else:
        modelName = model.__name__

    if field_names:
        fields = field_names
    else:
        fields = model._meta.get_all_field_names()

    modelViewString = render_to_string("knockout_modeler/model.html", {'modelName': modelName, 'fields': fields, 'data': data} )

    return modelViewString

def koData(queryset, field_names):

    modelName = queryset[0].__class__.__name__
    modelDataString = render_to_string("knockout_modeler/data.html", {'modelName': modelName, 'queryset': queryset, 'field_names': field_names} )

    return modelDataString

def ko(queryset, field_names):

    koDataString = koData(queryset, field_names)
    koModelString = koModel(queryset[0].__class__.__name__, field_names, data=True)

    koString = koDataString + '\n' + koModelString

    return koString
