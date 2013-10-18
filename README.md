![Django knockout!](http://i.imgur.com/Nf7Vxq6.gif)

django-knockout-modeler
==============

'''django-knockout-modeler''' makes it super easy to use knockout.js with your Django models. It's great for project with objects that have lots of different models, or models with lots of different fields, or both. It can be used in both prototyping complex applications and directly in the templates of simple ones.

* '''django-knockout-modeler''' turns this:

    ```python
    class MyObject(models.Model):
        myNumber = models.IntegerField()
        myName = models.CharField()

    ```

* into this:

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
        self.myobjects = ko.observableArray(ContractJobData);

        self.addmyobject = function() {
            self.myobjects.push(new MyObject({ }));
        };
        self.removeMyObject = function(myobject){ self.myobjects.remove(myobject) };

    }

    ko.applyBindings(new MyObjectViewModel());
    ```

* with just this!

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



Custom Usage
---------

1. Import it!

    ```python
    import knockout_modeler.ko
    ```

2. Pass it a model!

    ```python
    koString = ko.koModel(YourModel)
    ```

