#! /usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import setup
import db.config as dbconfig
# from models.ant_colony import AntColony
import SUPPAI

_debug = True

def connect_to_database():
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    data = setup.read_database(config)
    return data["F"], data["S"], data["P"], data["E"]
 

def get_active_heuristic():
    return "Aguante Cristina!"

def run_aco(alpha, beta, rho, Q, tau_max, tau_min, num_prod_levels, num_ants, num_iterations):
    F, S, P, E = connect_to_database()
    # model_aco = AntColony(F, S, P, E, 
    #                 alpha=alpha, 
    #                     beta=beta, 
    #                     rho=rho,
    #                     Q= Q if Q else None,
    #                     tau_max= tau_max if tau_max else None,
    #                     tau_min= tau_min if tau_min else None,
    #                     num_prod_levels=num_prod_levels)
    # solution = model_aco.solve(num_ants=num_ants, max_iterations=num_iterations)
    # return [solution["X"], solution["Z"]]
    return [[10, 10, 10, 10], 100]

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
