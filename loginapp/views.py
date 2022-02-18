from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm

from loginapp.models import context_2
from magazin.forms import *
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
        formgeneral = OwnSettingsForm(initial=context_2(OwnSettings.objects.first()))
        formnavbar = NavbarForm(initial=context_2(NavbarSettings.objects.last()))
        formslideshow = SlideShowForm(initial=context_2(SlideShowSettings.objects.last()))
        formgalerie = GalerieForm(initial=context_2(GalerieSettings.objects.last()))
        formfooter = FooterForm(initial=context_2(GalerieSettings.objects.last()))
        formcard = CardForm(initial=context_2(CardSettings.objects.last()))
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

saved = {}
@user_passes_test(lambda u: u.is_superuser)
def modify(request):
    global saved
    if request.method == "GET":
        cdict = {}
        if 'produs' in request.GET:
            produs = Produs.objects.get(id=int(request.GET["produs"]))
            formgeneral = GeneralForm(initial=context_2(produs))
            if "rating" in saved: formrating = RatingForm(initial=context_2(saved["rating"]))
            else: formrating = RatingForm(initial=context_2(produs.rating))
            if "pret" in saved: formpret = PretForm(initial=context_2(saved["pret"]))
            else: formpret = PretForm(initial=context_2(produs.pret))
            if "card" in saved: formimagini = ImaginiForm(initial=context_2(saved["card"]))
            else: formimagini = ImaginiForm(initial=context_2(produs.imagini))
            if "specificatii" in saved: formspecificatii = SpecificatiiForm(initial=context_2(saved["specificatii"]))
            else: formspecificatii = SpecificatiiForm(initial=context_2(produs.specificatii))
            imgs = Imagine.objects.filter(colectie_id=produs.imagini.id)
            cdict["imglen"] = imgs.count()
            limg = []
            for img, i in zip(imgs.all(), range(imgs.count())):
                limg.append((img.img, i+1))
            cdict["imgs"] = limg
            cdict["rangeotherimgs"] = range(cdict["imglen"], 21)
            formimagine = ImagineForm
        else:
            formgeneral = GeneralForm
            if "rating" in saved: formrating = RatingForm(initial=context_2(saved["rating"]))
            else: formrating = RatingForm
            if "pret" in saved: formpret = PretForm(initial=context_2(saved["pret"]))
            else: formpret = PretForm
            if "card" in saved:
                formimagini = ImaginiForm(initial=context_2(saved["card"]))
                imgs = Imagine.objects.filter(colectie_id=saved["card"].id)
                cdict["imglen"] = imgs.count()
                limg = []
                for img, i in zip(imgs.all(), range(imgs.count())):
                    limg.append((img.img, i + 1))
                cdict["imgs"] = limg
                cdict["rangeotherimgs"] = range(cdict["imglen"], 21)
            else: formimagini = ImaginiForm
            if "specificatii" in saved: formspecificatii = SpecificatiiForm(initial=context_2(saved["specificatii"]))
            else: formspecificatii = SpecificatiiForm

        cdict.update({
            'formgeneral': formgeneral, 'formrating': formrating, 'formpret': formpret, 'formimagini': formimagini, 'formspecificatii': formspecificatii,
            **context(OwnSettings.objects.first())})
        if not "rangeotherimgs" in cdict:
            cdict["rangeotherimgs"] = range(1, 21)
        #cdict["produsul"] = produs
        return render(request, 'modify.html', cdict)
    else:
        if "general" in request.POST:
            produs = None
            qs = None
            if "produs" in request.GET:
                produs = Produs.objects.get(id=int(request.GET['produs']))
                qs = Produs.objects.filter(id=int(request.GET['produs']))
            if produs is None: # INSERT
                for key in ["rating", "pret", "card", "imgs", "specificatii"]:
                    if not key in saved:
                        messages.success(request, f"{key} nesetat!")
                        return redirect("modify")
                try:
                    createdict  = {
                        "nume" : request.POST['nume'],
                        "descriere" : request.POST['descriere'],
                        "stoc": int(request.POST['stoc']),
                        "sters": "sters" in request.POST,
                    }
                    createdict.update({
                        k: saved[k] for k in ["rating", "pret", "specificatii"]
                    })
                    createdict["imagini"] = saved["card"]
                    produs = Produs.objects.create(**createdict)
                    messages.success(request, "Produsul a fost adaugat!")
                    saved.clear()  # daca nu au fost erori, operatia s-a efectuat cu success
                    return redirect('modify')
                except Exception as e:
                    messages.success(request, "NU toate campurile au fost completate!")
                    print(e)
                    return redirect('modify')
            else:
                try:
                    createdict = {
                        "nume": request.POST['nume'],
                        "descriere": request.POST['descriere'],
                        "stoc": int(request.POST['stoc']),
                        "sters": "sters" in request.POST,
                    }
                    # createdict.update({
                    #     k: saved[k] for k in ["rating", "pret", "specificatii"]
                    # })
                    # createdict["imagini"] = produs.imagini
                    qs.all().update(**createdict)
                    messages.success(request, "Produsul a fost actualizat!")
                    saved.clear()  # daca nu au fost erori, operatia s-a efectuat cu success
                    return redirect('modify')
                except Exception as e:
                    messages.success(request, "Operatie nereusita!")
                    saved.clear()
                    print(e)
                    return redirect('modify')
        elif "rating" in request.POST:
            form = RatingForm(request.POST)
            if form.is_valid():
                if "produs" in request.GET:
                    qs = Produs.objects.filter(id=int(request.GET['produs']))
                    qs.all().update(rating=form.save())
                else: saved["rating"] = form.save()
            else:
                messages.success(request, "Rating invalid!")
                return redirect('modify')
        elif "pret" in request.POST:
            form = PretForm(request.POST)
            if form.is_valid():
                if "produs" in request.GET:
                    qs = Produs.objects.filter(id=int(request.GET['produs']))
                    qs.all().update(pret=form.save())
                else:
                    saved["pret"] = form.save()
            else:
                messages.success(request, "Pret invalid!")
                return redirect('modify')
        elif "imagini" in request.POST:
            iscard = False
            card = Produs.objects.get(id=int(request.GET['produs'])).imagini
            if "card" in request.FILES:
                if "produs" in request.GET:
                    qs = Produs.objects.filter(id=int(request.GET['produs']))
                    qs.all().update(imagini=Imagini.objects.create(card=request.FILES['card']))
                    card = qs.first().imagini
                    iscard = True
                else:
                    saved["card"] = Imagini.objects.create(card=request.FILES['card'])
                    iscard = True
            if iscard or "produs" in request.GET:
                for i in range(1, 21):
                    if f"img{i}" in request.FILES:
                        if "produs" in request.GET:
                            produs = Produs.objects.get(id=int(request.GET['produs']))
                            qs = Imagine.objects.filter(img=request.FILES[f"img{i}"])
                            image = Imagine.objects.create(img=request.FILES[f'img{i}'], colectie=card)
                            assert isinstance(card, Imagini)
                            ud = qs.all().update(img=image.img)
                        else:
                            saved["imgs"] = Imagine.objects.create(img=request.FILES[f'img{i}'], colectie=saved['card'])
            else:
                messages.success(request, "Nu aveti o imagine Card selectata!")
                return redirect('modify')
        elif "specificatii" in request.POST:
            form = SpecificatiiForm(request.POST)
            if form.is_valid():
                if "produs" in request.GET:
                    qs = Produs.objects.filter(id=int(request.GET['produs']))
                    qs.all().update(specificatii=form.save())
                else:
                    saved["specificatii"] = form.save()
            else:
                messages.success(request, "Specificatii invalide!")
                return redirect('modify')
        messages.success(request, "Setari partiale salvate!")
        return redirect("modify")
