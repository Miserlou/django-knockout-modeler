![Django knockout!](http://i.imgur.com/Nf7Vxq6.gif)

django-knockout-modeler
==============

**django-knockout-modeler** makes it super easy to use knockout.js with your Django models. It's great for project with objects that have lots of different models, or models with lots of different fields, or both. It can be used in both prototyping complex applications and directly in the templates of simple ones.

**django-knockout-modeler** turns this:

```python
class MyObject(models.Model):
    myNumber = models.IntegerField()
    myName = models.CharField()

myObjects = MyObject.objects.all()
```

into this:

```javascript
var MyObjectData = [{   
    "myNumber": 666,
    "myName": "Gabe Newell"
}];

function MyObject(data) {
    myNumber = ko.observable(),
    myName = ko.observable()
}

function MyObjectViewModel() { 
    var self = this;
    self.myobjects = ko.observableArray(MyObjectData);

    self.addMyObject = function() {
        self.myobjects.push(new MyObject({ }));
    };
    self.removeMyObject = function(myobject){ 
        self.myobjects.remove(myobject) 
    };
    self.sortMyObjectsAsc = function(contractjob){
        self.myobjects(self.myobjects().sort(function(a, b) {
            return a.id>b.id?-1:a.id<b.id?1:0;
        ));
    };
    self.sortMyObjectsDesc = function(contractjob){
        self.myobjects(self.myobjects().sort(function(a, b) {
            return a.id<b.id?-1:a.id>b.id?1:0;
        ));
    };

}

ko.applyBindings(new MyObjectViewModel());
```

with just this!

```django
{{ myObjects | knockout }}
```

Quick start
------------

0. Install django-knockout-modeler

    ```python
    pip install django-knockout-modeler
    ```

1. Add 'knockout-modeler' to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = (
      ...
      'knockout-modeler',
    )
    ```

Simple Usage
---------

**django-knockout-modeler** can be used directly in templates to generate knockout models and knockout-ready data, or either one you choose. To put a QuerySet directly into a django template as a Knockout object, you can do this:

```django
{{ myObjects | knockout }}
```

To get the data object by itself, you can do this: 

```django
{{ myObjects | knockout_data }}
```

Similarly, you can get just the model, if you prefer to load your data from apis, like this: 

```django
{{ myObjects | knockout_model }}
```

Progammatic Usage
---------

First, import it!

```python
from knockout_modeler.ko import ko, koData, koModel
```

To get the whole template, you can do this:

```python
koString = ko(YourModel)
```

And to get just the data string you can do this..

```python
koString = koData(YourModel)
```

And, surprisingly, you can do the same for the model string:

```python
koString = koModel(YourModel)
```

Custom fieldsets are also allowed:
```python
fields = ['custom', 'fieldset', 'allowed']
koString = ko(entries, fields)
```

Access Control
----------

If you don't want to expose your entire model to Knockout, you can define a function in your model:

```python
def knockout_fields(self):
    return['name', 'number']
```

by default, it uses the keys in the object's __to_dict()__ method.

Sorting
----------

django-knockout provides some convenient methods for sorting your data. By default, it will use the object's 'id' field, but you can also define your own comparator like so:

```python
@classmethod
def comparator(self):
    return 'value'
```

If you don't define a comparator, 'id' must be in your knockout_fields.

Issues
-------

There's probably a lot more that can be done to improve this. Please file issues if you find them!
