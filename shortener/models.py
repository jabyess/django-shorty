from django.db import models

# Create your models here.

class Link(models.Model):
    long = models.URLField()
    short = models.URLField()

class Stats(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="link")
    total_visits = models.IntegerField()
    visits = models.DateTimeField()
