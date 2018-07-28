from django import forms
from django.shortcuts import render, redirect
from .models import UserData
from django.contrib.auth import (
        authenticate,
        get_user_model,
        login,
        logout,

)


from .forms import UserLoginForm, UserRegisterForm ,UserDetails

# Create your views here.

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        #print(request.user.is_authenticated())
        request.session["username"]=username
        return redirect("/newscards/")


    return render(request, "accounts/form.html", {"form": form, "title":title})


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request,new_user)
        return redirect("/details/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "accounts/form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/newscards/")




def details_view(request):
    title = "Details"
    form = UserDetails(request.POST or None)
    if form.is_valid():
        UserData=form.save(commit=False)
        UserData.save()
        return redirect("/newscards/")

    context = {
        "form": form,
        "title": title
    }

    #return redirect("/newscards")

    return render(request, 'accounts/form.html', context)
