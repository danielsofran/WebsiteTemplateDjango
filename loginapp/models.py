from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import OneToOneField, OneToOneRel, ManyToOneRel

from magazin.utils import isLight, stringtocolor
from WebsiteTemplate.settings import MEDIA_ROOT
from itertools import chain

# Create your models here.
class NavbarSettings(models.Model):
    title=models.CharField("Titlu", default=u"Ie \xa0Romanească", max_length=50)
    titlefont=models.CharField("Font", default="Alex Brush", max_length=40)
    fontmultiplier=models.IntegerField("Procent marime font titlu", default=200)
    titlecolor=models.CharField("Culoare titlu", default="0, 0, 0, 1", max_length=20)
    itemcolor=models.CharField("Culoare iteme", default="77, 77, 77, 0.8", max_length=20)
    itemhovercolor=models.CharField("Culoare iteme onhover", default="179, 179, 179, 0.9", max_length=20)
    color=models.CharField("Culoare de fundal", default="127, 255, 212, 0.95", max_length=20)
    hidelogin=models.BooleanField("Ascunde Loginul", default=False)

class SlideShowSettings(models.Model):
    imgpath=models.CharField("Folderul imaginilor din slideshow", default="SlideShow/", max_length=50)
    duration=models.IntegerField("Numarul de milisecunde per imagine", default=10000)
    maxheight=models.IntegerField("Intaltimea maxima a slideshow-ului", default=500)
    breakpoint=models.IntegerField("Slideshowul opreste animatia la ecrane mai mici de(px)", default=1000)

class FooterSettings(models.Model):
    title=models.CharField("Titlu", default=u"Art \xa0\xa0Traditional", max_length=30)
    titlefont=models.CharField("Font", default="Alex Brush", max_length=40)
    fontmultiplier=models.IntegerField("Multiplicator font(%)", default=200)
    fcolor=models.CharField("Colare text", default="255, 255, 255, 1", max_length=20)
    bgcolor=models.CharField("Culoare fundal", default="33, 37, 41, 1", max_length=20)
    credits=models.TextField("Text footer", default="Drepturi de autor © 2022. Toate drepturile rezervate", max_length=200)
    imgsource=models.CharField("Imagine", default="/media/BannerR.png", max_length=50)

class CardSettings(models.Model):
    color=models.CharField("Culoare fundal", default="255, 255, 255, 0", max_length=20)
    #islight
    titlecolor=models.CharField("Culoare titlu", default="0, 0, 0, 1", max_length=20)
    finalpricecolor=models.CharField("Culoare pret final", default="0, 0, 0, 1", max_length=20)
    reducerecolor=models.CharField("Culoare reducere", default="255, 26, 26, 1", max_length=20)
    initialpretcolor=models.CharField("Culoare pret initial", default="0, 0, 0, 1", max_length=20)
    starcolor=models.CharField("Culoare stele rating", default="255, 255, 0, 1", max_length=20)
    showtitle=models.BooleanField("Afiseaza numele", default=True)
    titlealign=models.CharField("Alinierea titlului", choices=[("center", "Centru"), ("end", "Dreapta"), ("start", "Stanga")], default="center", max_length=10)
    showprice=models.BooleanField("Afiseaza pret", default=True)
    showdescription=models.BooleanField("Afiseaza descrierea", default=True)
    showimage=models.BooleanField("Afiseaza imaginea produsului", default=True)
    specificatii=models.CharField("Specificatiile afisate", default="marime rating", max_length=30)

class GalerieSettings(models.Model):
    pretmin=models.IntegerField("Pret minim", default=50)
    pretmax=models.IntegerField("Pret maxim", default=2000)
    pas=models.IntegerField("Pas", default=50)

