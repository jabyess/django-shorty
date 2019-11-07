from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Link(models.Model):
    long = models.URLField()
    short = models.URLField()

    def __str__(self):
        return self.long

class Stats(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="link")
    total_visits = models.IntegerField()
    visits = models.DateTimeField()

    def __str__(self):
        return self.total_visits
