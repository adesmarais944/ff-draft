from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, DraftForm, DraftPlayerForm
from django import forms
from .models import Draft, Player, DraftPlayer, Team
from threading import Event, Thread
from .draft_handler import draft_handler

# Home page renders Drafts and facilitates new Draft/Team creation
def home(request):
    if request.user.is_authenticated:
        form = DraftForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            # Create the Draft object
            draft_name = form.cleaned_data['name']
            num_of_teams = form.cleaned_data['num_of_teams']
            time_per_pick = form.cleaned_data['time_per_pick']
            draft = Draft.objects.create(
                name=draft_name,
                user=request.user,
                num_of_teams=num_of_teams,
                time_per_pick=time_per_pick
            )
            
            # Get draft position from form
            user_draft_pos = form.cleaned_data['draft_pos']
            
            # Create the Team object with the specified draft position
            team = Team.objects.create(
                name=f"User Team for {draft.name}",
                draft=draft,
                draft_pos=user_draft_pos,
                user=request.user
            )

            # Create CPU teams for the draft
            for t in range(num_of_teams):
                Team.objects.create(
                   name=f"Team {t + 1} for {draft.name}",
                   draft=draft,
                   draft_pos=t + 1,
                   user=None
                )
            
            messages.success(request, f"Draft {draft.name} created with your team in position {user_draft_pos}")
            return redirect('home')
        
        drafts = Draft.objects.all().order_by("-date")
        return render(request, 'home.html', {"drafts": drafts, "form": form})
    else:
        return render(request, 'home.html', {})

draft_event = Event()  # Global event to control the timer

def draft(request, pk):
    draft = get_object_or_404(Draft, id=pk)
    
    if request.method == "POST":
        if 'start_draft' in request.POST:
            draft_thread = Thread(target=draft_handler, args=(draft, draft_event))
            draft_thread.start()
            messages.success(request, "Draft started!")
            return redirect('draft', pk=draft.id)

        form = DraftPlayerForm(request.POST)
        if form.is_valid():
            player_id = request.POST.get('player')
            team_id = request.POST.get('team')

            player = get_object_or_404(Player, id=player_id)
            team = get_object_or_404(Team, id=team_id)
            
            # Update existing Draft Player record
            draft_player = DraftPlayer.objects.filter(draft=draft, player=player).update(
                team=team,
                pick=0,  # Replace with logic to determine the correct pick
                rostered=True
            )
            draft_event.set()  # Trigger the event to reset the timer
            messages.success(request, f"You have selected {player.name}!")
            return redirect('draft', pk=draft.id)
        else:
            print("Form is not valid")
            print(form.errors)

    else:
        players = Player.objects.all().order_by("adp")
        for player in players:
            DraftPlayer.objects.get_or_create(
                draft=draft,
                player=player,
                defaults={'team': None, 'rostered': False}
            )
    
    draft_players = DraftPlayer.objects.filter(draft=draft, rostered=False)
    form = DraftPlayerForm()
    user_team = DraftPlayer.objects.filter(draft=draft, team__user=request.user, rostered=True)
    
    return render(request, 'draft.html', {
        "draft": draft,
        "form": form,
        "draft_players": draft_players,
        "user_team": user_team
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