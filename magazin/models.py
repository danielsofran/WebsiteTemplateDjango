from django.db import models
from django.contrib.auth.models import User as UserAdmin

class Rating(models.Model):
    stars = models.IntegerField("Stele", default=0)
    count = models.IntegerField("Nr de feedback-uri", default=0)
    accesari = models.BigIntegerField("Numar de accesari", default=0)

    @property
    def value(self) -> float:
        return int(self.stars) / (5*int(self.count)) * 5
    def __str__(self):
        return str(self.value)

class Pret(models.Model):
    pret = models.FloatField("Pret", default=0)
    reducere = models.IntegerField("Reducere", default=0)

    def pret_final(self):
        return self.pret - self.pret * (self.reducere/100)
    def __str__(self):
        return str(self.pret)


class Imagine(models.Model):
    img = models.FileField("Card Image", upload_to="Products/", blank=False, null=True)
    def __str__(self):
        return self.img.path

class Imagini(models.Model):
    card = models.OneToOneField(Imagine, related_name="Card", blank=True, null=True, on_delete=models.CASCADE)
    images = models.ForeignKey(Imagine, related_name="Imagini", blank=True, on_delete=models.CASCADE, default="", null=True)
    def __str__(self):
        return self.card.img.path

class Specificatii(models.Model):
    marime = models.CharField("Mărime", default="XL", max_length=10)
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

    def in_stoc(self):
        return self.stoc > 0

    def is_last(self):
        return self.stoc == 1

    def __str__(self):
        return f"{self.nume}"

