import requests
import json
from decimal import Decimal
from .models import Player

def players(request):
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players = data['players']

        for player in players:
            try:
                # Convert the 'pick' field to a decimal
                adp_value = Decimal(player['pick'])
            except (ValueError, Decimal.InvalidOperation):
                # Handle the error if conversion fails
                adp_value = Decimal(0)  # Default value or handle as needed

            # Update or create the player record
            Player.objects.update_or_create(
                api_id=player['playerId'],  # Match based on api_id
                defaults={
                    'name': player['name'],
                    'position': player['position'],
                    'adp': adp_value
                }
            )
            print(player['name'])