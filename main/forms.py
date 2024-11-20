from django import forms
from .models import Team, Player, Draft, RosteredPlayer

class CreateNewTeam(forms.Form):
    positions = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    name = forms.CharField(label="Team Name", max_length=200)
    pos = forms.ChoiceField(label="Draft Position", choices=positions)

'''
class DraftPlayer(forms.Form):
    player = 
    draft = 
    team = 
'''