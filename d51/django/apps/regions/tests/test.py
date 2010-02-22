import d51.django.apps.regions.tests.support.models
from django import test
from django.core.management.color import no_style
from django.core.management.sql import sql_create, sql_delete, sql_indexes
from django.db import connection
from django.db import models as django_models
import random
import re

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

class GeometryModelTestCase(ModelTestCase):
    def test_has_proper_geometry_in_raw_field(self):
        model = self.model_class()
        self.assertHasField(model, 'raw', self.expected_geometry)

class Client(test.client.Client):
    pass

def execute_sql(statements):
    cursor = connection.cursor()
    for sql in statements:
        cursor.execute(sql)

def create_model_tables():
    """
    Create the table for the provided model(s)

    Yes, yes, yes.  This *should* be part of Django.  Instead, this logic is
    locked down like porn star with an STD inside the `django.core.management`
    command, so we've got the logic here.
    """
    style = no_style()
    app = d51.django.apps.regions.tests.support.models
    statements = sql_create(app, style) + sql_indexes(app, style)
    execute_sql(statements)

def destroy_model_tables():
    try:
        statements = sql_delete(d51.django.apps.regions.tests.support.models, no_style())
        execute_sql(statements)
    except Exception, e:
        # Postgres seems to like to pretend that the table isn't there, even
        # when the database says it is.  We're catching this error here to keep
        # everyone happy.  "Pick your battles" I believe is the phrase.
        if re.search('table "[a-z_]+" does not exist', str(e)):
                return
        raise e

