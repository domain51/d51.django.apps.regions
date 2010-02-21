from django.contrib.gis.db import models
from d51.django.apps.regions import managers

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

    def __unicode__(self):
        return self.name
