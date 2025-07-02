#! /usr/bin/env python3
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/')))

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog
from tkinter import messagebox
import db.config as dbconfig
import setup
from models.ant_colony import AntColony
from models.hill_climbing import HillClimbing
from models.random_restart import RandomRestart
import experiments.initial_x.initial_x as initial_x

import SUPPAI

_debug = True

class Optimizer():

    def __init__(self):
        self.F = []
        self.S = []
        self.P = []
        self.E = []

        self.is_connected = False
        self.time_start = 0.0

    def connect_to_database(self):
        file_path = filedialog.askopenfilename(
            title="Open database configuration file",
            # initialdir=os.path.expanduser("~"),
            filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
        )
        if file_path:
            config = dbconfig.load_config(file_path, 'supply_chain')
            data = setup.read_database(config)
            self.F, self.S, self.P, self.E = data["F"], data["S"], data["P"], data["E"]
            self.is_connected = True
            print(f"[info] ini file read: {file_path}")
        else:
            print("?no file selected.")


    def run_aco(self, alpha, beta, rho, Q, tau_min, tau_max, num_prod_levels, num_ants, num_iterations, observer=None):
        model = AntColony(
            self.F, self.S, self.P, self.E,
            alpha=float(alpha), beta=float(beta), rho=rho,
            Q = int(Q) if Q else 100,
            tau_min = float(tau_min) if tau_min else 0.01,
            tau_max = float(tau_max) if tau_max else 10.0,
            num_prod_levels = int(num_prod_levels)
        )
        model.add_observer(observer)
        self.time_start = time.time()
        _ = model.solve(num_ants=int(num_ants), max_iterations=int(num_iterations))

    def run_rr(self, step, epsilon, num_iterations_hc, num_loops_wo_improvement, num_restarts, observer=None):
        model = RandomRestart(self.F, self.S, self.P, self.E)
        model.add_observer(observer)
        self.time_start = time.time()
        _ = model.solve(step=step, epsilon=epsilon if epsilon else 1e-12, max_iterations_allowed=num_iterations_hc, max_loops_without_improvement=num_loops_wo_improvement, max_restarts=num_restarts)

    def run_hc(self, step, epsilon, num_iterations, observer=None):
        model = HillClimbing(self.F, self.S, self.P, self.E)
        x = initial_x.get_initial_X_from_most_probable_scenario(model, self.F, self.E)
        model.add_observer(observer)
        self.time_start = time.time()
        _ = model.solve(step=step, epsilon=epsilon if epsilon else 1e-12, max_iterations_allowed=num_iterations, initial_X=x)


def about_app(root):
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x150")
    about_window.resizable(False, False)

    msg = "SUPPly chAIn Optimizer App\n\nCopyright © 2025 Ebertz, Rondelli, Soria"
    label = tk.Label(about_window, text=msg, justify="center", pady=20)
    label.pack()

    dismiss_button = tk.Button(about_window, text="Dismiss", command=about_window.destroy)
    dismiss_button.pack(pady=10)

    about_window.transient(root)
    about_window.grab_set()
    root.wait_window(about_window)


def show_license(root):
    license_window = tk.Toplevel(root)
    license_window.title("License")
    license_window.geometry("600x600")
    license_window.resizable(False, False)

    license_text = """
Copyright (c) 2025, Ebertz, Rondelli, Soria

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

    text_widget = tk.Text(license_window, wrap="word", padx=10, pady=10, font=("Aptos", 10))
    text_widget.insert("1.0", license_text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both")

    dismiss_button = tk.Button(license_window, text="Dismiss", command=license_window.destroy)
    dismiss_button.pack(pady=10)

    license_window.transient(root)
    license_window.grab_set()
    root.wait_window(license_window)

def show_database_error():
    messagebox.showerror(
        title="Database Connection Error",
        message="Please connect to an apropriate database first before running the heuristics.\n\nGo to File → Connect to database..."
    )

def main(*args):
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    global _top1, _w1
    _top1 = root
    _w1 = SUPPAI.MainWindow(_top1)
    root.mainloop()

if __name__ == '__main__':
    SUPPAI.start_up()
