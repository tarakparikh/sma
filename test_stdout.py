import sys
import time

def status(s):
        sys.stdout.write(s + " " * (78 - len(s)) + "\r")
        sys.stdout.flush()

for i in range(12):
        status("   AAAAAAAAAAAAAAAAAAAAAAAAAA  HELLLLLLLLLOOOOOO WORKLD")
        time.sleep(1)

status("done")

