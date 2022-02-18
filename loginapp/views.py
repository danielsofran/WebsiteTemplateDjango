from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import context, OwnSettings
from .forms import *
from WebsiteTemplate import settings


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        try:
            user = get_user_model().objects.get(email=username)
        except:
            messages.success(request, ("Utilizator inexistent!"))
            return redirect('login')
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'login.html', {**context(OwnSettings.objects.first())})

def logout_user(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_superuser)
def admin_(request):
    if request.method == "GET":
        formgeneral = OwnSettingsForm
        formnavbar = NavbarForm
        formslideshow = SlideShowForm
        formgalerie = GalerieForm
        formfooter = FooterForm
        formcard = CardForm
        return render(request, "admingeneral.html", {"formgeneral": formgeneral, 'formnavbar' : formnavbar, 'formslideshow' : formslideshow, 'formgalerie' : formgalerie, 'formfooter' : formfooter, 'formcard' : formcard,  **context(OwnSettings.objects.first())})
    else: # request.POST["VIEW"]=="test":
        if "general" in request.POST:
            form = OwnSettingsForm(request.POST)
            if form.is_valid():
                OwnSettings.objects.all().delete()
                form.save()
        elif "navbar" in request.POST:
            form = NavbarForm(request.POST)
            if form.is_valid():
                NavbarSettings.objects.all().delete()
                form.save()
        elif "slideshow" in request.POST:
            form = SlideShowForm(request.POST)
            if form.is_valid():
                SlideShowSettings.objects.all().delete()
                form.save()
        elif "galerie" in request.POST:
            form = GalerieForm(request.POST)
            if form.is_valid():
                GalerieSettings.objects.all().delete()
                form.save()
        elif "footer" in request.POST:
            form = FooterForm(request.POST)
            if form.is_valid():
                FooterSettings.objects.all().delete()
                form.save()
        elif "card" in request.POST:
            form = CardForm(request.POST)
            if form.is_valid():
                CardSettings.objects.all().delete()
                form.save()
        messages.success(request, "Modificarile au fost efectuate!")
        return redirect('admin')

@user_passes_test(lambda u: u.is_superuser)
def test(request):
    if request.method == "GET":
        messages.success(request, "Versiune site de test.\n Numai dvs o puteti vedea.")
        return render(request, "test.html", {**context(OwnSettings.objects.last())})
    else: # save
        return redirect('admin')

@user_passes_test(lambda u: u.is_superuser)
def reset(request):
    OwnSettings.objects.all().delete()
    return redirect('admin')
