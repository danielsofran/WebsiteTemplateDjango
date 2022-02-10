from django import forms
from django.forms import ModelForm
from .models import *

# create a form
class ProdusForm(ModelForm):
    class Meta:
        model = Produs
        fields = "__all__"
