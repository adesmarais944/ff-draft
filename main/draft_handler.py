from .models import Team, DraftPlayer
from .timer import timer
from threading import Event

def autodraft_player(team, draft):
    draft_player = DraftPlayer.objects.filter(draft=draft, rostered=False).order_by('player__adp').first()
    if draft_player:
        draft_player.rostered = True
        draft_player.team = team
        draft_player.save()
        print(f"Auto-drafted {draft_player.player.name} for {team.name}")

def draft_handler(draft, event):
    teams = Team.objects.filter(draft=draft).order_by('draft_pos')
    time_per_pick = draft.time_per_pick

    for team in teams:
        if team.user:
            while not event.is_set():
                timer(time_per_pick, team, event, autodraft_callback=lambda t: autodraft_player(t, draft))
                if event.is_set():
                    break
            event.clear()
        else:
            autodraft_player(team, draft)