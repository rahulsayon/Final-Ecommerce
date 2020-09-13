from django.shortcuts import render , redirect
from . forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import  User
from django.utils.http import is_safe_url
# Create your views here.
from accounts.models import GuestEmail

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {}
    context['form'] = form
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    print("redirect_pathredirect_path",redirect_path)
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {}
    context['form'] = form
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    print("redirect_pathredirect_path",redirect_path)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(username,password)
        if user is not None:
            print("user" , user)
            login(request,user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("error")
    return render(request, "accounts/login.html",context)



def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {}
    context['form'] = form
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        User.objects.create_user(username=username,email=email,password=password)
        return redirect('/login')
        print(form.cleaned_data)
    return render(request,"accounts/register.html",context)