class OwnSettings(models.Model):
    showprice=models.BooleanField("Arata pret", default=True)
    allowrating=models.BooleanField("Permite rating", default=True)
    title=models.CharField("Titlul paginii", default="Art Traditional", max_length=20)
    productimagepath=models.CharField("Folderul unde se incarca imaginile produselor", default="Products/", max_length=20)
    # bindings
    # navbar=models.OneToOneField(NavbarSettings, on_delete=models.CASCADE, related_name="navbar")
    # slideshow=models.OneToOneField(SlideShowSettings, on_delete=models.CASCADE, related_name="slideshow")
    # footer=models.OneToOneField(FooterSettings, on_delete=models.CASCADE, related_name="footer")
    # card=models.OneToOneField(CardSettings, on_delete=models.CASCADE, related_name="card")
    # galerie=models.OneToOneField(GalerieSettings, on_delete=models.CASCADE, related_name="galerie")

def context_old(setare): # determina context dict-ul
    # get current setting
    rez = {}
    for field in OwnSettings._meta.get_fields():
        # print(field.name)
        if isinstance(field, OneToOneField):
            for field2 in setare._meta.get_field(field.name).related_model._meta.get_fields():
                if field2.name != field.name and field2.name != "id":
                    # print("\t"+field2.name)
                    # print("\t\t"+str(field2.value_from_object(getattr(setare, field.name))))
                    if "color" in field2.name:
                        rez[field.name+field2.name] = stringtocolor(str(field2.value_from_object(getattr(setare, field.name))))
                        rez[field.name+"islight"] = isLight(rez[field.name+field2.name])
                    else: rez[field.name+field2.name] = field2.value_from_object(getattr(setare, field.name))
        else: rez[field.name] = field.value_from_object(setare)
    return rez

def context_2(setare): # determina context dict-ul
    # get current setting
    rez = {}
    for field in setare._meta.get_fields():
        if isinstance(field, (OneToOneField, OneToOneRel, ManyToOneRel)) or field.name == "id": continue
        # print(field.name)
        # if isinstance(field, OneToOneField):
        #     obj = setare._meta.get_field(field.name).related_model.objects.last()
        #     for field2 in setare._meta.get_field(field.name).related_model._meta.get_fields():
        #         if field2.name != field.name and field2.name != "id":
        #             # print("\t"+field2.name)
        #             # print("\t\t"+str(field2.value_from_object(getattr(setare, field.name))))
        #             if "color" in field2.name:
        #                 #obj = asocs[field.name].objects.last()
        #                 rez[field.name + field2.name] = stringtocolor(str(field2.value_from_object(obj)))
        #                 # rez[field.name+field2.name] = stringtocolor(str(field2.value_from_object(getattr(setare, field.name))))
        #                 rez[field.name+"islight"] = isLight(rez[field.name+field2.name])
        #             else: rez[field.name+field2.name] = field2.value_from_object(obj)
        # else:
        rez[field.name] = field.value_from_object(setare)
    return rez

def context(setare): # determina context dict-ul
    # get current setting
    rez = {}
    asocs={"navbar":NavbarSettings, "card":CardSettings, "slideshow": SlideShowSettings, "galerie": GalerieSettings, "footer":FooterSettings}
    for field in OwnSettings._meta.get_fields():
        rez[field.name] = field.value_from_object(setare)
    for fieldname,obj in asocs.items():
        for field2 in obj._meta.get_fields():
            if field2.name != fieldname and field2.name != "id":
                # print("\t"+field2.name)
                # print("\t\t"+str(field2.value_from_object(getattr(setare, field.name))))
                if "color" in field2.name:
                    # obj = asocs[field.name].objects.last()
                    rez[fieldname + field2.name] = stringtocolor(str(field2.value_from_object(obj.objects.last())))
                    # rez[fieldname+field2.name] = stringtocolor(str(field2.value_from_object(getattr(setare, fieldname))))
                    rez[fieldname + "islight"] = isLight(rez[fieldname + field2.name])
                else:
                    rez[fieldname + field2.name] = field2.value_from_object(obj.objects.last())
    return rez
