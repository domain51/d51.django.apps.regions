from d51.django.apps.regions import models
from d51.django.apps.regions.tests import test
from d51.django.apps.regions.tests.support.models import EventForRegionTesting
from django.contrib.gis import geos
import random

django_models = models.models

def generate_random_poly():
    random_number = random.randint(10, 20)
    return models.Polygon.objects.create(
        name="some random polygon %d" % random_number,
        raw=geos.GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))')
    )

def generate_random_multipoly():
    random_number = random.randint(10, 20)
    return models.MultiPolygon.objects.create(
        name="some random multipolygon %d" % random_number,
        raw=geos.MultiPolygon(
            geos.GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))'),
            geos.GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))')
        )
    )

def generate_random_poly():
    random_number = random.randint(10, 20)
    return models.Polygon.objects.create(
        name="some random polygon %d" % random_number,
        raw=geos.GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))')
    )

def generate_random_point():
    random_number = random.randint(10, 20)
    return models.Point.objects.create(
        name="some random geometry %d" % random_number,
        raw=geos.Point(random.randint(100, 200), random.randint(100, 200))
    )

def generate_random_multipoint():
    random_number = random.randint(10, 20)
    return models.MultiPoint.objects.create(
        name="some random multipoint %d" % random_number,
        raw=geos.MultiPoint(
            geos.Point(random.randint(100, 200), random.randint(100, 200)),
            geos.Point(random.randint(100, 200), random.randint(100, 200))
        )
    )

def generate_random_linestring():
    random_number = random.randint(10, 20)
    return models.LineString.objects.create(
        name="some random linestring %d" % random_number,
        raw=geos.LineString((random_number, random_number), (random_number+20, random_number+20))
    )

def generate_random_multilinestring():
    random_number = random.randint(10, 20)
    return models.MultiLineString.objects.create(
        name="some random multilinestring %d" % random_number,
        raw=geos.MultiLineString(
            geos.LineString((random_number, random_number), (random_number+20, random_number+20)),
            geos.LineString((random_number, random_number), (random_number+20, random_number+20))
        )
    )

def generate_random_collection():
    random_number = random.randint(10, 20)
    return models.GeometryCollection.objects.create(
        name="some random geometrycollection %d" % random_number,
        raw=geos.GeometryCollection(
            geos.Point(random.randint(100, 200), random.randint(100, 200)),
            geos.LineString((random_number, random_number), (random_number+20, random_number+20)),
            geos.GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))')
        )
    )

def generate_random_region(geometry):
    random_number = random.randint(10, 20)
    return models.Region.objects.create(
        name="some random name %d" % random_number,
        slug="some/random/name/%d" % random_number,
        geometry=geometry
    )

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

    def test_allows_point_geometry(self):
        point = generate_random_point()
        region = generate_random_region(geometry=point)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, point)

    def test_allows_multipoint_geometry(self):
        multipoint = generate_random_multipoint()
        region = generate_random_region(geometry=multipoint)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, multipoint)

    def test_allows_polygon_geometry(self):
        poly = generate_random_poly()
        region = generate_random_region(geometry=poly)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, poly)

    def test_allows_multipolygon_geometry(self):
        multipoly = generate_random_multipoly()
        region = generate_random_region(geometry=multipoly)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, multipoly)

    def test_allows_linestring_geometry(self):
        linestring = generate_random_linestring()
        region = generate_random_region(geometry=linestring)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, linestring)

    def test_allows_multilinestring_geometry(self):
        multilinestring = generate_random_multilinestring()
        region = generate_random_region(geometry=multilinestring)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, multilinestring)

    def test_allows_geometrycollection_geometry(self):
        collection = generate_random_collection()
        region = generate_random_region(geometry=collection)
        self.assertEqual(models.Region.objects.get(pk=region.id).geometry, collection)

class TestOfRegionRelation(test.ModelTestCase):
    model_class = models.RegionRelation

    def setUp(self):
        super(TestOfRegionRelation, self).setUp()
        test.create_model_tables()

    def tearDown(self):
        super(TestOfRegionRelation, self).tearDown()
        test.destroy_model_tables()

    def test_ties_a_region_to_another_model(self):
        point = generate_random_point()
        region = generate_random_region(geometry=point)

        event = EventForRegionTesting.objects.create(name="foobar")
        relation = models.RegionRelation.objects.create(
            region=region,
            content_object=event
        )

        self.assertEqual(1, models.RegionRelation.objects.filter(region=region).count())

    def test_can_reach_through_relation(self):
        point = generate_random_point()
        region = generate_random_region(geometry=point)

        event = EventForRegionTesting.objects.create(name="foobar")
        relation = models.RegionRelation.objects.create(
            region=region,
            content_object=event
        )

        events = models.RegionRelation.objects.filter(region=region).return_related()
        self.assertEqual(1, events.count(), "sanity check")
        self.assertEqual(event, events[0])

class TestOfPoint(test.GeometryModelTestCase):
    model_class = models.Point
    expected_geometry = django_models.PointField

class TestOfPolygon(test.GeometryModelTestCase):
    model_class = models.Polygon
    expected_geometry = django_models.PolygonField

class TestOfMultiPoint(test.GeometryModelTestCase):
    model_class = models.MultiPoint
    expected_geometry = django_models.MultiPointField

class TestOfMultiPolygon(test.GeometryModelTestCase):
    model_class = models.MultiPolygon
    expected_geometry = django_models.MultiPolygonField

class TestOfLineString(test.GeometryModelTestCase):
    model_class = models.LineString
    expected_geometry = django_models.LineStringField

class TestOfMultiLineString(test.GeometryModelTestCase):
    model_class = models.MultiLineString
    expected_geometry = django_models.MultiLineStringField

class TestOfGeometryCollection(test.GeometryModelTestCase):
    model_class = models.GeometryCollection
    expected_geometry = django_models.GeometryCollectionField

