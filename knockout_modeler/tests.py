"""
Simple tests for Django Knockout Modeler.

"""

import json
import uuid

import js2py
from django.db import models
from django.test import TransactionTestCase
from django_fake_model import models as f

from knockout_modeler.ko import get_fields
from knockout_modeler.ko import get_object_data
from knockout_modeler.ko import ko
from knockout_modeler.ko import ko_bindings
from knockout_modeler.ko import ko_data
from knockout_modeler.ko import ko_json
from knockout_modeler.ko import ko_model
from knockout_modeler.templatetags import knockout


######
#  Fake Testing Models
######

class Profession(f.FakeModel):
    title = models.CharField('Title', max_length=200, blank=True)
    skill = models.IntegerField('Skill', default=0)

    class Meta:
        app_label = 'test'


class HomeCity(f.FakeModel):
    name = models.CharField('Name', max_length=200, blank=True)
    population = models.IntegerField('Skill', default=0)

    class Meta:
        app_label = 'test'

    @staticmethod
    def knockout_fields():
        return ['name']


class Person(f.FakeModel):
    first_name = models.CharField('First Name', max_length=200, blank=True)
    last_name = models.CharField('Last Name', max_length=200, blank=True)
    uuid = models.CharField('UUID', max_length=200, blank=False, unique=True)

    profession = models.ForeignKey(
        Profession, blank=True, on_delete=models.PROTECT)
    home_city = models.ForeignKey(
        HomeCity, blank=True, on_delete=models.PROTECT)

    class Meta:
        app_label = 'test'

    @classmethod
    def comparator(cls):
        return 'uuid'

    @staticmethod
    def knockout_fields():
        return ['first_name', 'home_city', 'profession']

####
# The actual tests
####


class KnockoutTests(TransactionTestCase):

    def setup_user(self):

        rapper = Profession()
        rapper.title = "Rapper"
        rapper.skill = 999
        rapper.save()

        no = HomeCity()
        no.name = "New Orleans"
        no.population = 999
        no.save()

        wayne = Person()
        wayne.first_name = 'Lil'
        wayne.last_name = 'Wayne'
        wayne.uuid = uuid.uuid4()
        wayne.profession = rapper
        wayne.home_city = no
        wayne.save()

        return wayne

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2. (Sanity test.)
        """

        self.assertEqual(1 + 1, 2)

    @Profession.fake_me
    @HomeCity.fake_me
    @Person.fake_me
    def test_get_fields(self):
        """
        Tests get_fields
        """

        wayne = self.setup_user()
        fields = get_fields(wayne)
        self.assertEqual(fields, ['first_name', 'home_city', 'profession'])

    @Profession.fake_me
    @HomeCity.fake_me
    @Person.fake_me
    def test_get_object_data(self):
        """
        Tests get_object_data
        """

        # Test a regular model
        wayne = self.setup_user()
        fields = get_fields(wayne)
        expected = {
            'first_name': 'Lil',
            'home_city': {'name': 'New Orleans'},
            'profession': {'skill': 999, 'id': 1, 'title': 'Rapper'},
        }
        actual = get_object_data(wayne, fields, safe=False)
        self.assertEqual(actual, expected)

        # Test a model with a dict
        wayne = self.setup_user()
        expected = {
            'first_name': 'Lil',
            'home_city': {'name': 'New Orleans'},
            'home_city_dict': {'name': 'New Orleans'},
            'profession': {'skill': 999, 'id': 2, 'title': 'Rapper'},
            'profession_dict': {'skill': 999, 'id': 2, 'title': 'Rapper'},
        }
        wayne.home_city_dict = expected['home_city']
        wayne.profession_dict = expected['profession']
        new_fields = ['home_city_dict', 'profession_dict']
        actual = get_object_data(wayne, fields + new_fields, safe=False)
        self.assertEqual(actual, expected)

        # Test a model with a list of dicts
        wayne = self.setup_user()
        expected = {
            'first_name': 'Lil',
            'home_city': {'name': 'New Orleans'},
            'profession': {'skill': 999, 'id': 3, 'title': 'Rapper'},
            'list_of_dicts': [
                {'name': 'New Orleans'},
                {'skill': 999, 'id': 3, 'title': 'Rapper'},
            ],
        }
        wayne.list_of_dicts = [expected['home_city'], expected['profession']]
        new_fields = ['list_of_dicts']
        actual = get_object_data(wayne, fields + new_fields, safe=False)
        self.assertEqual(actual, expected)

        # Test a model with a list of models
        wayne = self.setup_user()
        expected = {
            'first_name': 'Lil',
            'home_city': {'name': 'New Orleans'},
            'profession': {'skill': 999, 'id': 4, 'title': 'Rapper'},
            'list_of_models': [{
                'first_name': 'Lil',
                'home_city': {'name': 'New Orleans'},
                'profession': {'skill': 999, 'id': 5, 'title': 'Rapper'},
            }],
        }
        wayne.list_of_models = [self.setup_user()]
        new_fields = ['list_of_models']
        actual = get_object_data(wayne, fields + new_fields, safe=False)
        self.assertEqual(actual, expected)

        # Test with safe=True and some existing and non-existing fields
        wayne = self.setup_user()
        fields = ['first_name', 'home_city', 'non-existent']
        expected = {
            'first_name': 'Lil',
            'home_city': {'name': 'New Orleans'},
        }
        actual = get_object_data(wayne, fields, safe=True)
        self.assertEqual(actual, expected)

    @Profession.fake_me
    @HomeCity.fake_me
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

    @Profession.fake_me
    @HomeCity.fake_me
    @Person.fake_me
    def test_ko_bindings(self):
        """
        Tests ko_bindings
        """

        wayne = self.setup_user()
        bindings = ko_bindings(wayne)
        self.assertNotEqual(bindings, '')

    @Profession.fake_me
    @HomeCity.fake_me
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

    @Profession.fake_me
    @HomeCity.fake_me
    @Person.fake_me
    def test_ko_data(self):
        """
        Tests ko_data
        """

        # Test an object
        wayne = self.setup_user()
        people = Person.objects.all()

        data = ko_data(people)
        self.assertNotEqual(data, '[]')

        # Will raise if invalid.
        interpreted = js2py.eval_js(data)

        # Test a vanilla QS
        rapper = Profession.objects.get(pk=1)
        data = ko_data(rapper)
        self.assertNotEqual(data, '[]')
        interpreted = js2py.eval_js(data)

        rapper = Profession.objects.none()
        data = ko_data(rapper)
        self.assertNotEqual(data, '[]')
        interpreted = js2py.eval_js(data)

        rapper = ''
        data = ko_data(rapper)
        self.assertEqual(data, '[]')
        interpreted = js2py.eval_js(data)

        rapper = []
        data = ko_data(rapper)
        self.assertEqual(data, '[]')
        interpreted = js2py.eval_js(data)

        # Test an individual object
        rapper = wayne.profession
        data = ko_data(rapper)
        self.assertNotEqual(data, '[]')
        interpreted = js2py.eval_js(data)

    @Profession.fake_me
    @HomeCity.fake_me
    @Person.fake_me
    def test_ko(self):
        """
        Tests ko
        """

        wayne = self.setup_user()
        people = Person.objects.all()

        ko_s = ko(people)
        self.assertNotEqual(ko_s, '')

    @Profession.fake_me
    @HomeCity.fake_me
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
