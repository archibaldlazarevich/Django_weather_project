from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)


class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
