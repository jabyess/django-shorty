from django.db import models
from datetime import datetime
from django.core.validators import URLValidator

# Create your models here.

class Link(models.Model):
    long = models.URLField()
    short = models.URLField()
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Long: {self.long} \n Short: {self.short}"

class Visit(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="link")
    visit = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.visit)
