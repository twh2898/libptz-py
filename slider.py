#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk


def print_value(val):
    print(val)


root = tk.Tk()

scale = ttk.Scale(orient='horizontal', from_=0, to=10, command=print_value)
scale.pack()

root.mainloop()
