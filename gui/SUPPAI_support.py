#! /usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/')))

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog
import db.config as dbconfig
import setup
from models.ant_colony import AntColony
from models.hill_climbing import HillClimbing
from models.random_restart import RandomRestart
import experiments.initial_x.initial_x as initial_x

import SUPPAI

_debug = True

def connect_to_database():
    file_path = filedialog.askopenfilename(
        title="Open database configuration file",
        filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
    )
    if file_path:
        # ay no sé cómo sería esto :(
        config = dbconfig.load_config(file_path, 'supply_chain')
        setup.create_database(config) # Acá rompe porque no existen más las funciones de ahí
        data = setup.read_database(config)
        F, S, P, E = data["F"], data["S"], data["P"], data["E"]
        print(f"INI file selected: {file_path}, data:", F, S, P, E )
    else:
        print("No file selected.")

def get_active_heuristic():
    return "Aguante Cristina!"

def run_aco(alpha, beta, rho, Q, tau_max, tau_min, num_prod_levels, num_ants, num_iterations):
    F, S, P, E = connect_to_database()
    model = AntColony(F, S, P, E, 
                    alpha=alpha, 
                    beta=beta, 
                    rho=rho,
                    Q= Q if Q else None,
                    tau_max= tau_max if tau_max else None,
                    tau_min= tau_min if tau_min else None,
                    num_prod_levels=num_prod_levels)
    solution = model.solve(num_ants=num_ants, max_iterations=num_iterations)
    return [solution["X"], solution["Z"]]

def run_rr(step, epsilon, num_iterations, num_restarts):
    F, S, P, E = connect_to_database()
    model = RandomRestart(F, S, P, E)
    x = initial_x.get_initial_X_from_most_probable_scenario(model, F, E)
    solution = model.solve(step=step, epsilon=epsilon, max_iterations_allowed=num_iterations, initial_X=x, max_restarts=num_restarts)
    return [solution["X"], solution["Z"]]

def run_hc(step, epsilon, num_iterations):
    F, S, P, E = connect_to_database()
    model = HillClimbing(F, S, P, E)
    x = initial_x.get_initial_X_from_most_probable_scenario(model, F, E)
    solution = model.solve(step=step, epsilon=epsilon, max_iterations_allowed=num_iterations, initial_X=x)
    return [solution["X"], solution["Z"]]

def about_app(root):
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x150")
    about_window.resizable(False, False)

    # Center contents
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
