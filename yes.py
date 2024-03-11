"""making this because windows has no yes command as far as I'm aware :p"""
import time
import sys
def yes(time, print=True):
    global e
    e=0
    while True:
        if print:
            print("yes")
        e += 1
try:
    currenttime = time.time()
    yes()
except KeyboardInterrupt:
    print(f"yes: {e} in {round(time.time()-currenttime, 3)} seconds.")
    sys.exit(0)
