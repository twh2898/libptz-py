
from . import PTZError
import socket


# API reference
# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


def _word(n, w):
    return (n >> (w * 4)) & 0xF


class PTZ:
    def __init__(self, addr='192.168.1.15', port=5678):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((addr, port))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.s.close()
        self.s = None

    def _send(self, packet):
        self.s.send(packet)

    def zoom_stop(self):
        self._send([0x01, 0x04, 0x07, 0x00, 0xFF])

    def zoom_tele(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZError('Invalid Speed')
        self._send([0x01, 0x04, 0x07, 0x20 + speed, 0xFF])

    def zoom_wide(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZError('Invalid Speed')
        self._send([0x01, 0x04, 0x07, 0x30 + speed, 0xFF])

    def zoom_direct(self, position):
        if position < 0 or position > 0xFF:
            raise PTZError('Invalid Position')

        p = position
        self._send([0x01, 0x04, 0x47, _word(p, 3), _word(
            p, 2), _word(p, 1), _word(p, 0), 0xFF])

    def focus_stop(self):
        self._send([0x01, 0x04, 0x08, 0x00, 0xFF])

    def focus_far(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZError('Invalid Speed')
        self._send([0x01, 0x04, 0x08, 0x20 + speed, 0xFF])

    def focus_near(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZError('Invalid Speed')
        self._send([0x01, 0x04, 0x08, 0x30 + speed, 0xFF])

    def focus_af_auto(self):
        self._send([0x01, 0x04, 0x38, 0x02, 0xFF])

    def focus_af_manual(self):
        self._send([0x01, 0x04, 0x38, 0x03, 0xFF])

    def focus_af_toggle(self):
        self._send([0x01, 0x04, 0x38, 0x10, 0xFF])

    def focus_direct(self, focus):
        if focus < 0 or focus > 0xFF:
            raise 'Invalid Position'

        f = focus
        self._send([0x01, 0x04, 0x48, _word(f, 3), word(
            f, 2), _word(f, 1), _word(f, 0), 0xFF])
