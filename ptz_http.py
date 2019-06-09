#!/usr/bin/env python3

# API reference
# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf

from __future__ import print_function
from urllib.request import urlopen
import time

PTZ_ADDR = '192.168.1.15'
PTZ_URL = 'http://{addr}/cgi-bin/ptzctrl.cgi?{cmd}'


def send(*args):
    command = '&'.join(['ptzcmd'] + list(args))
    request = PTZ_URL.format(addr=PTZ_ADDR, cmd=command)
    print(request)
    response = urlopen(request)
    for line in response:
        print(line)
    

class PTZError(Exception):
    pass


def move(direction, pan_speed=1, tilt_speed=1):
    if not direction in ['up', 'down', 'left', 'right', 'ptzstop']:
        raise PTZError('Direction must be one of up, down, left, right, ptzstop')
    if not 0 < pan_speed < 25:
        raise PTZError('pan_speed must be on the range [1, 24]')
    if not 0 < tilt_speed < 21:
        raise PTZError('tilt_speed must be on the range [1, 20]')
    send(direction, str(pan_speed), str(tilt_speed))

def zoom(direction, zoom_speed=1):
    if not direction in ['zoomin', 'zoomout', 'zoomstop']:
        raise PTZError('Direction must be one of zoomin, zoomout, zoomstop')
    if not 0 < zoom_speed < 8:
        raise PTZError('zoom_speed must be on the range [1, 7]')
    send(direction, str(zoom_speed))

def focus(direction, focus_speed):
    if not direction in ['focusin', 'focusout', 'focusstop']:
        raise PTZError('Direction must be one of focusin, focusout, focusstop')
    if not 0 < focus_speed < 8:
        raise PTZError('focus_speed must be on the range [1, 7]')
    send(direction, str(focus_speed))

def preset(preset):
    if not 0 <= preset <= 89:
        raise PTZError('preset must be on the range [0, 89]')
    send('poscall', str(preset))
