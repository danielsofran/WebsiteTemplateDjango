from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from WebsiteTemplate.settings import ownsettings


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']  # or email?
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
        return render(request, 'login.html', {**ownsettings.context()})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('home')
