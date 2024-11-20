import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Player
import json
from typing import List


# Create your views here.
def index(request):
    return HttpResponse("Yo")

# Fetches player records stored in Player table
def player_data(request):
    players = Player.objects.all()
    context = {"collection": players}
    return render(request, "main/home.html", context)

# Purgres all Player records, retrieves Player data via API and creates new Player records
def player_data2(request):
    Player.objects.all().delete()
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        players = data['players']
        
        # Iterate through the players and create Player objects
        for player in players:
            Player.objects.create(
                name=player['name'],
                position=player['position'],
                adp=player['pick']
            )
        return JsonResponse({'message': 'Players created successfully'})
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
