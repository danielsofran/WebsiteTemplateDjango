from django.db import models
from django.contrib.auth.models import User as UserAdmin

class Rating(models.Model):
    stars = models.IntegerField("Stele", default=0)
    count = models.IntegerField("Nr de feedback-uri", default=1)
    accesari = models.BigIntegerField("Numar de accesari", default=0)

    @property
    def value(self) -> float:
        return int(self.stars) / (5*int(self.count)) * 5
    def __str__(self):
        return str(self.value)

class Pret(models.Model):
    pret = models.FloatField("Pret", default=0)
    reducere = models.FloatField("Reducere", default=0)

    @property
    def pret_final(self):
        return self.pret - self.pret * (self.reducere/100)
    def __str__(self):
        return str(self.pret_final)


class Imagini(models.Model):
    card = models.FileField("Card Image", upload_to="Products/", blank=False, null=True)
    def __str__(self):
        return self.card.path


class Imagine(models.Model):
    img = models.FileField("Image", upload_to="Products/", blank=False, null=True)
    colectie = models.ForeignKey(Imagini, related_name="ColectieImagini", blank=True, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.img.path


class Specificatii(models.Model):
    marime = models.CharField("Mărime", default="XL", max_length=10)
    gen = models.TextField("Gen", default="FEMEI", blank=False, null=False, choices=[("BARBATI", "BARBATI"), ("FEMEI", "FEMEI"), ("COPII", "COPII")])
    spalaremasina = models.BooleanField("Se spală la mașină", default=True)
    temperatura = models.IntegerField("Temperatura de spălare recomandată", default=60)
    timpspalare = models.CharField("Timpul de spălare recomandat", default="2h", max_length=10)
    def __str__(self):
        return self.marime


# class Recenzie(models.Model):
#     autor = None  # foreign key la user
#     data = models.DateField("Data recenzie", blank=True)
#     text = models.TextField("Text recenzie", blank=True, max_length=200)
#     stars = models.IntegerField("Stele", default=0)


class Produs(models.Model):
    id = models.AutoField("Id", primary_key=True)
    nume = models.CharField("Denumire", max_length=50, blank=False)
    descriere = models.TextField("Descriere", blank=True)
    stoc = models.IntegerField("Stoc", default=1)

    rating = models.OneToOneField(Rating, related_name="Rating", blank=True, null=True, on_delete=models.CASCADE)
    pret = models.OneToOneField(Pret, related_name="Pret", blank=True, null=True, on_delete=models.CASCADE)
    imagini = models.OneToOneField(Imagini, related_name="Imagini", null=True, on_delete=models.CASCADE)
    specificatii = models.OneToOneField(Specificatii, related_name="Specificatii", blank=False, null=True, on_delete=models.CASCADE)

    @property
    def in_stoc(self):
        return self.stoc > 0

    @property
    def is_last(self):
        return self.stoc == 1

    def __str__(self):
        return f"{self.nume}"

