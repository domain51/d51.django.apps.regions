from d51.django.apps.regions import models
from d51.django.apps.regions.tests import test

django_models = models.models

class TestOfRegion(test.ModelTestCase):
    model_class = models.Region

    def test_has_a_slug(self):
        region = models.Region()
        self.assertHasField(region, 'slug', django_models.SlugField)

    def test_has_optional_parent_that_relates_to_itself(self):
        region = models.Region()
        self.assertHasField(region, 'parent', django_models.ForeignKey)
        self.assertFieldIsOptional(region, 'parent')
        self.assertRelatesTo(region, 'parent', models.Region)

class TestOfPoint(test.ModelTestCase):
    model_class = models.Point

    def test_has_a_geometry_field_that_is_a_point(self):
        point = models.Point()
        self.assertHasField(point, 'geometry', django_models.PointField)

class TestOfPolygon(test.ModelTestCase):
    model_class = models.Polygon

    def test_has_a_geometry_field_that_is_a_polygon(self):
        polygon = models.Polygon()
        self.assertHasField(polygon, 'geometry', django_models.PolygonField)
