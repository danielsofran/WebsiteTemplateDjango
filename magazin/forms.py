from django import forms
from django.db.models import BooleanField, FileField
from django.forms import ModelForm
from .models import *

class GeneralForm(ModelForm):
    class Meta:
        model = Produs
        fields = ("nume", "descriere", "stoc", "sters")
        widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in model._meta.get_fields() if not isinstance(k, (BooleanField, FileField))}

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'
        widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in model._meta.get_fields() if not isinstance(k, (BooleanField, FileField))}

class PretForm(ModelForm):
    class Meta:
        model = Pret
        fields = '__all__'
        widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in model._meta.get_fields() if not isinstance(k, (BooleanField, FileField))}
class ImaginiForm(ModelForm):
    class Meta:
        model = Imagini
        fields = '__all__'
        widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in model._meta.get_fields() if not isinstance(k, (BooleanField, FileField))}

class ImagineForm(ModelForm):
    class Meta:
        model = Imagine
        fields = '__all__'
        widgets = {k.name: forms.TextInput(attrs={'class': 'form-control'}) for k in model._meta.get_fields() if
                   not isinstance(k, (BooleanField, FileField))}
class SpecificatiiForm(ModelForm):
    class Meta:
        model = Specificatii
        fields = '__all__'
        widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in model._meta.get_fields() if not isinstance(k, (BooleanField, FileField))}
