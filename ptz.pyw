#!/usr/bin/env python3

from __future__ import print_function
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from urllib.request import urlopen
import socket
import time
import ptz_http
from ptz_http import PTZError
from ptz_widgets import PresetsWidget, PanWidget

# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


class PTZ:
    def __init__(self, addr, port=5678):
        self.addr = addr
        self.port = port

        self.s = socket.socket(socekt.AF_INET, socket.SOCK_STREAM)
        self.s.connect((addr, port))

    def send(self, packet):
        self.s.send(packet)

    def zoom_stop(self):
        self.send([0x01, 0x04, 0x07, 0x00, 0xFF])

    def zoom_tele(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZException('Invalid Speed')
        self.send([0x01, 0x04, 0x07, 0x20 + speed, 0xFF])
        
    def zoom_wide(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZException('Invalid Speed')
        self.send([0x01, 0x04, 0x07, 0x30 + speed, 0xFF])

    def zoom_direct(self, position):
        if position < 0 or position > 0xFF:
            raise PTZException('Invalid Position')
        word = lambda n, w: (n >> (w * 4)) | 0x0F
        p = position
        self.send([0x01, 0x04, 0x47, word(p, 3), word(p, 2), word(p, 1), word(p, 0), 0xFF])

    def focus_stop(self):
        self.send([0x01, 0x04, 0x08, 0x00, 0xFF])

    def focus_far(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZException('Invalid Speed')
        self.send([0x01, 0x04, 0x08, 0x20 + speed, 0xFF])

    def focus_near(self, speed=3):
        if speed < 0 or speed > 7:
            raise PTZException('Invalid Speed')
        self.send([0x01, 0x04, 0x08, 0x30 + speed, 0xFF])

    def focus_af_auto(self):
        self.send([0x01, 0x04, 0x38, 0x02, 0xFF])

    def focus_af_manual(self):
        self.send([0x01, 0x04, 0x38, 0x03, 0xFF])

    def focus_af_toggle(self):
        self.send([0x01, 0x04, 0x38, 0x10, 0xFF])

    def focus_direct(self, focus):
        if focus < 0 or focus > 0xFF:
            raise 'Invalid Position'
        word = lambda n, w: (n >> (w * 4)) | 0x0F
        f = focus
        self.send([0x01, 0x04, 0x48, word(f, 3), word(f, 2), word(f, 1), word(f, 0), 0xFF])
        

class App(Frame):
    def __init__(self, master, default_ip='192.168.1.15'):
        Frame.__init__(self, master)

        self.buttons = []
        ## THIS IS THE BUTTON STUFFFFFFFFFF
        names = ['Announcements', 'Communion Blurred', 'Projector Screen', 'Sermon', 'Crowd and Screen', 'Communion Prep', 'Announcements']
        for i in range(7):
            button = Button(self, text=str(i) + ' - ' + names[i], command=lambda i=i: self.locate(i))
            button.pack(fill=X, expand=True)
            self.buttons.append(button)
        #self.addr_var = StringVar(self)
        #self.addr_var.set(default_ip)
        #Entry(self, textvar=self.addr_var).pack(fill=X, expand=True)
        #Button(self, text='send', command=self.locate).pack()

    def locate(self, preset):
        ptz_http.preset(preset)



def main():
    root = Tk()
    root.title('PTZ Control')
    root.resizable(0, 0)
    
    p = PresetsWidget(root)
    p.pack(ipadx=4, ipady=4)

    PanWidget(root).pack()
    
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting!')

