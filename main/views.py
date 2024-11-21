import requests
import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Player, Team, Draft
from .forms import CreateNewTeam, CreateDraft
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, "main/base.html", {})

# Players view: Deletes all Player records, retrieves Player data via API, and creates new Player records
def players(request):
    Player.objects.all().delete()
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        players = data['players']

        for player in players:
            Player.objects.create(
                name=player['name'],
                position=player['position'],
                adp=player['pick']
            )
        context = {"collection": Player.objects.all()}
        return render(request, "main/home.html", context)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)

# Teams view: Handles form submission to create a new team.
def teams(request):
    if request.method == "POST":
        form = CreateNewTeam(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            p = form.cleaned_data["pos"]
            new_team = Team(name=n,draft_pos=p)
            new_team.save()
            request.user.team.add(new_team)
        return HttpResponse("Team Created!")
    else:
        form = CreateNewTeam()
    return render(request, "main/teams.html", {"form":form})

# Drafts view: Handles form submission to create a new draft.
def drafts(request):
    if request.method == "POST":
        form = CreateDraft(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            d = datetime.datetime.now()
            new_draft = Draft(name=n,date=d)
            new_draft.save()
            request.user.draft.add(new_draft)
        return players(request)
    else:
        form = CreateDraft()
    return render(request, "main/drafts.html", {"form":form})

def view(request):
    return render(request, "main/view.html", {})

def login_user(request):
    pass

def logout_user(request):
    pass