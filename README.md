![Django knockout!](http://i.imgur.com/JOBuh4u.gif)

django-knockout-modeler
==============

Super easy knockout.js ModelView templates for you Django models

    django-knockout-modeler turns this:

    ```python
    class MyObjectViewModel(models.Model):
        myNumber = models.IntegerField()
        myName = models.CharField()
    ```

    into this:

    ```javascript
        MyObjectViewModel = {
            myNumber: ko.observable(),
            myName: ko.observable(),
        }


        MyObjectViewModel.myNumber.subscribe(function(newValue) { });
        MyObjectViewModel.myName.subscribe(function(newValue) { });
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

