from django.shortcuts import render
from django.views import generic
from .models import City
from .models import Camera


# Create your views here.
def index(request):
    return render(request, 'edith/index.html')


def about(request):
    return render(request, 'edith/about.html')


class DetailView(generic.DetailView):
    model = City

    def get_queryset(self):
        return Camera.objects.all()
