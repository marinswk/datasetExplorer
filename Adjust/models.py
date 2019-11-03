from django.db import models


class Dataset(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=25)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=10)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()
