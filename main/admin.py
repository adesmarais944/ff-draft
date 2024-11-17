from django.contrib import admin
from.models import Player,Team,Draft,RosteredPlayer
# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Draft)
admin.site.register(RosteredPlayer)