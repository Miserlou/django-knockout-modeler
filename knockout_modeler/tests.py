"""
Simple tests for Django Knockout Modeler.

"""

from django.conf import settings
from django.db import models
from django.test import TestCase
from django_fake_model import models as f

from knockout_modeler.ko import get_fields
from knockout_modeler.ko import ko_model
from knockout_modeler.ko import ko_bindings
from knockout_modeler.ko import ko_json
from knockout_modeler.ko import ko_data
from knockout_modeler.ko import ko

from knockout_modeler.templatetags import knockout

import json
import js2py

class Person(f.FakeModel):
    """
    FakeModel lets us test as if we real models.

    """

    first_name = models.CharField('First Name', max_length=200, blank=True)
    last_name = models.CharField('Last Name', max_length=200, blank=True)
    uuid = models.CharField('UUID', max_length=200, blank=False, unique=True)

    def knockout_fields(self):
        return ['first_name', 'uuid']

    @classmethod
    def comparator(self):
        return 'uuid'

class KnockoutTests(TestCase):
    
    def setup_user(self):
        wayne = Person()
        wayne.first_name = 'Lil'
        wayne.last_name = 'Wayne'
        wayne.uuid = 'dead-beef'
        wayne.save()
        return wayne

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2. (Sanity test.)
        """

        self.assertEqual(1 + 1, 2)

    @Person.fake_me
    def test_get_fields(self):
        """
        Tests get_fields
        """

        wayne = self.setup_user()
        fields = get_fields(wayne)
        self.assertEqual(fields, ['first_name', 'uuid'])

    @Person.fake_me
    def test_ko_model(self):
        """
        Tests ko_model
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        model = ko_model(wayne)
        self.assertNotEqual(model, '')

        interpreted = js2py.eval_js(model)

    @Person.fake_me
    def test_ko_bindings(self):
        """
        Tests ko_bindings
        """

        wayne = self.setup_user()
        bindings = ko_bindings(wayne)
        self.assertNotEqual(ko_bindings, '')

    @Person.fake_me
    def test_ko_json(self):
        """
        Tests ko_json
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        json_s = ko_json(people)
        self.assertNotEqual(json_s, '')

        loaded = json.loads(json_s)
        self.assertNotEqual(json_s, loaded)

    @Person.fake_me
    def test_ko_data(self):
        """
        Tests ko_data
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        data = ko_data(people)
        self.assertNotEqual(data, '')

        interpreted = js2py.eval_js(data)

    @Person.fake_me
    def test_ko(self):
        """
        Tests ko
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        ko_s = ko(people)
        self.assertNotEqual(ko_s, '')

    @Person.fake_me
    def test_ko_tags(self):
        """
        Tests the tags
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        knocked_data = knockout.knockout_data(people)
        self.assertNotEqual(knocked_data, '')

        knocked_bindings = knockout.knockout_bindings(people)
        self.assertNotEqual(knocked_bindings, '')

        knocked_model = knockout.knockout_model(people)
        self.assertNotEqual(knocked_model, '')

        knocked = knockout.knockout(people)
        self.assertNotEqual(knocked, '')
