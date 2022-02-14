import os

from django.db.models import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from .models import Produs
from WebsiteTemplate import settings
from WebsiteTemplate.settings import ownsettings
from .utils import isfilterok, getlength
# Create your views here.

def home(request):
    path = ownsettings["slideshow"]["imgpath"]
    files = os.listdir(path)
    slideshowimages = [f'media/SlideShow/{imgname}' for imgname in files]
    return render(request, "home.html", {
        "firstimage": slideshowimages[0],
        "slideshowimages": slideshowimages[1:],
        "range": range(1, len(slideshowimages)),
        **ownsettings.context(),
    })

def galerie(request):
    _products = Produs.objects.filter(sters=False)
    nrprod = len(_products)
    numemarimi = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL"]
    numegenuri = ["Barbati", "Femei", "Copii"]
    marimi = []
    genuri = []
    try: pret = int(request.GET["pret"])
    except: pret = None
    try: stoc = request.GET["stoc"]
    except: stoc="tot"
    filtru = {
        "stoc": stoc,
        "pret_max": pret,
        "ch_spalare": "spalare" in request.GET,
    }
    for marime in numemarimi:
        marimi.append((marime, getlength(_products, specificatii__marime=marime), "marime"+marime in request.GET))
    for gen in numegenuri:
        genuri.append((gen, getlength(_products, specificatii__gen=gen), "gen"+gen in request.GET))

    products = []
    for product in _products:
        if isfilterok(product, filtru, genuri, marimi):
            products.append(product)

    if "nume" in request.GET:
        l = []
        for product in products:
            for token in request.GET['nume'].split():
                if product.nume.casefold() in token or token in product.nume.casefold():
                    l.append(product)
        products = l

    return render(request, "galerie.html", {
        'listaproduse': list(products)*12,
        "noresult": len(products) == 0,
        'nrproduse': nrprod,
        "range5": range(1, 6),
        "reduse": sum(produs.pret.reducere>0 for produs in _products),
        "prinstoc": sum(produs.stoc>0 for produs in _products),
        "marimi": marimi,
        "genuri": genuri,
        "cardshowmarime": "marime" in ownsettings['card']['specificatii'],
        "cardshowgen": "gen" in ownsettings['card']['specificatii'],
        "cardshowrating": "rating" in ownsettings['card']['specificatii'],
        **filtru,
        **ownsettings.context(),
    })

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
        "allimages": images,
        "allimagesindexes": zip(images[1:], range(2, len(images)+1)),
        "range5": range(5),
        **ownsettings.context(),
    })

def rateprodus(request, id):
    produs = Produs.objects.get(id=id)
    produs.rating.count += 1
    produs.rating.stars += int(request.GET['stars'])
    produs.rating.save()
    return HttpResponseRedirect(f'/galerie/{id}')

def search(request):
    text = request.GET["text"]
    products = Produs.objects.filter(sters=False)
    numemarimi = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL"]
    numegenuri = ["Barbati", "Femei", "Copii"]
    numegenuri = [x.casefold() for x in numegenuri]
    numemarimi = [x.casefold() for x in numemarimi]
    tokens = text.split()
    filter = {"stoc": "tot", "nume": ""}
    for product in products:
        for token in tokens:
            token = token.casefold()
            if product.nume.casefold() in token or token in product.nume.casefold():
                filter["nume"] += token + " "
            for gen in numegenuri:
                if gen == token:
                    filter["gen"+gen[0].upper()+gen[1:]] = "on"
            for marime in numemarimi:
                if marime == token:
                    filter["marime"+marime.upper()] = "on"
            if ownsettings['showprice']:
                if "redus" in token or "reducere" in token:
                    filter["stoc"] = "redus"
                try: token=int(token)
                except: pass
                else: filter["pret"] = int(token)
    if filter["nume"]=="": filter.pop("nume")
    filter = urlencode(filter)
    return HttpResponseRedirect("/galerie?"+filter)




