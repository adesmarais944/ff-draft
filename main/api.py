import requests
import json
from .models import Player

def players(request):
    url = ""
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players = data['players']

        for player in players:
            Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                adp=player['pick'],
                api_id=['playerId']
            )