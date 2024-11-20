import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Player
import json
from typing import List


# Create your views here.
def index(request):
    return HttpResponse("Yo")

'''
def player_api(request):
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)
    data = response.json()
    values = [data[]]
    return JsonResponse(data)
'''


def player_data(request):
    players = Player.objects.all()
    context = {"collection": players}
    return render(request, "main/home.html", context)