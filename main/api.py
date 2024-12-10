import requests
import json
from .models import Player

def players(request):
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players = data['players']

        for player in players:
            try:
                # Convert the 'pick' field to an integer
                adp_value = int(player['pick'])
            except ValueError:
                # Handle the error if conversion fails
                adp_value = 0  # Default value or handle as needed

            Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                adp=adp_value,
                api_id=player['playerId']  # Ensure the key 'playerId' is accessed correctly
            )
            print(player['name'])