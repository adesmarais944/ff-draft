from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, DraftForm
from django import forms
from .models import Draft, Player
from datetime import datetime

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = DraftForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                draft = form.save(commit=False)
                draft.user = request.user
                #draft.date = datetime.now()
                draft.save()
                messages.success(request, ('Draft created!'))
                return redirect ('home')
        drafts = Draft.objects.all().order_by("-date")
        return render(request, 'home.html', {"drafts":drafts, "form":form})
    else:
        return render(request, 'home.html', {})
    
def draft(request, pk):
    draft = get_object_or_404(Draft, id=pk)
    if draft:
        players = Player.objects.all().order_by("adp")
        return render(request, 'draft.html', {"draft":draft, "players":players})

def login_user(request):
    print("yo")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have logged in.'))
            return redirect('home')
        else:
            messages.success(request, ('There was an issue logging in. Please try again.'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out.'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfully registered.'))
            return redirect('home')
    return render(request, 'register.html', {"form":form})