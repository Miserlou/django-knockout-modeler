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

    self.addMyObject = function(myobject) {
        self.myobjects.push(myobject);
    };
    self.removeMyObject = function(myobject){ 
        self.myobjects.remove(myobject) 
    };
    self.sortMyObjectsAsc = function(){
        self.myobjects(self.myobjects().sort(function(a, b) {
            return a.myNumber>b.myNumber?-1:a.myNumber<b.myNumber?1:0;
        }));
    };
    self.sortMyObjectsDesc = function(){
        self.myobjects(self.myobjects().sort(function(a, b) {
            return a.myNumber<b.myNumber?-1:a.myNumber>b.myNumber?1:0;
        }));
    };
}

ko.applyBindings(new MyObjectViewModel(), $('#myobjects')[0]);
```

with just this!

```django
{{ myObjects|knockout }}
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
      'knockout_modeler',
    )
    ```

2. Include Knockout.js in your HTML:

    ```html
    <script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/knockout/2.3.0/knockout-min.js'></script>
    ```

4. Knockout your QuerySet:

    ```html   
    {% load knockout %}
    <script>
        {{ myObjects|knockout }}
    </script>
    ```

5. Template your results:

    ```html
    <script type="text/html" id="myTemplate">
        <div>
            <h2><span data-bind="text: myName"></span></h2>
            <h3><span data-bind="text: myNumber"></span></h3>
        </div>
    </script> 
    ```

6. Loop over your bound data like so:

    ```html
    <div id="myobjects">
        <div data-bind="template: { name: 'myTemplate', foreach: myobjects }"></div>   
    </div>
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

And even just the bindings:

```django
{{ myObjects | knockout_bindings }}
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

by default, it uses the keys in the object's __to_dict()__ method. For computed properties, you can use python's __property__ function.

Sorting
----------

django-knockout provides some convenient methods for sorting your data. By default, it will use the object's 'id' field, but you can also define your own comparator like so:

```python
@classmethod
def comparator(self):
    return 'value'
```

If you don't define a comparator, 'id' must be in your knockout_fields.

Multi-Model Support
----------

django-knockout is all ready set up to be used with multiple types of data at the same time, as bindings happen to specific objects:

```javascript
ko.applyBindings(new MyObjectViewModel(), $('#myobjects')[0]);
```

which means that you somewhere in your HTML template, you will need to have an object with that id, like so:

```html
<div id="myobjects">
    <div data-bind="foreach: myobjects">
        User <span data-bind="text: myName"></span> is number <span data-bind="text: myNumber"></span>.
    </div>
</div>
```

This is handy for prototyping, but more advanced applications may want to use the [master ViewModel](http://stackoverflow.com/a/9294752/1135467) technique instead.

Multi-Data Support
----------

If you're using multiple QuerySets of the same type, you'll need to define a custom name for the data variables.

```django
{{ myObjects | knockout_data:'MyNamedObjectsData' }}
```

Issues
-------

There's probably a lot more that can be done to improve this. Please file issues if you find them!
