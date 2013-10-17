from django.template.loader import render_to_string

def koModel(model):

    modelName = model.__name__
    fields = model._meta.get_all_field_names()
    modelViewString = render_to_string("knockout_modeler/model.html", {'modelName': modelName, 'fields': fields} )

    return modelViewString
