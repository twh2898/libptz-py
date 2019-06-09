
from . import *
import logging
from urllib.request import urlopen


# API reference
# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


PTZ_URL = 'http://{addr}/cgi-bin/ptzctrl.cgi?{cmd}'


PAN_SPEED = SpeedRange('pan_speed', 1, 24)
TILT_SPEED = SpeedRange('tilt_speed', 1, 20)
PAN_LEFT = 'left'
PAN_RIGHT = 'right'
TILT_UP = 'up'
TILT_DOWN = 'down'
PAN_TILT_STOP = 'ptzstop'
_move_commands = [PAN_LEFT, PAN_RIGHT, TILT_UP, TILT_DOWN]

ZOOM_SPEED = SpeedRange('zoom_speed', 1, 7)
ZOOM_IN = 'zoomin'
ZOOM_OUT = 'zoomout'
ZOOM_STOP = 'zoomstop'
_zoom_commands = [ZOOM_IN, ZOOM_OUT]

FOCUS_SPEED = SpeedRange('focus_speed', 1, 7)
FOCUS_IN = 'focusin'
FOCUS_OUT = 'focusout'
FOCUS_STOP = 'focusstop'
_focus_commands = [FOCUS_IN, FOCUS_OUT]

PRESET_MIN = 0
PRESET_MAX = 89
PRESET_CALL_COMMAND = 'poscall'
PRESET_SET_COMMAND = 'posset'


def _ensure_direction(value, options):
    if not value in options:
        raise PTZCommandError('direction', options)


def _ensure_speed_range(value, speed_range):
    if not speed_range.min <= value <= speed_range.max:
        raise PTZSpeedError(speed_range)


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
        _ensure_direction(direction, _move_commands)
        _ensure_speed_range(pan_speed, PAN_SPEED)
        _ensure_speed_range(tilt_speed, TILT_SPEED)
        self._send(direction, str(pan_speed), str(tilt_speed))
    
    def move_stop(self):
        self._send(PAN_TILT_STOP, '1', '1')

    def zoom(self, direction, zoom_speed=1):
        _ensure_direction(direction, _zoom_commands)
        _ensure_speed_range(zoom_speed, ZOOM_SPEED)
        self._send(direction, str(zoom_speed))
    
    def zoom_stop(self):
        self._send(ZOOM_STOP, '1')

    def focus(self, direction, focus_speed=1):
        _ensure_direction(direction, _focus_commands)
        _ensure_speed_range(focus_speed, FOCUS_SPEED)
        self._send(direction, str(focus_speed))
    
    def focus_stop(self):
        self._send(FOCUS_STOP, '1')

    def preset(self, preset):
        if not PRESET_MIN <= preset <= PRESET_MAX:
            raise PTZError('preset must be in the range [{}, {}]'.format(
                PRESET_MIN, PRESET_MAX))
        self._send(PRESET_CALL_COMMAND, str(preset))
