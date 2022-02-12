import os

from django.shortcuts import render
from .models import Produs
from WebsiteTemplate import settings
# Create your views here.

def home(request):
    path = settings.MEDIA_ROOT + "\\SlideShow\\"
    files = os.listdir(path)
    slideshowimages = [f'media/SlideShow/{imgname}' for imgname in files]
    return render(request, "home.html", {"slideshowimages": slideshowimages[1:], "range": range(1, len(slideshowimages))})

def galerie(request):
    products = list(Produs.objects.all())
    products = products * 12
    return render(request, "galerie.html", {'listaproduse': products, "range5": range(1, 6)})

def produs(request, id):
    produs = Produs.objects.get(id=id)
    images = produs.imagini.ColectieImagini.all()
    imglist = []
    for img in images:
        i = str(img).find("media")
        imglist.append("/" + str(img)[i:].replace("\\", "/"))
    images = imglist
    return render(request, "produs.html", {
        "produs": produs,
        "firstimage": images[0],
        "images": images[1:],
        "allimages": images,
        "allimagesindexes": zip(images[1:], range(2, len(images)+1)),
    })
