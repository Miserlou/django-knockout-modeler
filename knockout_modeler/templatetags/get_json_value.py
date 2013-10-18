from django import template
import simplejson as json
import datetime

register = template.Library()

def get_json_value(value, arg):
    """
    Get a json-safe value from an item.
    """
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
    return json.dumps(getattr(value, arg), default=dthandler)

register.filter(get_json_value)