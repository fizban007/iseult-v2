class ScalarFieldsSettings(Tk.Toplevel):
    def __init__(self, parent):
        self.parent = parent
        Tk.Toplevel.__init__(self)

        self.wm_title('Dens Plot (%d,%d) Settings' % self.parent.FigWrap.pos)
        self.parent = parent
        frm = ttk.Frame(self)
        frm.pack(fill=Tk.BOTH, expand=True)
        self.protocol('WM_DELETE_WINDOW', self.OnClosing)
        self.bind('<Return>', self.TxtEnter)


        # Create the OptionMenu to chooses the Chart Type:
        self.InterpolVar = Tk.StringVar(self)
        self.InterpolVar.set(self.parent.GetPlotParam('interpolation')) # default value
        self.InterpolVar.trace('w', self.InterpolChanged)

        ttk.Label(frm, text="Interpolation Method:").grid(row=0, column = 2)
        InterplChooser = ttk.OptionMenu(frm, self.InterpolVar, self.parent.GetPlotParam('interpolation'), *tuple(self.parent.InterpolationMethods))
        InterplChooser.grid(row =0, column = 3, sticky = Tk.W + Tk.E)

        # Create the OptionMenu to chooses the Chart Type:
        self.ctypevar = Tk.StringVar(self)
        self.ctypevar.set(self.parent.chartType) # default value
        self.ctypevar.trace('w', self.ctypeChanged)

        ttk.Label(frm, text="Choose Chart Type:").grid(row=0, column = 0)
        ctypeChooser = ttk.OptionMenu(frm, self.ctypevar, self.parent.chartType, *tuple(self.parent.ChartTypes))
        ctypeChooser.grid(row =0, column = 1, sticky = Tk.W + Tk.E)


        self.TwoDVar = Tk.IntVar(self) # Create a var to track whether or not to plot in 2-D
        self.TwoDVar.set(self.parent.GetPlotParam('twoD'))
        cb = ttk.Checkbutton(frm, text = "Show in 2-D",
                variable = self.TwoDVar,
                command = self.Change2d)
        cb.grid(row = 1, sticky = Tk.W)

        # the Radiobox Control to choose the Field Type
        self.DensList = ['dens', 'dens_i', 'dens_e', 'rho']
        self.DensTypeVar  = Tk.IntVar()
        self.DensTypeVar.set(self.parent.GetPlotParam('dens_type'))

        ttk.Label(frm, text='Choose Density:').grid(row = 2, sticky = Tk.W)

        for i in range(len(self.DensList)):
            ttk.Radiobutton(frm,
                text=self.DensList[i],
                variable=self.DensTypeVar,
                command = self.RadioField,
                value=i).grid(row = 3+i//2, column = i-2*(i//2), sticky =Tk.W)


        # Control whether or not Cbar is shown
        self.CbarVar = Tk.IntVar()
        self.CbarVar.set(self.parent.GetPlotParam('show_cbar'))
        cb = ttk.Checkbutton(frm, text = "Show Color bar",
                        variable = self.CbarVar,
                        command = self.CbarHandler)
        cb.grid(row = 6, sticky = Tk.W)

        # show shock
        self.ShockVar = Tk.IntVar()
        self.ShockVar.set(self.parent.GetPlotParam('show_shock'))
        cb = ttk.Checkbutton(frm, text = "Show Shock",
                        variable = self.ShockVar,
                        command = self.ShockVarHandler)
        cb.grid(row = 6, column = 1, sticky = Tk.W)

        # Normalize Density Var
        self.NormDVar = Tk.IntVar()
        self.NormDVar.set(self.parent.GetPlotParam('normalize_density'))
        cb = ttk.Checkbutton(frm, text = "Normalize to ppc0",
                        variable = self.NormDVar,
                        command = self.NormPPCHandler)
        cb.grid(row = 7, sticky = Tk.W)

        # show labels
        self.ShowLabels = Tk.IntVar()
        self.ShowLabels.set(self.parent.GetPlotParam('show_labels'))
        cb = ttk.Checkbutton(frm, text = "Show Labels 2D",
                        variable = self.ShowLabels,
                        command = self.LabelHandler)
        cb.grid(row = 7, column = 1, sticky = Tk.W)
        # Control whether or not diverging cmap is used
        self.DivVar = Tk.IntVar()
        self.DivVar.set(self.parent.GetPlotParam('UseDivCmap'))
        cb = ttk.Checkbutton(frm, text = "Use Diverging Cmap",
                        variable = self.DivVar,
                        command = self.DivHandler)
        cb.grid(row = 8, sticky = Tk.W)

        # Use full div cmap
        self.StretchVar = Tk.IntVar()
        self.StretchVar.set(self.parent.GetPlotParam('stretch_colors'))
        cb = ttk.Checkbutton(frm, text = "Asymmetric Color Space",
                        variable = self.StretchVar,
                        command = self.StretchHandler)
        cb.grid(row = 9, column = 0, columnspan =2, sticky = Tk.W)

        self.CPUVar = Tk.IntVar()
        self.CPUVar.set(self.parent.GetPlotParam('show_cpu_domains'))
        cb = ttk.Checkbutton(frm, text = "Show CPU domains",
                        variable = self.CPUVar,
                        command = self.CPUVarHandler)
        cb.grid(row = 10, column = 0, sticky = Tk.W)

        # Create the OptionMenu to chooses the cnorm_type:
        self.cnormvar = Tk.StringVar(self)
        self.cnormvar.set(self.parent.chartType) # default value
        self.cnormvar.trace('w', self.cnormChanged)

        ttk.Label(frm, text="Choose Color Norm:").grid(row=6, column = 2)
        cnormChooser = ttk.OptionMenu(frm, self.cnormvar, self.parent.GetPlotParam('cnorm_type'), *tuple(['Pow', 'Linear']))
        cnormChooser.grid(row =6, column = 3, sticky = Tk.W + Tk.E)

        # Now the gamma of the pow norm
        self.powGamma = Tk.StringVar()
        self.powGamma.set(str(self.parent.GetPlotParam('cpow_num')))
        ttk.Label(frm, text ='gamma =').grid(row = 7, column = 2, sticky =Tk.E)
        ttk.Label(frm, text ='If cnorm is Pow =>').grid(row = 8, column = 2,columnspan = 2, sticky =Tk.W)
        ttk.Label(frm, text ='sign(data)*|data|**gamma').grid(row = 9, column = 2,columnspan = 2, sticky =Tk.E)

        self.GammaEnter = ttk.Entry(frm, textvariable=self.powGamma, width=7)
        self.GammaEnter.grid(row = 7, column = 3)


        # Now the field lim
        self.setZminVar = Tk.IntVar()
        self.setZminVar.set(self.parent.GetPlotParam('set_v_min'))
        self.setZminVar.trace('w', self.setZminChanged)

        self.setZmaxVar = Tk.IntVar()
        self.setZmaxVar.set(self.parent.GetPlotParam('set_v_max'))
        self.setZmaxVar.trace('w', self.setZmaxChanged)



        self.Zmin = Tk.StringVar()
        self.Zmin.set(str(self.parent.GetPlotParam('v_min')))

        self.Zmax = Tk.StringVar()
        self.Zmax.set(str(self.parent.GetPlotParam('v_max')))


        cb = ttk.Checkbutton(frm, text ='Set dens min',
                        variable = self.setZminVar)
        cb.grid(row = 3, column = 2, sticky = Tk.W)
        self.ZminEnter = ttk.Entry(frm, textvariable=self.Zmin, width=7)
        self.ZminEnter.grid(row = 3, column = 3)

        cb = ttk.Checkbutton(frm, text ='Set dens max',
                        variable = self.setZmaxVar)
        cb.grid(row = 4, column = 2, sticky = Tk.W)

        self.ZmaxEnter = ttk.Entry(frm, textvariable=self.Zmax, width=7)
        self.ZmaxEnter.grid(row = 4, column = 3)

    def ShockVarHandler(self, *args):
        if self.parent.GetPlotParam('show_shock')== self.ShockVar.get():
            pass
        else:
            if self.parent.GetPlotParam('twoD'):
                self.parent.shockline_2d.set_visible(self.ShockVar.get())
            else:
                self.parent.shock_line.set_visible(self.ShockVar.get())

            self.parent.SetPlotParam('show_shock', self.ShockVar.get())

    def CbarHandler(self, *args):
        if self.parent.GetPlotParam('show_cbar')== self.CbarVar.get():
            pass
        else:
            if self.parent.GetPlotParam('twoD'):
                self.parent.axC.set_visible(self.CbarVar.get())

            self.parent.SetPlotParam('show_cbar', self.CbarVar.get(), update_plot =self.parent.GetPlotParam('twoD'))

    def DivHandler(self, *args):
        if self.parent.GetPlotParam('UseDivCmap')== self.DivVar.get():
            pass
        elif self.parent.GetPlotParam('twoD'):
            self.parent.SetPlotParam('UseDivCmap', self.DivVar.get(),  NeedsRedraw = True)
        else:
            self.parent.SetPlotParam('UseDivCmap', self.DivVar.get(),  update_plot = False)


    def StretchHandler(self, *args):
        if self.parent.GetPlotParam('stretch_colors')== self.StretchVar.get():
            pass
        elif self.parent.GetPlotParam('twoD'):
            self.parent.SetPlotParam('stretch_colors', self.StretchVar.get(), NeedsRedraw = True)
        else:
            self.parent.SetPlotParam('stretch_colors', self.StretchVar.get(), update_plot = False)

    def cnormChanged(self, *args):
        if self.parent.GetPlotParam('cnorm_type')== self.cnormvar.get():
            pass
        elif self.parent.GetPlotParam('twoD'):
            self.parent.SetPlotParam('cnorm_type', self.cnormvar.get(), NeedsRedraw = True)
        else:
            self.parent.SetPlotParam('cnorm_type', self.cnormvar.get(), update_plot = False)


    def NormPPCHandler(self, *args):
        if self.parent.GetPlotParam('normalize_density')== self.NormDVar.get():
            pass
        elif np.isnan(self.parent.ppc0):
            self.NormDVar.set(self.parent.GetPlotParam('normalize_density'))
        else:
            # First see if the plot is 2d and change the labels if necessary
            if self.parent.GetPlotParam('twoD')==1:
                tmp_str = ''
                if self.parent.GetPlotParam('dens_type') == 0:
                    tmp_str += r'$n$'
                if self.parent.GetPlotParam('dens_type') == 1:
                    tmp_str += r'$n_i$'
                if self.parent.GetPlotParam('dens_type') == 2:
                    tmp_str += r'$n_e$'
                if self.parent.GetPlotParam('dens_type') == 3:
                    tmp_str += r'$\rho$'
                if self.NormDVar.get():
                    tmp_str += r'$\ [n_0]$'
                self.parent.an_2d.set_text(tmp_str)
            # Now for the 1d label
            else:
                if self.parent.GetPlotParam('dens_type') == 0:
                    if self.NormDVar.get():
                        self.parent.axes.set_ylabel(r'${\rm density}\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel('density', size = self.parent.parent.MainParamDict['AxLabelSize'])
                if self.parent.GetPlotParam('dens_type') == 1:
                    if self.NormDVar.get():
                        self.parent.axes.set_ylabel(r'$n_i\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$n_i$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                if self.parent.GetPlotParam('dens_type') == 2:
                    if self.NormDVar.get():
                        self.parent.axes.set_ylabel(r'$n_e\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$n_e$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                if self.parent.GetPlotParam('dens_type') == 3:
                    if self.NormDVar.get():
                        self.parent.axes.set_ylabel(r'$\rho\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$\rho$', size = self.parent.parent.MainParamDict['AxLabelSize'])

            self.parent.SetPlotParam('normalize_density', self.NormDVar.get())#, update_plot = self.parent.GetPlotParam('dens_type')==0)

    def LabelHandler(self, *args):
        if self.parent.GetPlotParam('show_labels')== self.ShowLabels.get():
            pass
        else:
            if self.parent.GetPlotParam('twoD'):
                self.parent.an_2d.set_visible(self.ShowLabels.get())

            self.parent.SetPlotParam('show_labels', self.ShowLabels.get(), update_plot =self.parent.GetPlotParam('twoD'))

    def CPUVarHandler(self, *args):
        if self.parent.GetPlotParam('show_cpu_domains')== self.CPUVar.get():
            pass
        else:
            self.parent.SetPlotParam('show_cpu_domains', self.CPUVar.get(), update_plot = False)
            if self.parent.GetPlotParam('show_cpu_domains'):
                self.parent.FigWrap.SetCpuDomainLines()
            else: # We need to get remove of the cpu lines. Pop them out of the array and remove them from the list.
                self.parent.FigWrap.RemoveCpuDomainLines()
            self.parent.parent.canvas.draw()
            self.parent.parent.canvas.get_tk_widget().update_idletasks()

    def Change2d(self):
        if self.TwoDVar.get() == self.parent.GetPlotParam('twoD'):
            pass
        else:
            self.parent.SetPlotParam('spatial_y', self.TwoDVar.get(), update_plot = False)
            self.parent.SetPlotParam('twoD', self.TwoDVar.get())


    def ctypeChanged(self, *args):
        if self.ctypevar.get() == self.parent.chartType:
            pass
        else:
            self.parent.ChangePlotType(self.ctypevar.get())
            self.destroy()

    def InterpolChanged(self, *args):
        if self.InterpolVar.get() == self.parent.GetPlotParam('interpolation'):
            pass
        else:
            if self.parent.GetPlotParam('twoD'):
                self.parent.cax.set_interpolation(self.InterpolVar.get())
            self.parent.SetPlotParam('interpolation', self.InterpolVar.get())

    def setZminChanged(self, *args):
        if self.setZminVar.get() == self.parent.GetPlotParam('set_v_min'):
            pass
        else:
            self.parent.SetPlotParam('set_v_min', self.setZminVar.get())

    def setZmaxChanged(self, *args):
        if self.setZmaxVar.get() == self.parent.GetPlotParam('set_v_max'):
            pass
        else:
            self.parent.SetPlotParam('set_v_max', self.setZmaxVar.get())

    def TxtEnter(self, e):
        self.FieldsCallback()
        self.GammaCallback()

    def GammaCallback(self):
        try:
        #make sure the user types in a float
            if np.abs(float(self.powGamma.get()) - self.parent.GetPlotParam('cpow_num')) > 1E-4:
                if self.parent.GetPlotParam('twoD') and self.parent.GetPlotParam('cnorm_type')=='Pow':
                    self.parent.SetPlotParam('cpow_num', float(self.powGamma.get()), NeedsRedraw = True)

                else:
                    self.parent.SetPlotParam('cpow_num', float(self.powGamma.get()), update_plot = False)

        except ValueError:
            #if they type in random stuff, just set it ot the param value
            self.powGamma.set(str(self.parent.GetPlotParam('cpow_num')))


    def FieldsCallback(self):
        tkvarLimList = [self.Zmin, self.Zmax]
        plot_param_List = ['v_min', 'v_max']
        tkvarSetList = [self.setZminVar, self.setZmaxVar]
        to_reload = False
        for j in range(len(tkvarLimList)):
            try:
            #make sure the user types in a int
                if np.abs(float(tkvarLimList[j].get()) - self.parent.GetPlotParam(plot_param_List[j])) > 1E-4:
                    self.parent.SetPlotParam(plot_param_List[j], float(tkvarLimList[j].get()), update_plot = False)
                    to_reload += True*tkvarSetList[j].get()

            except ValueError:
                #if they type in random stuff, just set it ot the param value
                tkvarLimList[j].set(str(self.parent.GetPlotParam(plot_param_List[j])))
        if to_reload:
            self.parent.SetPlotParam('v_min', self.parent.GetPlotParam('v_min'))


    def RadioField(self):
        if self.DensTypeVar.get() == self.parent.GetPlotParam('dens_type'):
            pass
        else:
            if self.parent.GetPlotParam('twoD'):
                if self.DensTypeVar.get() == 0:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.an_2d.set_text(r'$n/n_0$')
                    else:
                        self.parent.an_2d.set_text(r'$n$')

                elif self.DensTypeVar.get() == 1:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.an_2d.set_text(r'$n_i/n_0$')
                    else:
                        self.parent.an_2d.set_text(r'$n_i$')

                elif self.DensTypeVar.get() == 2:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.an_2d.set_text(r'$n_e/n_0$')
                    else:
                        self.parent.an_2d.set_text(r'$n_e$')
                elif self.DensTypeVar.get() == 3:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.an_2d.set_text(r'$\rho/n_0$')
                    else:
                        self.parent.an_2d.set_text(r'$\rho$')

            else:
                if self.DensTypeVar.get() == 0:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.axes.set_ylabel(r'${\rm density}\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$\rm density$', size = self.parent.parent.MainParamDict['AxLabelSize'])


                elif self.DensTypeVar.get() ==1:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.axes.set_ylabel(r'$n_i\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$n_i$', size = self.parent.parent.MainParamDict['AxLabelSize'])

                elif self.DensTypeVar.get() ==2:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.axes.set_ylabel(r'$n_e\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$n_e$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                elif self.DensTypeVar.get() ==3:
                    if self.parent.GetPlotParam('normalize_density'):
                        self.parent.axes.set_ylabel(r'$\rho\ [n_0]$', size = self.parent.parent.MainParamDict['AxLabelSize'])
                    else:
                        self.parent.axes.set_ylabel(r'$\rho$', size = self.parent.parent.MainParamDict['AxLabelSize'])


            self.parent.SetPlotParam('dens_type', self.DensTypeVar.get())


    def OnClosing(self):
        self.parent.settings_window = None
        self.destroy()