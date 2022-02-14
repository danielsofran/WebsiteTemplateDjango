import os

from django.db.models import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from .models import Produs
from WebsiteTemplate import settings
# Create your views here.

def home(request):
    path = settings.ownsettings["slideshow"]["imgpath"]
    files = os.listdir(path)
    slideshowimages = [f'media/SlideShow/{imgname}' for imgname in files]
    return render(request, "home.html", {
        "firstimage": slideshowimages[0],
        "slideshowimages": slideshowimages[1:],
        "range": range(1, len(slideshowimages)),
        **settings.ownsettings.context(),
    })

def getlength(products, **kwargs):
    try:
        rez = products.filter(**kwargs)
        try: return len(rez)
        except: return 1
    except Exception as e: return 0

def isfilterok(produs, filter, genuri, marimi) -> bool:
    if filter["stoc"]=="in" and produs.stoc<=0:
        return False
    if filter["stoc"]=="redus" and produs.pret.reducere<=0:
        return False
    if filter["pret_max"] is not None and produs.pret.pret_final>filter["pret_max"]:
        return False
    if produs.specificatii.spalaremasina==False and filter["ch_spalare"]==True:
        return False

    skip_gen = True
    _genuri = []
    for gen in genuri:
        skip_gen &= not gen[2]
        if gen[2]: _genuri.append(gen[0])
    if not skip_gen and produs.specificatii.gen not in _genuri:
        return False

    skip_marime = True
    _marimi = []
    for marime in marimi:
        skip_marime &= not marime[2]
        if marime[2]: _marimi.append(marime[0])
    if not skip_marime and produs.specificatii.marime not in _marimi:
        return False

    return True

def galerie(request):
    _products = Produs.objects.filter(sters=False)
    nrprod = len(_products)
    numemarimi = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL"]
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
        'nrproduse': nrprod,
        "range5": range(1, 6),
        "marimi": marimi,
        "reduse": sum(produs.pret.reducere>0 for produs in _products),
        "prinstoc": sum(produs.stoc>0 for produs in _products),
        "genuri": genuri,
        **filtru,
        **settings.ownsettings.context(),
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
        **settings.ownsettings.context(),
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
    numemarimi = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL"]
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
            if "redus" in token or "reducere" in token:
                filter["stoc"] = "redus"
            try: token=int(token)
            except: pass
            else: filter["pret"] = int(token)
    if filter["nume"]=="": filter.pop("nume")
    filter = urlencode(filter)
    return HttpResponseRedirect("/galerie?"+filter)




