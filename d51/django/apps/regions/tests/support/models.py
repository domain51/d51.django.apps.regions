from d51.django.apps.regions.models import Region
from django.db import models

class EventForRegionTesting(models.Model):
    name = models.CharField(max_length=50)

