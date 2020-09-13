from django.http import HttpResponse
from django.shortcuts import render , redirect
from . forms import ContactForm,LoginForm,RegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import  User


def home_page(request):
    # print(request.session['firstname'])
    print(request.session.get('firstname','Unknown'))
    context = {
        "title" : "This is About Page",
        "content" : "Home Page",
        "premium" : "You are Premium Member"
    }
    return render(request,"home_page.html",context)


def about_page(request):
    context = {
        "title" : "This is About Page",
        "content" : "About Page"
    }
    return render(request,"home_page.html",context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    context = {
        "title" : "This is About Page",
        "content" : "Wellcome The Contact Page",
        "form" : form
    }
    if form.is_valid():
        # print(request.POST.get('fullname'))
        print(form.cleaned_data)
    return render(request,"contact/view.html",context)

