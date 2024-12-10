import time
from threading import Event

def timer(duration, team, event, autodraft_callback):
    start = time.time()
    while (time.time() - start) < duration:
        if event.is_set():
            event.clear()  # Reset the event
            return
        remaining = duration - (time.time() - start)
        print(f"Time remaining for {team.name}: {remaining:.2f} seconds", end='\r')
        time.sleep(1)

    print(f"\nTime's up for {team.name}!")
    autodraft_callback(team)  # Trigger auto-draft when timer elapses