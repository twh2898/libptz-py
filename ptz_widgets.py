#!/usr/bin/env python3

from __future__ import print_function
try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    from Tkinter import ttk
import ptz_http

# https://ptzoptics.com/wp-content/uploads/2014/09/PTZOptics_TCP_UDP_CGI_Control-1.pdf


class Spinbox(ttk.Entry):
    def __init__(self, master=None, **kw):
        ttk.Entry.__init__(self, master, "ttk::spinbox", **kw)

    def set(self, value):
        self.tk.call(self._w, "set", value)

        
class PanWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        buttons = [
            ('Up', 0, 1, self.tilt_u_start),
            ('Down', 2, 1, self.tilt_d_start),
            ('Left', 1, 0, self.pan_l_start),
            ('Right', 1, 2, self.pan_r_start),
            ('Stop', 1, 1, self.stop)
            ]

        for text, r, c, action in buttons:
            b = Button(self, text=text)
            b.grid(row=r, column=c)
            b.bind("<ButtonPress>", action)
            b.bind("<ButtonRelease>", self.stop)

        Label(self, text='Pan:').grid(row=3, column=0)
        Label(self, text='Tilt:').grid(row=4, column=0)

        self.pan_speed = Spinbox(self, from_=1, to=24)
        self.pan_speed.grid(row=3, column=1, columnspan=2)
        self.pan_speed.set(10)
        self.tilt_speed = Spinbox(self, from_=1, to=20)
        self.tilt_speed.set(10)
        self.tilt_speed.grid(row=4, column=1, columnspan=2)

    def stop(self, e):
        ptz_http.move('ptzstop')
        
    def pan_l_start(self, e):
        pan_speed = int(self.pan_speed.get())
        ptz_http.move('left', pan_speed=pan_speed)
    def pan_r_start(self, e):
        pan_speed = int(self.pan_speed.get())
        ptz_http.move('right', pan_speed=pan_speed)
        
    def tilt_u_start(self, e):
        tilt_speed = int(self.tilt_speed.get())
        ptz_http.move('up', tilt_speed=tilt_speed)
    def tilt_d_start(self, e):
        tilt_speed = int(self.tilt_speed.get())
        ptz_http.move('down', tilt_speed=tilt_speed)


class PresetsWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.buttons = []
        presets = [
            (0, 'Announcements'),
            (1, 'Communion Blurred'),
            (2, 'Projector Screen'),
            (3, 'Sermon'),
            (4, 'Crowd and Screen'),
            (5, 'Communion Prep'),
            (6, 'Announcements')
        ]
        for i, name in presets:
            text = '{} - {}'.format(i, name)
            command = lambda i=i: self.locate(i)
            button = Button(self, text=text, command=command)
            button.pack(fill=X, expand=True)
            self.buttons.append(button)

    def locate(self, preset):
        ptz_http.preset(preset)


