
from . import *
import socket


# API reference
# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


ZOOM_SPEED = Range('Zoom Speed', -8, 8)
ZOOM_POS = Range('Zoom Pos', 0, 0xFFFF)

FOCUS_SPEED = Range('Focus Speed', -8, 8)
FOCUS_POS = Range('Focus Pos', 0, 0xFFFF)

PAN_SPEED = Range('Pan Speed', -0x18, 0x18)
PAN_POS = Range('Pan Pos', 0, 0xFFFF)

TILT_SPEED = Range('Tilt Speed', -0x14, 0x14)
TILT_POS = Range('Tilt Pos', 0, 0xFFFF)

PRESET_RANGE = Range('Preset', 0, 254)


def _word(n, w):
    return (n >> (w * 4)) & 0xF


class PTZ:
    def __init__(self, addr='192.168.1.15', port=5678):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((addr, port))
        self.a = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.s.close()
        self.s = None

    def _send(self, packet):
        self.s.send([0x80 | (self.a & 0xF), 0x01] + packet + [0xFF])

    ### ZOOM ###

    def zoom_stop(self):
        self._send([0x04, 0x07, 0x00])

    def zoom(self, speed):
        '''-8 to 8, 0 is stop, - is wide, + is tel'''
        ensure_range(speed, ZOOM_SPEED)
        if speed == 0:
            return self.zoom_stop()
        elif speed < 0:
            speed = abs(speed) - 1
            speed = 0x20 | (abs(speed) & 0xF)
        else:
            speed = speed - 1
            speed = 0x30 | (speed & 0xF)
        self._send([0x04, 0x07, speed])

    def zoom_direct(self, pos):
        '''Zoom to potition 0 to 0xFFFF'''
        ensure_range(pos, ZOOM_POS)
        self._send([0x04, 0x47] + [_word(pos, 3-i) for i in range(4)] + [0xFF])

    ### FOCUS ###

    def focus_stop(self):
        self._send([0x04, 0x08, 0x00])

    def focus(self, speed):
        '''-8 to 8, 0 is stop, - is near, + is far'''
        ensure_range(
        if speed == 0:
            return self.focus_stop()
        elif speed < 0:
            speed=abs(speed) - 1
            speed=0x20 | (abs(speed) & 0xF)
        else:
            speed=speed - 1
            speed=0x30 | (speed & 0xF)
        self._send([0x04, 0x08, speed])

    def focus_direct(self, pos):
        ensure_range(pos, FOCUS_POS)
        self._send([0x04, 0x48] + [_word(pos, 3-i) for i in range(4)] + [0xFF])

    def focus_mode_auto(self):
        self._send([0x04, 0x38, 0x02])

    def focus_mode_manual(self):
        self._send([0x04, 0x38, 0x03])

    ### PAN/TILT ###

    def move_stop(self):
        self._send([0x06, 0x01, 0x01, 0x01, 0x03, 0x03])

    def move(self, pan_speed=0, tilt_speed=0):
        '''
        pan_speed: speed from -0x18 to 0x18 with 0 being stop,
        tilt_speed: speed from -0x14 to 0x14 with 0 being stop,
        '''
        ensure_range(pan_speed, PAN_SPEED)
        ensure_range(tilt_speed, TILT_RANGE)
        if pan_speed == 0:
            left=3
            pan_speed=1
        elif pan_speed < 0:
            left=1
            pan_speed=abs(pan_speed)
        else:
            left=2

        if tilt_speed == 0:
            up=3
            tilt_speed=1
        elif tilt_speed < 0:
            up=1
            tilt_speed=abs(tilt_speed)
        else:
            up=2

        self._send([0x06, 0x01, pan_speed, tilt_speed, left, up])

    def move_mode_abs(self, pan, tilt, pan_speed=0, tilt_speed=0):
        '''
        pan: pan position from 0 to 0xFFFF,
        tilt: tilt position from 0 to 0xFFFF,
        pan_speed: speed from -0x18 to 0x18 with 0 being stop,
        tilt_speed: speed from -0x14 to 0x14 with 0 being stop,
        '''
        ensure_range(pan, PAN_POS)
        ensure_range(tilt, TILT_POS)
        ensure_range(pan_speed, PAN_SPEED)
        ensure_range(tilt_speed, TILT_RANGE)
        if pan_speed == 0:
            left=3
            pan_speed=1
        elif pan_speed < 0:
            left=1
            pan_speed=abs(pan_speed)
        else:
            left=2

        if tilt_speed == 0:
            up=3
            tilt_speed=1
        elif tilt_speed < 0:
            up=1
            tilt_speed=abs(tilt_speed)
        else:
            up=2

        self._send([0x06, 0x02, pan_speed, tilt_speed] +
                [_word(pan, 3-i) for i in range(4)] +
                [_word(tilt, 3-i) for i in range(4)])


    def move_mode_rel(self, pan, tilt, pan_speed=0, tilt_speed=0):
        '''
        pan: pan position from 0 to 0xFFFF,
        tilt: tilt position from 0 to 0xFFFF,
        pan_speed: speed from -0x18 to 0x18 with 0 being stop,
        tilt_speed: speed from -0x14 to 0x14 with 0 being stop,
        '''
        ensure_range(pan, PAN_POS)
        ensure_range(tilt, TILT_POS)
        ensure_range(pan_speed, PAN_SPEED)
        ensure_range(tilt_speed, TILT_RANGE)
        if pan_speed == 0:
            left=3
            pan_speed=1
        elif pan_speed < 0:
            left=1
            pan_speed=abs(pan_speed)
        else:
            left=2

        if tilt_speed == 0:
            up=3
            tilt_speed=1
        elif tilt_speed < 0:
            up=1
            tilt_speed=abs(tilt_speed)
        else:
            up=2

        self._send([0x06, 0x03, pan_speed, tilt_speed] +
                [_word(pan, 3-i) for i in range(4)] +
                [_word(tilt, 3-i) for i in range(4)])

    def move_home(self):
        self._send([0x06, 0x04])


    ### MEMORY ###

    def mem_reset(self, preset):
        ensure_range(preset, PRESET_RANGE)
        self._send([0x04, 0x3F, 0x00, preset])

    def mem_set(self, preset):
        ensure_range(preset, PRESET_RANGE)
        self._send([0x04, 0x3F, 0x01, preset])

    def mem_recall(self, preset):
        ensure_range(preset, PRESET_RANGE)
        self._send([0x04, 0x3F, 0x02, preset])

    ### INQUIRE ###

    def get_zoom(self):
        self._send([0x09, 0x04, 0x47])
        packet = self.s.recv(7)
        y = (packet[0] >> 4) & 0xF
        pqrs = (packet[1] >> 4) & 0xF
        pqrs = (pqrs << 4) | ((packet[2] >> 4) & 0xF)
        pqrs = (pqrs << 4) | ((packet[3] >> 4) & 0xF)
        pqrs = (pqrs << 4) | ((packet[4] >> 4) & 0xF)
        return pqrs, y

    def get_focus(self):
        self._send([0x09, 0x04, 0x48])
        packet = self.s.recv(7)
        y = (packet[0] >> 4) & 0xF
        pqrs = (packet[1] >> 4) & 0xF
        pqrs = (pqrs << 4) | ((packet[2] >> 4) & 0xF)
        pqrs = (pqrs << 4) | ((packet[3] >> 4) & 0xF)
        pqrs = (pqrs << 4) | ((packet[4] >> 4) & 0xF)
        return pqrs, y

    def get_pos(self):
        self._send([0x09, 0x04, 0x48])
        packet = self.s.recv(7)
        y = (packet[0] >> 4) & 0xF
        wwww = (packet[1] >> 4) & 0xF
        wwww = (wwww << 4) | ((packet[2] >> 4) & 0xF)
        wwww = (wwww << 4) | ((packet[3] >> 4) & 0xF)
        wwww = (wwww << 4) | ((packet[4] >> 4) & 0xF)
        zzzz = (zzzz << 4) | ((packet[5] >> 4) & 0xF)
        zzzz = (zzzz << 4) | ((packet[6] >> 4) & 0xF)
        zzzz = (zzzz << 4) | ((packet[7] >> 4) & 0xF)
        zzzz = (zzzz << 4) | ((packet[8] >> 4) & 0xF)
        return wwww, zzzz, y
