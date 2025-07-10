from django.db import models

# Create your models here.


class City(models.Model):
    place_id = models.IntegerField(unique=True)
    data = models.JSONField(default=dict)
    last_update = models.DateTimeField(auto_now=True)
