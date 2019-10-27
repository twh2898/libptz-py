#!/usr/bin/env python3

from __future__ import print_function
import tkinter as tk
from tkinter import ttk
from ptz_widgets import PresetsWidget, PanWidget


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.scene = PresetsWidget(self)
        self.scene.pack(ipadx=4, ipady=4)

        self.control = PanWidget(self)
        self.control.pack()


def main():
    root = tk.Tk()
    root.title('PTZ Control')
    root.resizable(0, 0)

    app = App(root)
    app.pack()

    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting!')
