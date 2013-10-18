![Django knockout!](http://i.imgur.com/Nf7Vxq6.gif)

django-knockout-modeler
==============

Super easy knockout.js ModelView templates for you Django models

* django-knockout-modeler turns this:

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

    ```python
    {{ myContacts|knockout }}
    ```

Quick start
------------

0. Install django-knockout-modeler

    ```python
    pip install django-knockout-modeler
    ```

1. Add "welcome" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = (
      ...
      'knockout-modeler',
    )
    ```

Usage
---------

1. Import it!

    ```python
    import knockout_modeler.ko
    ```

2. Pass it a model!

    ```python
    koString = ko.koModel(YourModel)
    ```

