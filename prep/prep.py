#!/usr/bin/env python3

import os
import time
import subprocess
import argparse

DEFAULT_DISPLAY = "eDP-1-1"
DEFAULT_XRANDR_MODE = "1920x1080"

def cmd(command, ignore_stderr=False):
    command_run = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = command_run.communicate()
    if len(stderr) > 0 and ignore_stderr is False:
        raise Exception(f"Command {command} returned stderr:\n{stderr.decode('ascii')}")
    return stdout.decode('ascii')

def xrandr_has_mode(mode):
    output = cmd("xrandr")
    for line in output.split('\n'):
        if mode in line:
            return True
    return False

def create_xrandr_mode(resolution):
    output = cmd(f"cvt {resolution}")
    for line in output.split('\n'):
        if line.startswith("Modeline"):
            newmode = line.replace("Modeline ", "")

    if not newmode:
        raise Exception("Variable 'newmode' wasn't successfully set.")

    cmd(f"xrandr --newmode {newmode}")
    cmd(f"xrandr --addmode {DEFAULT_DISPLAY} '1280x800_60.00'")

def set_xrandr_mode(mode):
    cmd(f"xrandr --output {DEFAULT_DISPLAY} --mode {mode}")

def unmute_audio():
    cmd("pactl set-sink-mute @DEFAULT_SINK@ false")

def mute_audio():
    cmd("pactl set-sink-mute @DEFAULT_SINK@ true")
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action='store_true')
    parser.add_argument("--teardown", action='store_true')
    args = parser.parse_args()

    if args.setup:
        if not xrandr_has_mode("1280x800_60.00"):
            create_xrandr_mode("1280 800")
        set_xrandr_mode("1280x800")
        unmute_audio()
    elif args.teardown:
        mute_audio()
        set_xrandr_mode(DEFAULT_XRANDR_MODE)

if __name__ == '__main__':
    main()
