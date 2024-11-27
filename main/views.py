from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, DraftForm, DraftPlayerForm
from django import forms
from .models import Draft, Player, RosteredPlayer, Team

# Home page renders Drafts and facilitates new Draft/Team creation
def home(request):
    if request.user.is_authenticated:
        form = DraftForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            # Create the Draft object
            draft_name = form.cleaned_data['name']
            draft = Draft.objects.create(name=draft_name, user=request.user)
            
            # Get draft position from form
            draft_pos = form.cleaned_data['draft_pos']
            
            # Create the Team object with the specified draft position
            team = Team.objects.create(
                name=f"User Team for {draft.name}",
                draft=draft,
                draft_pos=draft_pos,
                user=request.user
            )
            
            messages.success(request, f"Draft {draft.name} created with your team in position {draft_pos}")
            return redirect('home')
        
        drafts = Draft.objects.all().order_by("-date")
        return render(request, 'home.html', {"drafts": drafts, "form": form})
    else:
        return render(request, 'home.html', {})

def draft(request, pk):
    draft = get_object_or_404(Draft, id=pk)
    
    if request.method == "POST":
        form = DraftPlayerForm(request.POST)
        if form.is_valid():
            player_id = request.POST.get('player')
            team_id = request.POST.get('team')

            player = get_object_or_404(Player, id=player_id)
            team = get_object_or_404(Team, id=team_id)
            
            # Create Rostered Player record
            rostered_player = RosteredPlayer.objects.create(
                draft=draft,
                team=team,
                player=player,
                pick=0  # Replace with logic to determine the correct pick if needed
            )
            messages.success(request, f"You have selected {rostered_player.player.name}!")
            return redirect('draft', pk=draft.id)
        else:
            print("Form is not valid")  # Debugging print
            print(form.errors)  # Print form errors for debugging
    
    players = Player.objects.all().order_by("adp")
    form = DraftPlayerForm()
    rostered_players = RosteredPlayer.objects.filter(draft=draft)
    
    return render(request, 'draft.html', {
        "draft": draft,
        "players": players,
        "form": form,
        "rostered_players": rostered_players
    })

def login_user(request):
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