#! /usr/bin/env python3
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox
import os.path
import SUPPAI_support
from observer import Observer

_location = os.path.dirname(__file__)

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 
_activebackground = _bgcolor

_style_code_ran = 0

_default_font = "-family {Segoe UI Variable} -size 10 -weight normal"

def _style_code():
    global _style_code_ran

    if _style_code_ran:
        return

    style = ttk.Style()
    style.configure('.', font = _default_font)
    print(style.theme_names())

    if sys.platform == "win32":
       style.theme_use('vista')
    elif sys.platform == "darwin":
         style.theme_use('aqua')
    else:
        style.theme_use('default')

    _style_code_ran = 1


class MainWindow(Observer):

    def _set_active_heuristic(self, heuristic):
        self._active_heuristic = heuristic
        self._update_heuristic_display()
        self._update_heuristic_menu_checkmark()

    def __init__(self, top=None):
        self.optimizer = SUPPAI_support.Optimizer()
        self.top = top
        self._active_heuristic = ""
        self.max_iterations = 0

        top.geometry("800x600")
        top.minsize(800, 600)
        top.resizable(1,  1)
        top.title("SUPPAI")

        self.TProgressbar1 = ttk.Progressbar(self.top)
        self.TProgressbar1.place(relx=0.025, rely=0.867, relwidth=0.95, relheight=0.0, height=19)
        self.TProgressbar1.configure(length="760")
        self.TProgressbar1.configure(value=0)

        self.menubar = tk.Menu(top,font=_default_font,bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        # File menu
        self.sub_menu0 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font,label='File',menu=self.sub_menu0, )
        self.sub_menu0.add_command(compound='left',font=_default_font,label='Connect to database...',command=lambda:self.optimizer.connect_to_database())
        self.sub_menu0.add_command(compound='left' ,font=_default_font, label='Quit', command=self.top.quit)

        # Heuristics menu
        self.sub_menu1 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font,label='Heuristics',menu=self.sub_menu1, )

        # Labelframes
        self.TLabelframeHC = self._new_frame("Hill Climbing")
        self.TLabelframeRR = self._new_frame("Random Restart")
        self.TLabelframeACO = self._new_frame("Ant Colony Optimization")

        self._setup_heuristic_menu()
        self._update_heuristic_display() 

        # Licence menu
        self.sub_menu12 = tk.Menu(self.menubar, activebackground=_activebackground,activeforeground='black',font=_default_font,tearoff=0)
        self.menubar.add_cascade(compound='left',font=_default_font, label='Help',menu=self.sub_menu12, )
        self.sub_menu12.add_command(compound='left',font=_default_font, label='Licence', command=lambda:SUPPAI_support.show_license(self.top))
        self.sub_menu12.add_command(compound='left',font=_default_font, label='About', command=lambda:SUPPAI_support.about_app(self.top))

        _style_code()

        self._set_active_heuristic("HC")


    def _setup_heuristic_menu(self):
        self.sub_menu1.add_command(compound='left',font=_default_font, label='Hill Climbing', command=lambda:self._set_active_heuristic("HC"))
        self.sub_menu1.add_command(compound='left',font=_default_font, label='Random Restart', command=lambda:self._set_active_heuristic("RR"))
        self.sub_menu1.add_command(compound='left',font=_default_font, label='Ant Colony', command=lambda:self._set_active_heuristic("ACO"))


    def _update_heuristic_menu_checkmark(self):
        self.sub_menu1.delete(0, tk.END)
        self.sub_menu1.add_command(
            compound='left',
            font=_default_font,
            label='✔️ Hill Climbing' if self._active_heuristic == "HC" else 'Hill Climbing',
            command=lambda:self._set_active_heuristic("HC")
        )
        self.sub_menu1.add_command(
            compound='left',
            font=_default_font,
            label='✔️ Random Restart' if self._active_heuristic == "RR" else 'Random Restart',
            command=lambda:self._set_active_heuristic("RR")
        )
        self.sub_menu1.add_command(
            compound='left',
            font=_default_font,
            label='✔️ Ant Colony' if self._active_heuristic == "ACO" else 'Ant Colony',
            command=lambda:self._set_active_heuristic("ACO")
        )


    def _update_heuristic_display(self):
        self.TLabelframeHC.place_forget()
        self.TLabelframeRR.place_forget()
        self.TLabelframeACO.place_forget()

        self.TProgressbar1.stop()
        self.TProgressbar1.configure(mode="determinate", value=0)

        if self._active_heuristic == "RR":
            self.TLabelframeRR.place(relx=0.025, rely=0.017, relheight=0.827, relwidth=0.953)
            self._show_RR()
        elif self._active_heuristic == "ACO":
            self.TLabelframeACO.place(relx=0.025, rely=0.017, relheight=0.827, relwidth=0.953)
            self._show_ACO()
        else:
            self.TLabelframeHC.place(relx=0.025, rely=0.017, relheight=0.827, relwidth=0.953)
            self._show_HC()


    def _show_HC(self):
        self.TLabelframeHC = self._new_frame("Hill Climbing")
        label_parameters = ["Step", "Epsilon", "Maximum iterations"]
        self._render_parameters(self.TLabelframeHC, label_parameters)
        label_results = [ "X", "Z", "margin", "pStk", "pDIn", "CTf2s", "CTs2p", "Iteration number" ]
        self._render_results(self.TLabelframeHC, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._abort, self._run_HC]
        self._render_buttons(buttons, actions)


    def _show_RR(self):
        self.TLabelframeRR = self._new_frame("Random Restart")
        label_parameters = ["Step", "Epsilon", "Maximum iterations HC", "Loops w/o improvement", "Maximum restarts"]
        self._render_parameters(self.TLabelframeRR, label_parameters)
        label_results = [ "X", "Z", "margin", "pStk", "pDIn", "CTf2s", "CTs2p", "Iteration number" ]
        self._render_results(self.TLabelframeRR, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._abort, self._run_RR]
        self._render_buttons(buttons, actions)


    def _show_ACO(self):
        self.TLabelframeACO = self._new_frame("Ant Colony Optimization")

        label_parameters = ["α", "β", "ρ", "Q", "τ min", "τ max", "Production levels", "Number of ants", "Maximum iterations"]
        self._render_parameters(self.TLabelframeACO, label_parameters)
        label_results = [ "X", "Z", "margin", "pStk", "pDIn", "CTf2s", "CTs2p", "Iteration number" ]

        self._render_results(self.TLabelframeACO, label_results)
        buttons = ["Abort", "Run"]
        actions = [self._abort, self._run_ACO]
        self._render_buttons(buttons, actions)


    def _abort(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to abort the process?"):
            os._exit(0)

    def _run_HC(self):
        if self.optimizer.is_connected is False:
            SUPPAI_support.show_database_error()
            return

        param_values = self._get_params_values()
        step = param_values[0]
        epsilon = param_values[1]
        num_iterations = param_values[2]

        self.max_iterations = num_iterations
        self.TProgressbar1.stop()
        self.TProgressbar1.configure(mode="determinate", maximum=self.max_iterations, value=0)
        self.optimizer.run_hc(step, epsilon, num_iterations, observer=self)


    def _run_RR(self):
        if self.optimizer.is_connected is False:
            SUPPAI_support.show_database_error()
            return

        param_values = self._get_params_values()
        step = param_values[0]
        epsilon = param_values[1]
        num_iterations_hc = param_values[2]
        num_loops_wo_improvement = param_values[3]
        num_restarts = param_values[4]

        self.TProgressbar1.configure(mode="indeterminate")
        self.TProgressbar1.start()
        self.max_iterations = num_restarts
        self.optimizer.run_rr(step, epsilon, num_iterations_hc, num_loops_wo_improvement, num_restarts, observer=self)
        self.TProgressbar1.stop()
        self.TProgressbar1.configure(mode="determinate", value=0)


    def _run_ACO(self):
        if self.optimizer.is_connected is False:
            SUPPAI_support.show_database_error()
            return

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

        self.max_iterations = num_iterations
        self.TProgressbar1.stop()
        self.TProgressbar1.configure(mode="determinate", maximum=self.max_iterations, value=0)
        self.optimizer.run_aco(alpha, beta, rho, Q, tau_max, tau_min, num_prod_levels, num_ants, num_iterations, observer=self)


    def _get_params_values(self):
        param_values = []
        for _, entry_widget in enumerate(self.input_entries):
            value = entry_widget.get()
            if value != "":
                param_values.append(float(value))
            else:
                param_values.append(None)
        return param_values


    def update(self, msg):
        self.update_output_results(msg)


    def update_output_results(self, results_data):
        SUPPAI_support.root.update()

        for i, entry_widget in enumerate(self.output_entries):
            if i < len(results_data):
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(results_data[i]))
                print(f"[info] Updated output entry {i} with value: {results_data[i]}")
            else:
                entry_widget.delete(0, tk.END)
        if results_data and isinstance(results_data[-1], (int, float)):
            current_iteration = int(results_data[-1])
            self.update_progressbar(current_iteration)
            if current_iteration == self.max_iterations:
                messagebox.showinfo(
                    title="Success!",
                    message=f"The optimization process has completed successfully.\n\nTime elapsed: {time.time() - self.optimizer.time_start:.2f} seconds."
                )


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

    def update_progressbar(self, value):
        if self.max_iterations > 0:
            progress_value = min(value, self.max_iterations)
            self.TProgressbar1.configure(value=progress_value)
        else:
            self.TProgressbar1.configure(value=0)


def start_up():
    SUPPAI_support.main()

if __name__ == '__main__':
    SUPPAI_support.main()
