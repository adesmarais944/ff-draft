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
    else:
        print(f"No more players to auto-draft for {team.name}.")

def draft_handler(draft, event):
    teams = Team.objects.filter(draft=draft).order_by('draft_pos')
    num_rounds = len(teams)
    time_per_pick = draft.time_per_pick
    
    for round_number in range(num_rounds):
        print(f"Starting round {round_number + 1}")
        if round_number % 2 == 0:
            current_order = teams
        else:
            current_order = reversed(teams)
        
        for team in current_order:
            if not DraftPlayer.objects.filter(draft=draft, rostered=False).exists():
                print("Draft complete! No more players left to draft.")
                return
            
            if team.user:
                print(f"{team.name}'s turn")
                timer(time_per_pick, team, event, autodraft_callback=lambda t: autodraft_player(t, draft))
            else:
                autodraft_player(team, draft)
            
            event.clear()

        print(f"Finished round {round_number + 1}")

    print("Draft complete!")