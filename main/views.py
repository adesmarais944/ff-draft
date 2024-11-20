import requests
import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Player, Team
from .forms import CreateNewTeam

# Create your views here.
def index(request):
    return HttpResponse("Yo")

# Players view: Deletes all Player records, retrieves Player data via API, and creates new Player records
def players(request):
    # Delete all existing Player objects from the database
    Player.objects.all().delete()
    # Define the URL for the API request
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    # Make the API request to get the player data
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        data = response.json()
        # Extract the list of players from the data
        players = data['players']
        
        # Iterate through the list of players and create new Player objects
        for player in players:
            Player.objects.create(
                name=player['name'],
                position=player['position'],
                adp=player['pick']
            )
        # Create a context dictionary with all Player objects to pass to the template
        context = {"collection": Player.objects.all()}
        # Render the 'home.html' template with the context data
        return render(request, "main/home.html", context)
    else:
        # Return an error message as JSON if the request failed
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)

def teams(request):
    if request.method == "POST":
        form = CreateNewTeam(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            p = form.cleaned_data["pos"]
            new_team = Team(name=n,draft_pos=p)
            new_team.save()
        return HttpResponse("Team Created!")

    else:
        form = CreateNewTeam()
    return render(request, "main/teams.html", {"form":form})