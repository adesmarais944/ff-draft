from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form":form})

def redirect_to_login(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        return redirect(reverse('drafts'))
    
def logout_view(request):
    logout(request)
    #message = "You've successfully logged out."
    #context = {"collection": message}
    return redirect(reverse('/accounts/login'))
