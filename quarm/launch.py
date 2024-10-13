#!/usr/bin/env python3

import psutil
import time
import subprocess

QUARM_LAUNCH_CMD = "env LUTRIS_SKIP_INIT=1 flatpak run net.lutris.Lutris lutris:rungameid/2"
PROCESS_NAME = "Everquest Quarm (TAKP 2.0)"

def launch_quarm():
    quarm = subprocess.Popen(QUARM_LAUNCH_CMD.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    if not quarm_is_running():
        raise Exception("Expected Quarm to be running by now, something is potentially wrong")

def quarm_is_running():
    found = False
    for process in psutil.process_iter():
        if PROCESS_NAME in process.name():
            found = True
            break
    return found
        
def main():
    launch_quarm()
    time.sleep(5)
    while quarm_is_running():
        time.sleep(10)

if __name__ == '__main__':
    main()
