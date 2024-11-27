from django.contrib import admin
from .models import Draft, Team, Player, RosteredPlayer

# Register your models here.
admin.site.register(Draft)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(RosteredPlayer)