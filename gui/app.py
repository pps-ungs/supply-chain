#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk

window = tk.Tk()

window.title("Supply Chain Optimization App")
window.geometry("800x600")

menu = tk.Menu(window)
item = tk.Menu(menu, tearoff=0)

item.add_command(label="Open", command=lambda: print("Open clicked"))
item.add_command(label="Quit", command=lambda: window.quit())
menu.add_cascade(label="App", menu=item)
window.config(menu=menu)

def on_button_click():
    print("Button clicked!")

button = tk.Button(window, text="Accept", command=on_button_click)
button.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", variable=progress_var, maximum=100)
progress_bar.pack(pady=20)

progress_var.set(0)

def update_progress():
    current_value = progress_var.get()
    if current_value < 100:
        progress_var.set(current_value + 10)
        window.after(1000, update_progress)
    else:
        print("Progress complete!")

start_button = tk.Button(window, text="Start Hill Climbing", command=update_progress)
start_button.pack(pady=10)

window.mainloop()
