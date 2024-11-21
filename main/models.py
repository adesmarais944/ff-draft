# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    adp = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    draft_pos = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team", null=True)
    def __str__(self):
        return self.name

class Draft(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField("draft created")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="draft", null=True)
    def __str__(self):
        return self.name
    
class RosteredPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)