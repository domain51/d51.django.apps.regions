from django.contrib.gis.db import models
from d51.django.apps.regions import managers

class Point(models.Model):
    name = models.CharField(max_length=250)
    geometry = models.PointField()

    def __unicode__(self):
        return self.name

class Polygon(models.Model):
    name = models.CharField(max_length=250)
    geometry = models.PolygonField()

    def __unicode__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name
