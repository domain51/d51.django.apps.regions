from d51.django.apps.regions import managers
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
    geometry = models.PointField()

class MultiPoint(AbstractGeometry):
    geometry = models.MultiPointField()

class Polygon(AbstractGeometry):
    geometry = models.PolygonField()

class MultiPolygon(AbstractGeometry):
    geometry = models.MultiPolygonField()

class LineString(AbstractGeometry):
    geometry = models.LineStringField()

class MultiLineString(AbstractGeometry):
    geometry = models.MultiLineStringField()

class GeometryCollection(AbstractGeometry):
    geometry = models.GeometryCollectionField()

class Region(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True)

    content_type = models.ForeignKey(
        generic_models.ContentType,
        limit_choices_to={'app_label':'regions', 'model__in':('point', 'shape')}
    )
    object_id = models.PositiveIntegerField()
    geometry = generic.GenericForeignKey()

    def __unicode__(self):
        return self.name
