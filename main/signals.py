from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Draft, Team

@receiver(post_save, sender=Draft)
def create_team(sender, instance, created, **kwargs):
    if created:
        team_name = f"User Team for {instance.name}"
        draft_pos = 1  # Replace with logic later
        Team.objects.create(name=team_name, draft=instance, draft_pos=draft_pos, user=instance.user)