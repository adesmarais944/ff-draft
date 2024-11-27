from django.db import models
from django.contrib.auth.models import User

class Draft(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="draft", null=True)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE, related_name="team")
    draft_pos = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team")
    def __str__(self):
        return self.name
    
class Player(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    adp = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name
    
class RosteredPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pick = models.IntegerField(default=0)
    def __str__(self):
        return(
            f"{self.draft} - "
            f"{self.team} - "
            f"{self.player} - "
            f"pick {self.pick}"
        )