#! /usr/bin/env python3
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
import SUPPAI_support

_location = os.path.dirname(__file__)

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 
_activebackground = _bgcolor
_activebackground = 'red'

_style_code_ran = 0

_default_font = "-family {Segoe UI Variable} -size 10 -weight bold"

def _style_code():
    global _style_code_ran

    if _style_code_ran:
        return        

    try:
        # Themes not working good
        # Choose a theme
        theme = "page-dark"
        theme = "elegance"
        theme = "elegance"
        theme = "cornsilk-dark"
        theme = "viva perón"

        SUPPAI_support.root.tk.call('source', os.path.join(_location, 'themes', f"{theme}.tcl"))
        style = ttk.Style()
        style.theme_use(theme)
    except:
        print("?theme not found, using default theme")
        style = ttk.Style()
        style.theme_use('default')

    style.configure('.', font = _default_font)
    if sys.platform == "win32":
       style.theme_use('winnative')
    _style_code_ran = 1

class MainWindow:

    def _set_active_heuristic(self, heuristic):
        self._active_heuristic = heuristic
        print(f"[info] active heuristic: {self._active_heuristic}")

    def __init__(self, top=None):
        self._active_heuristic = "HC"  # Default heuristic

        top.geometry("800x600")
        top.minsize(800, 600)
        # top.maxsize(1351, 738)
        top.resizable(1,  1)
        top.title("SUPPAI")

        self.top = top

        self.menubar = tk.Menu(top,font=_default_font,bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        # File menu
        self.sub_menu0 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font,label='File',menu=self.sub_menu0, )
        self.sub_menu0.add_command(accelerator='CTRL+O', compound='left',font=_default_font,label='Connect to database...',command=lambda:SUPPAI_support.connect_to_database())
        self.sub_menu0.add_command(accelerator='CTRL+Q', compound='left' ,font=_default_font, label='Quit', command=self.top.quit)

        # Heuristics menu
        self.sub_menu1 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font,label='Heuristics',menu=self.sub_menu1, )

        self.TLabelframeHC = ttk.Labelframe(self.top)
        self.TLabelframeRR = ttk.Labelframe(self.top)
        self.TLabelframeACO = ttk.Labelframe(self.top)

        # \begin{TODO}
        self._set_active_heuristic("HC")
        if self._active_heuristic == "HC":
            self.sub_menu1.add_command(compound='left',font=_default_font, label='✔️ Hill Climbing', command=lambda:print("Viva Perón!"))
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Random Restart', command=lambda:print("Aguante Cristina!"))
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Ant Colony', command=lambda:self._set_active_heuristic("ACO"))
            self._show_HC()
            self.TLabelframeRR.destroy()
            self.TLabelframeACO.destroy()
        elif self._active_heuristic == "RR":
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Hill Climbing',)
            self.sub_menu1.add_command(compound='left',font=_default_font, label='✔️ Random Restart',)
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Ant Colony',)
            self.TLabelframeHC.destroy()
            self._show_RR()
            self.TLabelframeACO.destroy()
        elif self._active_heuristic == "ACO":
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Hill Climbing',)
            self.sub_menu1.add_command(compound='left',font=_default_font, label='Random Restart',)
            self.sub_menu1.add_command(compound='left',font=_default_font, label='✔️ Ant Colony',)
            self._show_ACO()
            self.TLabelframeHC.destroy()
            self.TLabelframeRR.destroy()
        else:
            print("?no heuristic active, defaulting to Hill Climbing")
        # \end{TODO}

        self.sub_menu12 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font, label='Help',menu=self.sub_menu12, )
        self.sub_menu12.add_command(compound='left',font=_default_font, label='Licence')
        self.sub_menu12.add_command(compound='left',font=_default_font, label='About')

        _style_code()
        self.TProgressbar1 = ttk.Progressbar(self.top)
        self.TProgressbar1.place(relx=0.025, rely=0.867, relwidth=0.95, relheight=0.0, height=19)
        self.TProgressbar1.configure(length="760")


    def _show_HC(self):
        TLabelframeARR = self._new_frame("Hill Climbing")
        label_parameters = ["Step", "Epsilon", "Number of iterations"]
        self._render_parameters(TLabelframeARR, label_parameters)
        label_results = ["X", "Z"]
        self._render_results(TLabelframeARR, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._run_HC, self._run_HC]
        self._render_buttons(buttons, actions)

    def _show_RR(self):
        TLabelframeARR = self._new_frame("Random Restart")
        label_parameters = ["Step", "Epsilon", "Number of iterations", "Number of restarts"]
        self._render_parameters(TLabelframeARR, label_parameters)
        label_results = ["X", "Z"]
        self._render_results(TLabelframeARR, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._run_RR, self._run_RR]
        self._render_buttons(buttons, actions)

    def _show_ACO(self):
        TLabelframeACO = self._new_frame("Ant Colony Optimization")
        label_parameters = ["Alpha", "Beta", "Rho", "Q", "Tau min", "Tau max", "Number of production level", "Number of ants", "Number of iterations"]
        self._render_parameters(TLabelframeACO, label_parameters)
        label_results = ["X", "Z"]
        self._render_results(TLabelframeACO, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._run_ACO, self._run_ACO]
        self._render_buttons(buttons, actions)

    def _run_HC(self):
        param_values = self._get_params_values()
        step = param_values[0]
        epsilon = param_values[0]
        num_terations = param_values[0]

        results_hc = SUPPAI_support.run_hc(step, epsilon, num_terations)
        self._update_output_results(results_hc)

    def _run_RR(self):
        param_values = self._get_params_values()
        step = param_values[0]
        epsilon = param_values[0]
        num_terations = param_values[0]
        num_restarts = param_values[0]

        results_rr = SUPPAI_support.run_rr(step, epsilon, num_terations, num_restarts)
        self._update_output_results(results_rr)

    def _run_ACO(self):
        param_values = self._get_params_values()
        alpha = param_values[0]
        beta = param_values[1]
        rho = param_values[2]
        Q = param_values[3]
        tau_min = param_values[4]
        tau_max = param_values[5]
        num_prod_levels = param_values[6]
        num_ants = param_values[7]
        num_iterations = param_values[8]

        results_aco = SUPPAI_support.run_aco(alpha, beta, rho, Q, tau_max, tau_min, num_prod_levels, num_ants, num_iterations)
        self._update_output_results(results_aco)

    def _get_params_values(self):
        param_values = []
        for _, entry_widget in enumerate(self.input_entries):
            value = entry_widget.get()
            param_values.append(value)
        return param_values

    def _update_output_results(self, results_data):
        for i, entry_widget in enumerate(self.output_entries):
            if i < len(results_data):
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(results_data[i]))
            else:
                entry_widget.delete(0, tk.END)

    def _new_frame(self, title):
        labelFrame = ttk.Labelframe(self.top)
        labelFrame.place(relx=0.025, rely=0.017, relheight=0.827, relwidth=0.953)
        labelFrame.configure(relief='')
        labelFrame.configure(text=title)
        return labelFrame

    def _render_buttons(self, label_buttons, commands):
        initial_relax = 0.75
        relax_increment = 0.125
        for i in range (len(label_buttons)):
            TButton = ttk.Button(self.top)
            TButton.place(relx=initial_relax, rely=0.917, height=30, width=83)
            TButton.configure(takefocus="")
            TButton.configure(text=label_buttons[i])
            TButton.configure(compound='left')
            TButton.configure(command=commands[i])
            initial_relax += relax_increment

    def _render_results(self, frame, label_results):
        frame = ttk.Labelframe(frame)
        frame.place(relx=0.512, rely=0.081, relheight=0.861, relwidth=0.459, bordermode='ignore')
        frame.configure(relief='')
        frame.configure(text='''Results''')
        self.output_entries = []
        self.output_labels = []
        initial_rely = 0.068
        rely_increment = 0.094
        for label in label_results:
            result_label = ttk.Label(frame)
            result_label.place(relx=0.029, rely=initial_rely, height=20, width=150, bordermode='ignore')
            result_label.configure(font=_default_font)
            result_label.configure(relief="flat")
            result_label.configure(anchor='e')
            result_label.configure(text=label)
            result_label.configure(compound='left')
            self.output_labels.append(result_label)
            result_entry = ttk.Entry(frame)
            result_entry.place(relx=0.486, rely=initial_rely, relheight=0.054, relwidth=0.469, bordermode='ignore')
            result_entry.configure(cursor="xterm")
            result_entry.configure(font=_default_font)
            self.output_entries.append(result_entry)
            initial_rely += rely_increment

    def _render_parameters(self, frame, label_parameters):
        frame = ttk.Labelframe(frame)
        frame.place(relx=0.026, rely=0.081, relheight=0.861, relwidth=0.459, bordermode='ignore')
        frame.configure(relief='')
        frame.configure(text='''Parameters''')
        self.input_entries = []
        self.input_labels = []
        initial_rely = 0.068
        rely_increment = 0.094
        for label in label_parameters:
            result_label = ttk.Label(frame)
            result_label.place(relx=0.029, rely=initial_rely, height=20, width=150, bordermode='ignore')
            result_label.configure(font=_default_font)
            result_label.configure(relief="flat")
            result_label.configure(anchor='e')
            result_label.configure(text=label)
            result_label.configure(compound='left')
            self.input_labels.append(result_label)
            result_entry = ttk.Entry(frame)
            result_entry.place(relx=0.486, rely=initial_rely, relheight=0.054, relwidth=0.469, bordermode='ignore')
            result_entry.configure(cursor="xterm")
            result_entry.configure(font=_default_font)
            self.input_entries.append(result_entry)
            initial_rely += rely_increment

def start_up():
    SUPPAI_support.main()

if __name__ == '__main__':
    SUPPAI_support.main()
