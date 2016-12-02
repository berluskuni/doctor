from django.shortcuts import render, get_object_or_404
from .models import Service, Gallery, News

# Create your views here.


def home(request):
    context = {'service': Service.objects.all().order_by('label'),
               'gallery_img_1': get_object_or_404(Gallery, label=1),
               'gallery_img_2': get_object_or_404(Gallery, label=2),
               'gallery_img_3': get_object_or_404(Gallery, label=3),
               'news': News.objects.all().order_by('label')}
    return render(request, 'base.html', {'context': context})
