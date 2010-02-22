from d51.django.apps.regions import managers
from d51.django.db.models.generic import managers as d51_generic_manager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes import models as generic_models
from django.contrib.gis.db import models

class AbstractGeometry(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class Point(AbstractGeometry):
    raw = models.PointField()

class MultiPoint(AbstractGeometry):
    raw = models.MultiPointField()

class Polygon(AbstractGeometry):
    raw = models.PolygonField()

class MultiPolygon(AbstractGeometry):
    raw = models.MultiPolygonField()

class LineString(AbstractGeometry):
    raw = models.LineStringField()

class MultiLineString(AbstractGeometry):
    raw = models.MultiLineStringField()

class GeometryCollection(AbstractGeometry):
    raw = models.GeometryCollectionField()

class Region(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True)

    content_type = models.ForeignKey(generic_models.ContentType)
    object_id = models.PositiveIntegerField()
    geometry = generic.GenericForeignKey()

    def __unicode__(self):
        return self.name

class RegionRelation(models.Model):
    name = models.CharField(max_length=250)
    region = models.ForeignKey(Region)

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(generic_models.ContentType)
    content_object = generic.GenericForeignKey()

    objects = d51_generic_manager.GenericRelationshipManager()

    def __unicode__(self):
        return self.name
