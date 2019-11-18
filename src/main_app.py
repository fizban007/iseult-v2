#! /usr/bin/env python
import time, os, sys
from custom_toolbar import myCustomToolbar
from matplotlib.figure import Figure
from movie_dialog import MovieDialog
from oengus import Oengus
from pic_sim import picSim
import tkinter as Tk
from tkinter import ttk, filedialog, messagebox
from mpl_param import Param
import numpy as np
from scalar_flds_settings import ScalarFieldsSettings
from playback_bar import playbackBar

def destroy(e):
    sys.exit()


class MainApp(Tk.Tk):
    """ We simply derive a new class of Frame as the man frame of our app"""
    def __init__(self, name,cmd_args):

        Tk.Tk.__init__(self)
        #self.update_idletasks()
        menubar = Tk.Menu(self)
        self.wm_title(name)
        self.settings_window = None
        self.measure_window = None


        self.cmd_args = cmd_args
#        if self.cmd_args.r:
#            self.iconify()
        # A variable that keeps track of the first graph with spatial x & y axes
        self.first_x = None
        self.first_y = None

        # An int that stores the current stride
        self.stride = 0

        self.IseultDir = os.path.join(os.path.dirname(__file__),'..')

        fileMenu = Tk.Menu(menubar, tearoff=False)
        #self.presetMenu = Tk.Menu(menubar, tearoff=False, postcommand=self.ViewUpdate)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        #fileMenu.add_command(label= 'Open Directory', command = self.OnOpen, accelerator='Command+o')

        fileMenu.add_command(label="Exit", underline=1,
                             command=quit, accelerator="Ctrl+Q")
        #fileMenu.add_command(label= 'Save Current State', command = self.OpenSaveDialog)
        #fileMenu.add_command(label= 'Make a Movie', command = self.OpenMovieDialog)
        #fileMenu.add_command(label= 'Reset Session', command = self.ResetSession)


        self.bind_all("<Control-q>", self.quit)
        #self.bind_all("<Command-o>", self.OnOpen)
        #self.bind_all("S", self.OpenSettings)
        self.oengus = Oengus(interactive=True, tkApp = self)
        # open a sim
        self.sim = picSim(os.curdir)
        if len(self.sim) == 0:
            self.sim.outdir = os.path.join(os.curdir, 'output')
        if len(self.sim) == 0:
            self.sim.outdir = filedialog.askdirectory(
                title = 'Choose the directory of the output files',
                initialdir = os.curdir,
                mustexist = True,
                parent = self)
            if len(self.sim) == 0:
                self.sim.outdir = os.path.join(self.sim.outdir, 'output')
        self.oengus.open_sim(self.sim)#os.path.join(os.path.dirname(__file__),'../output')))

        self.oengus.create_graphs()
        self.geometry(self.oengus.MainParamDict['WindowSize'])
        self.minsize(780, 280)

        self.toolbar = myCustomToolbar(self.oengus.canvas, self)
        self.toolbar.update()
        self.oengus.canvas._tkcanvas.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.oengus.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.oengus.canvas.mpl_connect('button_press_event', self.onclick)
        # Make the object hold the timestep info
        self.time_step = Param(1, minimum=1, maximum=1000)
        self.playbackbar = playbackBar(self.oengus, self.time_step)
        self.playbackbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=0)
        self.time_step.attach(self)
        self.time_step.set_max(len(self.sim))
        self.time_step.set(len(self.sim))

        #menubar.add_cascade(label='Preset Views', underline=0, menu = self.presetMenu)


        self.popups_dict = {}

        self.config(menu=menubar)
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.bind('<Return>', self.txt_enter)
        self.bind('<Left>', self.playbackbar.skip_left)
        self.bind('<Right>', self.playbackbar.skip_right)
        #self.bind('r', self.playbackbar.OnReload)
        self.bind('<space>', self.playbackbar.play_handler)
        self.update()
    def GetPlotParam(self, val):
        return 1
    def onclick(self, event):
        '''After being clicked, we should use the x and y of the cursor to
        determine what subplot was clicked'''

        # Since the location of the cursor is returned in pixels and gs0 is
        # given as a relative value, we must first convert the value into a
        # relative x and y
        if not event.inaxes:
            pass
        if event.button == 1:
            pass
        else:
            fig_size = self.oengus.figure.get_size_inches()*self.oengus.figure.dpi # Fig size in px

            x_loc = event.x/fig_size[0] # The relative x position of the mouse in the figure
            y_loc = event.y/fig_size[1] # The relative y position of the mouse in the figure

            sub_plots = self.oengus.gs0.get_grid_positions(self.oengus.figure)
            row_array = np.sort(np.append(sub_plots[0], sub_plots[1]))
            col_array = np.sort(np.append(sub_plots[2], sub_plots[3]))
            i = int((len(row_array)-row_array.searchsorted(y_loc))/2)
            j = int(col_array.searchsorted(x_loc)//2)
            if f'{i,j}' in self.popups_dict:
                if self.popups_dict[f'{i,j}'] is not None:
                    self.popups_dict[f'{i,j}'].destroy()
            if self.oengus.SubPlotList[i][j].chart_type == 'ScalarFlds':
                self.popups_dict[f'{i,j}'] = ScalarFieldsSettings(self,(i,j))


    def txt_enter(self, e):
        self.playbackbar.text_callback()
    def set_knob(self, value):
        self.oengus.draw_output(value-1)
        self.oengus.canvas.get_tk_widget().update_idletasks()

def runMe(cmd_args):
    app = MainApp('Iseult', cmd_args)
    app.mainloop()
