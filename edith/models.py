from django.db import models


# Create your models here.
class City(models.Model):
    city_text = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.city_text


class Camera(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    camera_text = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.camera_text


class CameraHistory(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('updated at')
    status = models.FloatField()

    def __str__(self):
        return f'{self.camera} {self.timestamp} {self.status}'


class Agent(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name_text = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=10)

    def __str__(self):
        return self.name
