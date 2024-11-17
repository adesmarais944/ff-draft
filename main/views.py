import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.
def index(request):
    return HttpResponse("Yo")

def player_data(request):
    url = "https://api.fantasynerds.com/v1/nfl/adp?apikey=TEST&teams=&format=half"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)