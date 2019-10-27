
from __future__ import print_function
import tkinter as tk
from tkinter import ttk
import ptz_http


class Spinbox(ttk.Entry):
    def __init__(self, master=None, **kw):
        super().__init__(master, "ttk::spinbox", **kw)

    def set(self, value):
        self.tk.call(self._w, "set", value)


class PanWidget(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        buttons = [
            ('Up', 0, 1, self.tilt_u_start),
            ('Down', 2, 1, self.tilt_d_start),
            ('Left', 1, 0, self.pan_l_start),
            ('Right', 1, 2, self.pan_r_start),
            ('Stop', 1, 1, self.stop)
        ]

        for text, r, c, action in buttons:
            b = ttk.Button(self, text=text)
            b.grid(row=r, column=c)
            b.bind("<ButtonPress>", action)
            b.bind("<ButtonRelease>", self.stop)

        ttk.Label(self, text='Pan:').grid(row=3, column=0)
        ttk.Label(self, text='Tilt:').grid(row=4, column=0)

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


class PresetsWidget(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

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
            def command(i=i): return self.locate(i)
            button = ttk.Button(self, text=text, command=command)
            button.pack(fill='x', expand=True)
            self.buttons.append(button)

    def locate(self, preset):
        ptz_http.preset(preset)
