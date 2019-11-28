from django.contrib import admin
from .models import City
from .models import Camera
from .models import CameraHistory

# Register your models here.
admin.site.register(City)
admin.site.register(Camera)
# admin.site.register(CameraHistory)
