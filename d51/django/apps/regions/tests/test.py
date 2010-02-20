from django import test
from django.db import models as django_models
import random

class TestCase(test.TestCase):
    def assertSubclass(self, cls, clsinfo):
        self.assertTrue(issubclass(cls, clsinfo))

    def assertHasField(self, model, name, expected_field):
        field = model._meta.get_field(name)
        self.assertSubclass(field.__class__, expected_field)

    def assertFieldIsOptional(self, model, name):
        field = model._meta.get_field(name)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def assertRelatesTo(self, model, name, relates_to):
        field = model._meta.get_field(name)
        self.assertEqual(field.related.model.__name__, relates_to.__name__)

class ModelTestCase(TestCase):
    def test_is_a_django_model(self):
        self.assertSubclass(self.model_class, django_models.Model)

    def test_has_a_name_charfield(self):
        model = self.model_class()
        self.assertHasField(model, 'name', django_models.CharField)

    def test_returns_name_when_cast_to_string(self):
        random_name = "some random name %d" % random.randint(1000, 2000)
        model = self.model_class(name=random_name)
        self.assertEqual(str(model), random_name)


class Client(test.client.Client):
    pass

