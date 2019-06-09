
from . import *
import logging
from urllib.request import urlopen


# API reference
# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


PTZ_URL = 'http://{addr}/cgi-bin/ptzctrl.cgi?{cmd}'


PAN_SPEED = Range('pan_speed', 1, 24)
TILT_SPEED = Range('tilt_speed', 1, 20)
PAN_LEFT = 'left'
PAN_RIGHT = 'right'
TILT_UP = 'up'
TILT_DOWN = 'down'
PAN_TILT_STOP = 'ptzstop'
_move_commands = Options('Move', [PAN_LEFT, PAN_RIGHT, TILT_UP, TILT_DOWN])

ZOOM_SPEED = Range('zoom_speed', 1, 7)
ZOOM_IN = 'zoomin'
ZOOM_OUT = 'zoomout'
ZOOM_STOP = 'zoomstop'
_zoom_commands = Options('Zoom', [ZOOM_IN, ZOOM_OUT])

FOCUS_SPEED = Range('focus_speed', 1, 7)
FOCUS_IN = 'focusin'
FOCUS_OUT = 'focusout'
FOCUS_STOP = 'focusstop'
_focus_commands = Options('focus', [FOCUS_IN, FOCUS_OUT])

PRESET_RANGE = Range('preset_num', 0, 89)
PRESET_CALL_COMMAND = 'poscall'
PRESET_SET_COMMAND = 'posset'


class PTZ:
    def __init__(self, addr='192.168.1.15'):
        self.addr = addr

    def _send(self, *args):
        command = '&'.join(['ptzcmd'] + list(args))
        request = PTZ_URL.format(addr=self.addr, cmd=command)
        logging.info(request)
        response = urlopen(request)
        logging.debug(response)

    def move(self, direction, pan_speed=1, tilt_speed=1):
        ensure_options(direction, _move_commands)
        ensure_range(pan_speed, PAN_SPEED)
        ensure_range(tilt_speed, TILT_SPEED)
        self._send(direction, str(pan_speed), str(tilt_speed))

    def move_stop(self):
        self._send(PAN_TILT_STOP, '1', '1')

    def zoom(self, direction, zoom_speed=1):
        ensure_options(direction, _zoom_commands)
        ensure_range(zoom_speed, ZOOM_SPEED)
        self._send(direction, str(zoom_speed))

    def zoom_stop(self):
        self._send(ZOOM_STOP, '1')

    def focus(self, direction, focus_speed=1):
        ensure_options(direction, _focus_commands)
        ensure_range(focus_speed, FOCUS_SPEED)
        self._send(direction, str(focus_speed))

    def focus_stop(self):
        self._send(FOCUS_STOP, '1')

    def preset(self, preset):
        ensure_range(preset, PRESET_RANGE)
        self._send(PRESET_CALL_COMMAND, str(preset))
