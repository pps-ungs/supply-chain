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

        top.geometry("800x600+493+76")
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
                ,activeforeground='black', tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='File', menu=self.sub_menu, )
        self.sub_menu.add_command(accelerator='CTRL+O', compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Connect to database...')
        self.sub_menu.add_command(accelerator='CTRL+Q', compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Quit')
        self.sub_menu1 = tk.Menu(self.menubar, activebackground='#d9d9d9'
                ,activeforeground='black', tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Heuristics', menu=self.sub_menu1, )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Hill Climbing', state="active", )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Random Restart', state="disabled", )
        self.sub_menu1.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Ant Colony', state="disabled", )
        self.sub_menu12 = tk.Menu(self.menubar, activebackground='#d9d9d9'
                ,activeforeground='black', tearoff=0)
        self.menubar.add_cascade(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Help', menu=self.sub_menu12, )
        self.sub_menu12.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='Licence')
        self.sub_menu12.add_command(compound='left'
                ,font="-family {Segoe UI Variable} -size 10 -weight bold"
                ,label='About')

        _style_code()
        self.TLabelframeHC = ttk.Labelframe(self.top)
        self.TLabelframeHC.place(relx=0.025, rely=0.017, relheight=0.958
                , relwidth=0.953)
        self.TLabelframeHC.configure(relief='')
        self.TLabelframeHC.configure(text='''Hill Climbing''')

        self.TProgressbar1 = ttk.Progressbar(self.TLabelframeHC)
        self.TProgressbar1.place(relx=0.026, rely=0.87, relwidth=0.945
                , relheight=0.0, height=19, bordermode='ignore')
        self.TProgressbar1.configure(length="720")

        self.TLabelframeInput = ttk.Labelframe(self.TLabelframeHC)
        self.TLabelframeInput.place(relx=0.026, rely=0.052, relheight=0.791
                , relwidth=0.459, bordermode='ignore')
        self.TLabelframeInput.configure(relief='')
        self.TLabelframeInput.configure(text='''Parameters''')

        self.TEntry1 = ttk.Entry(self.TLabelframeInput)
        self.TEntry1.place(relx=0.486, rely=0.066, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="xterm")

        self.TEntry13 = ttk.Entry(self.TLabelframeInput)
        self.TEntry13.place(relx=0.486, rely=0.242, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry13.configure(takefocus="")
        self.TEntry13.configure(cursor="xterm")

        self.TEntry2 = ttk.Entry(self.TLabelframeInput)
        self.TEntry2.place(relx=0.486, rely=0.154, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="xterm")

        self.TEntry14 = ttk.Entry(self.TLabelframeInput)
        self.TEntry14.place(relx=0.486, rely=0.33, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry14.configure(takefocus="")
        self.TEntry14.configure(cursor="xterm")

        self.TEntry15 = ttk.Entry(self.TLabelframeInput)
        self.TEntry15.place(relx=0.486, rely=0.418, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry15.configure(takefocus="")
        self.TEntry15.configure(cursor="xterm")

        self.TEntry16 = ttk.Entry(self.TLabelframeInput)
        self.TEntry16.place(relx=0.486, rely=0.505, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry16.configure(takefocus="")
        self.TEntry16.configure(cursor="xterm")

        self.TEntry17 = ttk.Entry(self.TLabelframeInput)
        self.TEntry17.place(relx=0.486, rely=0.593, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry17.configure(takefocus="")
        self.TEntry17.configure(cursor="xterm")

        self.TEntry18 = ttk.Entry(self.TLabelframeInput)
        self.TEntry18.place(relx=0.486, rely=0.681, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry18.configure(takefocus="")
        self.TEntry18.configure(cursor="xterm")

        self.TEntry19 = ttk.Entry(self.TLabelframeInput)
        self.TEntry19.place(relx=0.486, rely=0.769, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry19.configure(takefocus="")
        self.TEntry19.configure(cursor="xterm")

        self.TEntry20 = ttk.Entry(self.TLabelframeInput)
        self.TEntry20.place(relx=0.486, rely=0.857, relheight=0.051
                , relwidth=0.469, bordermode='ignore')
        self.TEntry20.configure(takefocus="")
        self.TEntry20.configure(cursor="xterm")

        self.TLabelStep = ttk.Label(self.TLabelframeInput)
        self.TLabelStep.place(relx=0.029, rely=0.066, height=21, width=146
                , bordermode='ignore')
        self.TLabelStep.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelStep.configure(relief="flat")
        self.TLabelStep.configure(anchor='e')
        self.TLabelStep.configure(text='''Step''')
        self.TLabelStep.configure(compound='left')

        self.TLabelMaxIter = ttk.Label(self.TLabelframeInput)
        self.TLabelMaxIter.place(relx=0.029, rely=0.154, height=21, width=146
                , bordermode='ignore')
        self.TLabelMaxIter.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelMaxIter.configure(relief="flat")
        self.TLabelMaxIter.configure(anchor='e')
        self.TLabelMaxIter.configure(text='''Maximum iterations''')
        self.TLabelMaxIter.configure(compound='left')

        self.TLabel1 = ttk.Label(self.TLabelframeInput)
        self.TLabel1.place(relx=0.029, rely=0.242, height=21, width=150
                , bordermode='ignore')
        self.TLabel1.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(anchor='e')
        self.TLabel1.configure(text='''Tlabel''')
        self.TLabel1.configure(compound='left')

        self.TLabel2 = ttk.Label(self.TLabelframeInput)
        self.TLabel2.place(relx=0.029, rely=0.33, height=21, width=150
                , bordermode='ignore')
        self.TLabel2.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel2.configure(relief="flat")
        self.TLabel2.configure(anchor='e')
        self.TLabel2.configure(text='''Tlabel''')
        self.TLabel2.configure(compound='left')

        self.TLabel3 = ttk.Label(self.TLabelframeInput)
        self.TLabel3.place(relx=0.029, rely=0.418, height=21, width=150
                , bordermode='ignore')
        self.TLabel3.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel3.configure(relief="flat")
        self.TLabel3.configure(anchor='e')
        self.TLabel3.configure(text='''Tlabel''')
        self.TLabel3.configure(compound='left')

        self.TLabel4 = ttk.Label(self.TLabelframeInput)
        self.TLabel4.place(relx=0.029, rely=0.505, height=21, width=150
                , bordermode='ignore')
        self.TLabel4.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel4.configure(relief="flat")
        self.TLabel4.configure(anchor='e')
        self.TLabel4.configure(text='''Tlabel''')
        self.TLabel4.configure(compound='left')

        self.TLabel5 = ttk.Label(self.TLabelframeInput)
        self.TLabel5.place(relx=0.029, rely=0.593, height=21, width=150
                , bordermode='ignore')
        self.TLabel5.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel5.configure(relief="flat")
        self.TLabel5.configure(anchor='e')
        self.TLabel5.configure(text='''Tlabel''')
        self.TLabel5.configure(compound='left')

        self.TLabel6 = ttk.Label(self.TLabelframeInput)
        self.TLabel6.place(relx=0.029, rely=0.681, height=21, width=150
                , bordermode='ignore')
        self.TLabel6.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel6.configure(relief="flat")
        self.TLabel6.configure(anchor='e')
        self.TLabel6.configure(text='''Tlabel''')
        self.TLabel6.configure(compound='left')

        self.TLabel7 = ttk.Label(self.TLabelframeInput)
        self.TLabel7.place(relx=0.029, rely=0.769, height=21, width=150
                , bordermode='ignore')
        self.TLabel7.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel7.configure(relief="flat")
        self.TLabel7.configure(anchor='e')
        self.TLabel7.configure(text='''Tlabel''')
        self.TLabel7.configure(compound='left')

        self.TLabel8 = ttk.Label(self.TLabelframeInput)
        self.TLabel8.place(relx=0.029, rely=0.857, height=21, width=150
                , bordermode='ignore')
        self.TLabel8.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabel8.configure(relief="flat")
        self.TLabel8.configure(anchor='e')
        self.TLabel8.configure(text='''Tlabel''')
        self.TLabel8.configure(compound='left')

        self.TButtonRun = ttk.Button(self.TLabelframeHC)
        self.TButtonRun.place(relx=0.866, rely=0.922, height=30, width=83
                , bordermode='ignore')
        self.TButtonRun.configure(takefocus="")
        self.TButtonRun.configure(text='''Run''')
        self.TButtonRun.configure(compound='left')

        self.TButtonAbort = ttk.Button(self.TLabelframeHC)
        self.TButtonAbort.place(relx=0.735, rely=0.922, height=30, width=83
                , bordermode='ignore')
        self.TButtonAbort.configure(takefocus="")
        self.TButtonAbort.configure(text='''Abort''')
        self.TButtonAbort.configure(compound='left')

        self.TLabelframeOutput = ttk.Labelframe(self.TLabelframeHC)
        self.TLabelframeOutput.place(relx=0.512, rely=0.052, relheight=0.791
                , relwidth=0.459, bordermode='ignore')
        self.TLabelframeOutput.configure(relief='groove')
        self.TLabelframeOutput.configure(text='''Results''')
        self.TLabelframeOutput.configure(relief="groove")

        self.TEntry7 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry7.place(relx=0.471, rely=0.418, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry7.configure(takefocus="")
        self.TEntry7.configure(cursor="xterm")

        self.TEntry8 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry8.place(relx=0.471, rely=0.505, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry8.configure(takefocus="")
        self.TEntry8.configure(cursor="xterm")

        self.TEntry9 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry9.place(relx=0.471, rely=0.593, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry9.configure(takefocus="")
        self.TEntry9.configure(cursor="xterm")

        self.TEntry10 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry10.place(relx=0.471, rely=0.681, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry10.configure(takefocus="")
        self.TEntry10.configure(cursor="xterm")

        self.TEntry11 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry11.place(relx=0.471, rely=0.769, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry11.configure(takefocus="")
        self.TEntry11.configure(cursor="xterm")

        self.TEntry12 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry12.place(relx=0.471, rely=0.857, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry12.configure(takefocus="")
        self.TEntry12.configure(cursor="xterm")

        self.TLabelCTs2p = ttk.Label(self.TLabelframeOutput)
        self.TLabelCTs2p.place(relx=0.029, rely=0.593, height=21, width=144
                , bordermode='ignore')
        self.TLabelCTs2p.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelCTs2p.configure(relief="flat")
        self.TLabelCTs2p.configure(anchor='e')
        self.TLabelCTs2p.configure(text='''CTs2p''')
        self.TLabelCTs2p.configure(compound='left')

        self.TLabelTime = ttk.Label(self.TLabelframeOutput)
        self.TLabelTime.place(relx=0.029, rely=0.769, height=21, width=144
                , bordermode='ignore')
        self.TLabelTime.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelTime.configure(relief="flat")
        self.TLabelTime.configure(anchor='e')
        self.TLabelTime.configure(text='''Time''')
        self.TLabelTime.configure(compound='left')

        self.TLabelIterations = ttk.Label(self.TLabelframeOutput)
        self.TLabelIterations.place(relx=0.029, rely=0.681, height=21, width=144
                , bordermode='ignore')
        self.TLabelIterations.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelIterations.configure(relief="flat")
        self.TLabelIterations.configure(anchor='e')
        self.TLabelIterations.configure(text='''Iterations''')
        self.TLabelIterations.configure(compound='left')

        self.TLabelHalting = ttk.Label(self.TLabelframeOutput)
        self.TLabelHalting.place(relx=0.029, rely=0.857, height=21, width=144
                , bordermode='ignore')
        self.TLabelHalting.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelHalting.configure(relief="flat")
        self.TLabelHalting.configure(anchor='e')
        self.TLabelHalting.configure(text='''Halting condition''')
        self.TLabelHalting.configure(compound='left')

        self.TEntry6 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry6.place(relx=0.471, rely=0.33, relheight=0.051, relwidth=0.483
                , bordermode='ignore')
        self.TEntry6.configure(takefocus="")
        self.TEntry6.configure(cursor="xterm")

        self.TEntry5 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry5.place(relx=0.471, rely=0.242, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry5.configure(takefocus="")
        self.TEntry5.configure(cursor="xterm")

        self.TEntry3 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry3.place(relx=0.471, rely=0.066, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry3.configure(font="-family {Cascadia Code} -size 10 -weight bold")
        self.TEntry3.configure(state='readonly')
        self.TEntry3.configure(takefocus="")
        self.TEntry3.configure(cursor="xterm")

        self.TEntry4 = ttk.Entry(self.TLabelframeOutput)
        self.TEntry4.place(relx=0.471, rely=0.154, relheight=0.051
                , relwidth=0.483, bordermode='ignore')
        self.TEntry4.configure(font="-family {Cascadia Code} -size 10 -weight bold")
        self.TEntry4.configure(state='readonly')
        self.TEntry4.configure(takefocus="")
        self.TEntry4.configure(cursor="xterm")

        self.TLabelCTf2s = ttk.Label(self.TLabelframeOutput)
        self.TLabelCTf2s.place(relx=0.029, rely=0.505, height=21, width=144
                , bordermode='ignore')
        self.TLabelCTf2s.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelCTf2s.configure(relief="flat")
        self.TLabelCTf2s.configure(anchor='e')
        self.TLabelCTf2s.configure(text='''CTf2s''')
        self.TLabelCTf2s.configure(compound='left')

        self.TLabelpDIn = ttk.Label(self.TLabelframeOutput)
        self.TLabelpDIn.place(relx=0.029, rely=0.418, height=21, width=144
                , bordermode='ignore')
        self.TLabelpDIn.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelpDIn.configure(relief="flat")
        self.TLabelpDIn.configure(anchor='e')
        self.TLabelpDIn.configure(text='''pDIn''')
        self.TLabelpDIn.configure(compound='left')

        self.TLabelpStk = ttk.Label(self.TLabelframeOutput)
        self.TLabelpStk.place(relx=0.029, rely=0.33, height=21, width=144
                , bordermode='ignore')
        self.TLabelpStk.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelpStk.configure(relief="flat")
        self.TLabelpStk.configure(anchor='e')
        self.TLabelpStk.configure(text='''pStk''')
        self.TLabelpStk.configure(compound='left')

        self.TLabelMargin = ttk.Label(self.TLabelframeOutput)
        self.TLabelMargin.place(relx=0.029, rely=0.242, height=21, width=144
                , bordermode='ignore')
        self.TLabelMargin.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelMargin.configure(relief="flat")
        self.TLabelMargin.configure(anchor='e')
        self.TLabelMargin.configure(text='''Margin''')
        self.TLabelMargin.configure(compound='left')

        self.TLabelZ = ttk.Label(self.TLabelframeOutput)
        self.TLabelZ.place(relx=0.029, rely=0.154, height=21, width=144
                , bordermode='ignore')
        self.TLabelZ.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelZ.configure(relief="flat")
        self.TLabelZ.configure(anchor='e')
        self.TLabelZ.configure(text='''Z''')
        self.TLabelZ.configure(compound='left')

        self.TLabelX = ttk.Label(self.TLabelframeOutput)
        self.TLabelX.place(relx=0.029, rely=0.066, height=21, width=144
                , bordermode='ignore')
        self.TLabelX.configure(font="-family {Segoe UI Variable} -size 10 -weight bold")
        self.TLabelX.configure(relief="flat")
        self.TLabelX.configure(anchor='e')
        self.TLabelX.configure(text='''X''')
        self.TLabelX.configure(compound='left')

def start_up():
    SUPPAI_support.main()

if __name__ == '__main__':
    SUPPAI_support.main()
