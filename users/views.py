from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import reverse

'''
class Signup(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        def __init__(self, *args, **kwargs):
            super(Signup, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 
            self.fields['username'].widget.attrs['placeholder'] = "Username"
            self.fields['email'].widget.attrs['class'] = 
            self.fields['email'].widget.attrs['placeholder'] = "Email Address"
            self.fields['password1'].widget.attrs['class'] = 
            self.fields['password2'].widget.attrs['placeholder'] = "Password"
            self.fields['password2'].widget.attrs['class'] = 
            self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password"

'''


def frontpage(request:HttpRequest):
    return render(request, "users/frontpage.html")

def signup(request:HttpRequest):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username = username).exists() or User.objects.filter(email= email).exists():
            return render(request, "users/signup.html", {'user_message': "This User already exists"})
        if password1 != password2:
            return render(request, "users/signup.html", {'password_message': "Passwords do not match"})
        
        user = User.objects.create_user(username= username, email= email)
        user.set_password(password1)
        user.save()
        return HttpResponseRedirect('signin')

    return render(request, "users/signup.html")


def signin(request:HttpRequest):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password= password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('home')
        else:
            return render(request, "users/signin.html", {'message': "Invlaid username or password"})
    return render(request, "users/signin.html")

def home(request:HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signin'))
    return render(request, "users/home.html")

def signout(request:HttpRequest):
    logout(request)
    return HttpResponseRedirect('signin')

def user(request:HttpRequest, username):
    user = User.objects.get(username= username)
    return render(request, "users/user.html", {'user': user})