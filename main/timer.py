import time

def timer(duration, team):
    start = time.time()
    while (time.time() - start) < duration:
        remaining = duration - (time.time() - start)
        print(f"Time remaining for {team.name}: {remaining:.2f} seconds", end='\r')
        time.sleep(1)
    print(f"\nTime's up for {team.name}!")