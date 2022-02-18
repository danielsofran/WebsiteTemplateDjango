from django import forms
from django.db.models import BooleanField
from django.forms import ModelForm
from .models import *


class OwnSettingsForm(ModelForm):
    class Meta:
        model = OwnSettings
        fields = ('showprice', 'allowrating', 'title', 'productimagepath')
        # widgets = {k.name: forms.TextInput(attrs={'class': 'form-control'}) for k in NavbarSettings._meta.get_fields()
        #            if not isinstance(k, BooleanField)}

class NavbarForm(ModelForm):
    class Meta:
        model = NavbarSettings
        fields = '__all__'
        #widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in NavbarSettings._meta.get_fields() if not isinstance(k, BooleanField)}


class SlideShowForm(ModelForm):
    class Meta:
        model = SlideShowSettings
        fields = '__all__'
        #widgets = {k.name:forms.TextInput(attrs={'class':'form-control'}) for k in NavbarSettings._meta.get_fields() if not isinstance(k, BooleanField)}


class GalerieForm(ModelForm):
    class Meta:
        model = GalerieSettings
        fields = '__all__'
        # widgets = {k.name: forms.TextInput(attrs={'class': 'form-control'}) for k in NavbarSettings._meta.get_fields()
        #            if not isinstance(k, BooleanField)}

class FooterForm(ModelForm):
    class Meta:
        model = FooterSettings
        fields = '__all__'
        #widgets = {k.name: forms.TextInput(attrs={'class': 'form-control'}) for k in NavbarSettings._meta.get_fields()
                   #if not isinstance(k, BooleanField)}

class CardForm(ModelForm):
    class Meta:
        model = CardSettings
        fields = '__all__'
        #widgets = {k.name: forms.TextInput(attrs={'class': 'form-control'}) for k in NavbarSettings._meta.get_fields()
                   #if not isinstance(k, BooleanField)}
