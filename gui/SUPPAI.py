#! /usr/bin/env python3
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_location = os.path.dirname(__file__)

import SUPPAI_support

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: SUPPAI_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "-family {Segoe UI Variable} -size 10 -weight bold")
    if sys.platform == "win32":
       style.theme_use('winnative')    
    _style_code_ran = 1

class MainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("800x600+254+56")
        top.minsize(800, 600)
        top.maxsize(1351, 738)
        top.resizable(1,  1)
        top.title("SUPPAI")

        self.top = top

        self.menubar = tk.Menu(top
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,bg=_bgcolor, fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.sub_menu = tk.Menu(self.menubar, activebackground='#d9d9d9'
                ,activeforeground='black'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='File'
                ,menu=self.sub_menu, )
        self.sub_menu.add_command(accelerator='CTRL+O', compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Connect to database...')
        self.sub_menu.add_command(accelerator='CTRL+Q', compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Quit')
        self.sub_menu1 = tk.Menu(self.menubar, activebackground='#d9d9d9'
                ,activeforeground='black'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Heuristics'
                ,menu=self.sub_menu1, )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Hill Climbing'
                ,state="active", )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Random Restart'
                ,state="disabled", )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Ant Colony'
                ,state="disabled", )
        self.sub_menu12 = tk.Menu(self.menubar, activebackground='#d9d9d9'
                ,activeforeground='black'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Help'
                ,menu=self.sub_menu12, )
        self.sub_menu12.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='Licence')
        self.sub_menu12.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold", label='About')

        _style_code()
        self.TProgressbar1 = ttk.Progressbar(self.top)
        self.TProgressbar1.place(relx=0.025, rely=0.867, relwidth=0.95
                , relheight=0.0, height=19)
        self.TProgressbar1.configure(length="760")

        self.TLabelframeHC = ttk.Labelframe(self.top)
        self.TLabelframeHC.place(relx=0.025, rely=0.017, relheight=0.827
                , relwidth=0.953)
        self.TLabelframeHC.configure(relief='')
        self.TLabelframeHC.configure(text='''Hill Climbing''')

        self.TLabelframeOutput = ttk.Labelframe(self.TLabelframeHC)
        self.TLabelframeOutput.place(relx=0.512, rely=0.081, relheight=0.861
                , relwidth=0.459, bordermode='ignore')
        self.TLabelframeOutput.configure(relief='')
        self.TLabelframeOutput.configure(text='''Results''')

        self.TEntry1_3_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_3_1.place(relx=0.486, rely=0.344, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_3_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_3_1.configure(cursor="xterm")

        self.TEntry1_4_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_4_1.place(relx=0.486, rely=0.438, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_4_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_4_1.configure(cursor="xterm")

        self.TEntry1_7_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_7_1.place(relx=0.486, rely=0.712, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_7_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_7_1.configure(cursor="xterm")

        self.TEntry1_5_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_5_1.place(relx=0.486, rely=0.529, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_5_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_5_1.configure(cursor="xterm")

        self.TEntry1_6_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_6_1.place(relx=0.486, rely=0.621, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_6_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_6_1.configure(cursor="xterm")

        self.TLabel1_7_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_7_1.place(relx=0.029, rely=0.712, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_7_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_7_1.configure(relief="flat")
        self.TLabel1_7_1.configure(anchor='e')
        self.TLabel1_7_1.configure(text='''Tlabel''')
        self.TLabel1_7_1.configure(compound='left')

        self.TLabel1_6_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_6_1.place(relx=0.029, rely=0.621, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_6_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_6_1.configure(relief="flat")
        self.TLabel1_6_1.configure(anchor='e')
        self.TLabel1_6_1.configure(text='''Tlabel''')
        self.TLabel1_6_1.configure(compound='left')

        self.TLabel1_5_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_5_1.place(relx=0.029, rely=0.529, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_5_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_5_1.configure(relief="flat")
        self.TLabel1_5_1.configure(anchor='e')
        self.TLabel1_5_1.configure(text='''Tlabel''')
        self.TLabel1_5_1.configure(compound='left')

        self.TLabel1_4_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_4_1.place(relx=0.029, rely=0.438, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_4_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_4_1.configure(relief="flat")
        self.TLabel1_4_1.configure(anchor='e')
        self.TLabel1_4_1.configure(text='''Tlabel''')
        self.TLabel1_4_1.configure(compound='left')

        self.TEntry1_8_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_8_1.place(relx=0.486, rely=0.806, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_8_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_8_1.configure(cursor="xterm")

        self.TLabel1_3_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_3_1.place(relx=0.029, rely=0.344, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_3_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_3_1.configure(relief="flat")
        self.TLabel1_3_1.configure(anchor='e')
        self.TLabel1_3_1.configure(text='''Tlabel''')
        self.TLabel1_3_1.configure(compound='left')

        self.TEntry1_2_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_2_1.place(relx=0.486, rely=0.253, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_2_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_2_1.configure(cursor="xterm")

        self.TEntry1_0_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_0_1.place(relx=0.486, rely=0.068, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_0_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_0_1.configure(cursor="xterm")

        self.TEntry1_1_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_1_1.place(relx=0.486, rely=0.162, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TEntry1_1_1.configure(cursor="xterm")

        self.TLabel1_1_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_1_1.place(relx=0.029, rely=0.162, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_1_1.configure(relief="flat")
        self.TLabel1_1_1.configure(anchor='e')
        self.TLabel1_1_1.configure(text='''Tlabel''')
        self.TLabel1_1_1.configure(compound='left')

        self.TLabel1_2_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_2_1.place(relx=0.029, rely=0.253, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_2_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_2_1.configure(relief="flat")
        self.TLabel1_2_1.configure(anchor='e')
        self.TLabel1_2_1.configure(text='''Tlabel''')
        self.TLabel1_2_1.configure(compound='left')

        self.TLabel1_8_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_8_1.place(relx=0.029, rely=0.806, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_8_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_8_1.configure(relief="flat")
        self.TLabel1_8_1.configure(anchor='e')
        self.TLabel1_8_1.configure(text='''Tlabel''')
        self.TLabel1_8_1.configure(compound='left')

        self.TEntry1_9_1 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry1_9_1.place(relx=0.486, rely=0.897, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_9_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_9_1.configure(cursor="xterm")

        self.TLabel1_9_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_9_1.place(relx=0.029, rely=0.897, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_9_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_9_1.configure(relief="flat")
        self.TLabel1_9_1.configure(anchor='e')
        self.TLabel1_9_1.configure(text='''Tlabel''')
        self.TLabel1_9_1.configure(compound='left')

        self.TLabel1_0_1 = ttk.Label(self.TLabelframeOutput)
        self.TLabel1_0_1.place(relx=0.029, rely=0.068, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_0_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_0_1.configure(relief="flat")
        self.TLabel1_0_1.configure(anchor='e')
        self.TLabel1_0_1.configure(text='''Tlabel''')
        self.TLabel1_0_1.configure(compound='left')

        self.TLabelframeInput = ttk.Labelframe(self.TLabelframeHC)
        self.TLabelframeInput.place(relx=0.026, rely=0.081, relheight=0.861
                , relwidth=0.459, bordermode='ignore')
        self.TLabelframeInput.configure(relief='')
        self.TLabelframeInput.configure(text='''Parameters''')

        self.TEntry1_3_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_3_1_1.place(relx=0.486, rely=0.344, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_3_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_3_1_1.configure(cursor="xterm")

        self.TEntry1_4_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_4_1_1.place(relx=0.486, rely=0.438, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_4_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_4_1_1.configure(cursor="xterm")

        self.TEntry1_7_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_7_1_1.place(relx=0.486, rely=0.712, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_7_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_7_1_1.configure(cursor="xterm")

        self.TEntry1_5_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_5_1_1.place(relx=0.486, rely=0.529, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_5_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_5_1_1.configure(cursor="xterm")

        self.TEntry1_6_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_6_1_1.place(relx=0.486, rely=0.621, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_6_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_6_1_1.configure(cursor="xterm")

        self.TLabel1_7_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_7_1_1.place(relx=0.029, rely=0.712, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_7_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_7_1_1.configure(relief="flat")
        self.TLabel1_7_1_1.configure(anchor='e')
        self.TLabel1_7_1_1.configure(text='''Tlabel''')
        self.TLabel1_7_1_1.configure(compound='left')

        self.TLabel1_6_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_6_1_1.place(relx=0.029, rely=0.621, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_6_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_6_1_1.configure(relief="flat")
        self.TLabel1_6_1_1.configure(anchor='e')
        self.TLabel1_6_1_1.configure(text='''Tlabel''')
        self.TLabel1_6_1_1.configure(compound='left')

        self.TLabel1_5_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_5_1_1.place(relx=0.029, rely=0.529, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_5_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_5_1_1.configure(relief="flat")
        self.TLabel1_5_1_1.configure(anchor='e')
        self.TLabel1_5_1_1.configure(text='''Tlabel''')
        self.TLabel1_5_1_1.configure(compound='left')

        self.TLabel1_4_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_4_1_1.place(relx=0.029, rely=0.438, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_4_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_4_1_1.configure(relief="flat")
        self.TLabel1_4_1_1.configure(anchor='e')
        self.TLabel1_4_1_1.configure(text='''Tlabel''')
        self.TLabel1_4_1_1.configure(compound='left')

        self.TEntry1_8_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_8_1_1.place(relx=0.486, rely=0.806, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_8_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_8_1_1.configure(cursor="xterm")

        self.TLabel1_3_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_3_1_1.place(relx=0.029, rely=0.344, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_3_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_3_1_1.configure(relief="flat")
        self.TLabel1_3_1_1.configure(anchor='e')
        self.TLabel1_3_1_1.configure(text='''Tlabel''')
        self.TLabel1_3_1_1.configure(compound='left')

        self.TEntry1_2_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_2_1_1.place(relx=0.486, rely=0.253, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_2_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_2_1_1.configure(cursor="xterm")

        self.TEntry1_0_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_0_1_1.place(relx=0.486, rely=0.068, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_0_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_0_1_1.configure(cursor="xterm")

        self.TEntry1_1_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_1_1_1.place(relx=0.486, rely=0.162, relheight=0.052
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_1_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_1_1_1.configure(cursor="xterm")

        self.TLabel1_2_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_2_1_1.place(relx=0.029, rely=0.253, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_2_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_2_1_1.configure(relief="flat")
        self.TLabel1_2_1_1.configure(anchor='e')
        self.TLabel1_2_1_1.configure(text='''Tlabel''')
        self.TLabel1_2_1_1.configure(compound='left')

        self.TLabel1_8_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_8_1_1.place(relx=0.029, rely=0.806, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_8_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_8_1_1.configure(relief="flat")
        self.TLabel1_8_1_1.configure(anchor='e')
        self.TLabel1_8_1_1.configure(text='''Tlabel''')
        self.TLabel1_8_1_1.configure(compound='left')

        self.TEntry1_9_1_1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1_9_1_1.place(relx=0.486, rely=0.897, relheight=0.054
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1_9_1_1.configure(font="-family {Noto Sans} -size 10")
        self.TEntry1_9_1_1.configure(cursor="xterm")

        self.TLabel1_9_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_9_1_1.place(relx=0.029, rely=0.897, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_9_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_9_1_1.configure(relief="flat")
        self.TLabel1_9_1_1.configure(anchor='e')
        self.TLabel1_9_1_1.configure(text='''Tlabel''')
        self.TLabel1_9_1_1.configure(compound='left')

        self.TLabel1_1_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_1_1_1.place(relx=0.029, rely=0.162, height=20, width=150
                , bordermode='ignore')
        self.TLabel1_1_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_1_1_1.configure(relief="flat")
        self.TLabel1_1_1_1.configure(anchor='e')
        self.TLabel1_1_1_1.configure(text='''Tlabel''')
        self.TLabel1_1_1_1.configure(compound='left')

        self.TLabel1_0_1_1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1_0_1_1.place(relx=0.029, rely=0.068, height=21, width=150
                , bordermode='ignore')
        self.TLabel1_0_1_1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1_0_1_1.configure(relief="flat")
        self.TLabel1_0_1_1.configure(anchor='e')
        self.TLabel1_0_1_1.configure(text='''Tlabel''')
        self.TLabel1_0_1_1.configure(compound='left')

        self.TButtonRun = ttk.Button(self.top)
        self.TButtonRun.place(relx=0.875, rely=0.917, height=30, width=83)
        self.TButtonRun.configure(takefocus="")
        self.TButtonRun.configure(text='''Run''')
        self.TButtonRun.configure(compound='left')

        self.TButtonAbort = ttk.Button(self.top)
        self.TButtonAbort.place(relx=0.75, rely=0.917, height=30, width=83)
        self.TButtonAbort.configure(takefocus="")
        self.TButtonAbort.configure(text='''Abort''')
        self.TButtonAbort.configure(compound='left')

def start_up():
    SUPPAI_support.main()

if __name__ == '__main__':
    SUPPAI_support.main()




