# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:04:54 2015

@author: Matt Siebert
"""

import numpy as np
import sys
import pyqtgraph as pg
import datetime
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.ptime import time

class GUI_Form():
    """An instance sets up the basic gui layout for the sourcemap application."""
    
    def __init__(self, newmap):
        """Constructor creates and lays out the widgets to be used in the gui.
        The contents of many of these widgets are called upon and changed as 
        the application is running. 
        """
        
        self.newmap = newmap
        self.counter = 0
        
        #main window      
        self.win = QtGui.QWidget()
        self.win.setWindowTitle('Radio Source Sky Map: Haystack Observatory')
        self.win.setWindowIcon(QtGui.QIcon('/home/msiebert/Documents/MIT_REU/37m_GUI/Haystack_Icon.gif'))
        self.win.resize(1620,700)
        self.gridLayout = QtGui.QGridLayout(self.win)
        
        #main plot and strip charts
        self.plot = pg.PlotWidget(self.win)
        self.azstrip = pg.PlotWidget(self.win)
        self.elstrip = pg.PlotWidget(self.win)
        
        #set up the general layout
        self.gridLayout.addWidget(self.plot, 0, 1, 15, 7)
        self.gridLayout.addWidget(self.azstrip, 18, 1, 4, 2)
        self.gridLayout.addWidget(self.elstrip, 18, 3, 4, 2)
        self.gridLayout.setColumnStretch(0,0)
        self.gridLayout.setColumnMinimumWidth(0,130)
        self.gridLayout.setColumnStretch(1,1)
        self.gridLayout.setColumnMinimumWidth(1,200)
        self.gridLayout.setColumnStretch(2,1)
        self.gridLayout.setColumnMinimumWidth(2,200)
        self.gridLayout.setColumnStretch(3,1)
        self.gridLayout.setColumnMinimumWidth(3,200)
        self.gridLayout.setColumnStretch(4,1)
        self.gridLayout.setColumnMinimumWidth(4,200)
        
#        self.clickinfo = QtGui.QComboBox(self.win)
#        self.gridLayout.addWidget(self.clickinfo, 25, 0, 1, 1)
        
        self.menubut = QtGui.QPushButton('Menu')
        self.menu = QtGui.QMenu()
        self.menu.addAction('Change Source List', self.new_sourcelist)
        self.menu.addAction('Pause/Unpause', self.pause)
        self.menu.addAction('Reset Axes', self.reset_axes)
        self.menu.addAction('Toggle RA/Dec Grid', self.toggle_radecgrid)
        self.menu.addAction('Toggle Ephem', self.toggle_ephems)
        self.menu.addAction('Toggle Strip Charts', self.toggle_strips)
        self.menu.addAction('Toggle Click Track', self.toggle_track)
        self.menu.addAction('Toggle Antenna Track', self.toggle_track_ant)
        self.menu.addAction('Clear Paths', self.clear_path)
        self.menu.addAction('Enter New UT', self.set_time)
        self.menu.addAction('Add Object', self.add)
        self.menu.addAction('Remove Objects', self.remove)
        self.menubut.setMenu(self.menu)
        self.gridLayout.addWidget(self.menubut, 0, 8, 1, 1)
        
        #list of sources for user to choose from 
        self.sourcetable = pg.TreeWidget(self.win)
        self.sourcetable.setSelectionMode(2)
        for source in newmap.allsources:
            if len(source.split()) < 10:
                i = QtGui.QTreeWidgetItem([source.split()[0]])
                self.sourcetable.addTopLevelItem(i)
                degree_sign= u'\N{DEGREE SIGN}'
                ra = QtGui.QTreeWidgetItem(["Ra: " + source.split()[1] + "h " + source.split()[2] 
                                            + "m " + source.split()[3] + "s"])
                dec = QtGui.QTreeWidgetItem(["Dec: " + source.split()[4] + "%s " %degree_sign 
                                            + source.split()[5] + "' " + source.split()[6] + "\""])
                i.addChild(ra)
                i.addChild(dec)
        self.sourcetable.sortItems(0, 0) 
        self.sourcetable.headerItem().setText(0, "Sources (J2000)")
        self.gridLayout.addWidget(self.sourcetable, 1, 0, 21, 1)
        
        #spinbox for user to change the speed of the timelapse
        self.spdlabel = QtGui.QLabel(self.win)
        self.spdlabel.setText("<body style=\" font-size:8pt;\">""Time-lapse Speed (0 = Live):")
        self.gridLayout.addWidget(self.spdlabel, 5, 8, 1, 1)
        self.spdspin = pg.SpinBox(value=0, int=True, minStep=1, step=1)
        self.gridLayout.addWidget(self.spdspin, 6, 8, 1, 1)
        
        #frames per second label in order to see performance
        self.fpslabel = QtGui.QLabel(self.win)
        self.fpslabel.setText("")
        self.gridLayout.addWidget(self.fpslabel, 22, 0, 1, 1)
        
        #labels for az, el, ra, dec of source/antenna/target
        self.clicklabel = QtGui.QLabel(self.win)
        self.clicklabel.setText("Clicked Source: ")
        self.gridLayout.addWidget(self.clicklabel, 15, 1, 1, 1)
        self.azlabel = QtGui.QLabel(self.win)
        self.azlabel.setText("Clicked Az: ")
        self.gridLayout.addWidget(self.azlabel, 16, 1, 1, 1)
        self.ellabel = QtGui.QLabel(self.win)
        self.ellabel.setText("Clicked El: ")
        self.gridLayout.addWidget(self.ellabel, 16, 2, 1, 1)
        self.ralabel = QtGui.QLabel(self.win)
        self.ralabel.setText("Clicked Ra: ")
        self.gridLayout.addWidget(self.ralabel, 17, 1, 1, 1)
        self.declabel = QtGui.QLabel(self.win)
        self.declabel.setText("Clicked Dec: ")
        self.gridLayout.addWidget(self.declabel, 17, 2, 1, 1)
        
        self.antlabel = QtGui.QLabel(self.win)
        self.antlabel.setText("<body style=\" font-size:12pt;\">""Sky Map Information:")
        self.gridLayout.addWidget(self.antlabel, 1, 8, 1, 1)
        self.pauselabel = QtGui.QLabel(self.win)
        self.pauselabel.setText("<body style=\" font-size:8pt;\">""Paused: NO")
        self.gridLayout.addWidget(self.pauselabel, 2, 8, 1, 1)
        self.tracklabel = QtGui.QLabel(self.win)
        self.tracklabel.setText("<body style=\" font-size:8pt;\">""Source Tracking: OFF")
        self.gridLayout.addWidget(self.tracklabel, 3, 8, 1, 1)
        self.track2label = QtGui.QLabel(self.win)
        self.track2label.setText("<body style=\" font-size:8pt;\">""Antenna Tracking: OFF")
        self.gridLayout.addWidget(self.track2label, 4, 8, 1, 1)
        
        
        self.cmdazlabel = QtGui.QLabel(self.win)
        self.cmdazlabel.setText("<body style=\" color: blue;\">""Cmd Az-El: 00.00 00.00")
        self.gridLayout.addWidget(self.cmdazlabel, 22, 1, 1, 1)
        self.actazlabel = QtGui.QLabel(self.win)
        self.actazlabel.setText("<body style=\" color: green;\">""Actual Az-El: 00.00 00.00")
        self.gridLayout.addWidget(self.actazlabel, 23, 1, 1, 1)
        self.azofflabel = QtGui.QLabel(self.win)
        self.azofflabel.setText("Az-El Offset: 00.00 00.00")
        self.gridLayout.addWidget(self.azofflabel, 24, 1, 1, 1)
        self.usrofflabel = QtGui.QLabel(self.win)
        self.usrofflabel.setText("Usr Offset: 00.00 00.00")
        self.gridLayout.addWidget(self.usrofflabel, 22, 2, 1, 1)
        
        self.targetlabel = QtGui.QLabel(self.win)
        self.targetlabel.setText("<body style=\" color: red;\">""Target Source: ")
        self.gridLayout.addWidget(self.targetlabel, 15, 3, 1, 1)
        self.onlabel = QtGui.QLabel(self.win)
        self.onlabel.setText("On Source: False")
        self.gridLayout.addWidget(self.onlabel, 15, 4, 1, 1)
        self.tarazlabel = QtGui.QLabel(self.win)
        self.tarazlabel.setText("Target Az: ")
        self.gridLayout.addWidget(self.tarazlabel, 16, 3, 1, 1)
        self.tarellabel = QtGui.QLabel(self.win)
        self.tarellabel.setText("Target El: ")
        self.gridLayout.addWidget(self.tarellabel, 16, 4, 1, 1)
        self.tarralabel = QtGui.QLabel(self.win)
        self.tarralabel.setText("Target Ra: ")
        self.gridLayout.addWidget(self.tarralabel, 17, 3, 1, 1)
        self.tardeclabel = QtGui.QLabel(self.win)
        self.tardeclabel.setText("Target Dec: ")
        self.gridLayout.addWidget(self.tardeclabel, 17, 4, 1, 1)
        
        self.biaslabel = QtGui.QLabel(self.win)
        self.biaslabel.setText("Offsets and Tilts: ")
        self.gridLayout.addWidget(self.biaslabel, 15, 5, 1, 1)
        self.azb1label = QtGui.QLabel(self.win)
        self.azb1label.setText("azbias1: ")
        self.gridLayout.addWidget(self.azb1label, 16, 5, 1, 1)
        self.azb2label = QtGui.QLabel(self.win)
        self.azb2label.setText("azbias2: ")
        self.gridLayout.addWidget(self.azb2label, 17, 5, 1, 1)
        self.elblabel = QtGui.QLabel(self.win)
        self.elblabel.setText("elbias: ")
        self.gridLayout.addWidget(self.elblabel, 18, 5, 1, 1)
        
        self.subreflabel = QtGui.QLabel(self.win)
        self.subreflabel.setText("Subreflector: ")
        self.gridLayout.addWidget(self.subreflabel, 15, 6, 1, 1)
        self.subxlabel = QtGui.QLabel(self.win)
        self.subxlabel.setText("subdx: ")
        self.gridLayout.addWidget(self.subxlabel, 16, 6, 1, 1)
        self.subylabel = QtGui.QLabel(self.win)
        self.subylabel.setText("subdy: ")
        self.gridLayout.addWidget(self.subylabel, 17, 6, 1, 1)
        self.subzlabel = QtGui.QLabel(self.win)
        self.subzlabel.setText("subdz: ")
        self.gridLayout.addWidget(self.subzlabel, 18, 6, 1, 1)
        self.subpxlabel = QtGui.QLabel(self.win)
        self.subpxlabel.setText("subdpx: ")
        self.gridLayout.addWidget(self.subpxlabel, 19, 6, 1, 1)
        self.subpylabel = QtGui.QLabel(self.win)
        self.subpylabel.setText("subdpy: ")
        self.gridLayout.addWidget(self.subpylabel, 20, 6, 1, 1)
        
        self.timinglabel = QtGui.QLabel(self.win)
        self.timinglabel.setText("Timing: ")
        self.gridLayout.addWidget(self.timinglabel, 15, 7, 1, 1)
        self.dtlabel = QtGui.QLabel(self.win)
        self.dtlabel.setText("deltdt: ")
        self.gridLayout.addWidget(self.dtlabel, 16, 7, 1, 1)
        self.dut1label = QtGui.QLabel(self.win)
        self.dut1label.setText("dut1: ")
        self.gridLayout.addWidget(self.dut1label, 17, 7, 1, 1)
        self.atlabel = QtGui.QLabel(self.win)
        self.atlabel.setText("deltat: ")
        self.gridLayout.addWidget(self.atlabel, 18, 7, 1, 1)
        
        self.weatherlabel = QtGui.QLabel(self.win)
        self.weatherlabel.setText("Weather: ")
        self.gridLayout.addWidget(self.weatherlabel, 15, 8, 1, 1)
        self.tdklabel = QtGui.QLabel(self.win)
        self.tdklabel.setText("tdk: ")
        self.gridLayout.addWidget(self.tdklabel, 16, 8, 1, 1)
        self.dewptlabel = QtGui.QLabel(self.win)
        self.dewptlabel.setText("dewpt: ")
        self.gridLayout.addWidget(self.dewptlabel, 17, 8, 1, 1)
        self.rhlabel = QtGui.QLabel(self.win)
        self.rhlabel.setText("rh: ")
        self.gridLayout.addWidget(self.rhlabel, 18, 8, 1, 1)
        self.pmblabel = QtGui.QLabel(self.win)
        self.pmblabel.setText("pmb: ")
        self.gridLayout.addWidget(self.pmblabel, 19, 8, 1, 1)
        
        self.skinfolabel = QtGui.QLabel(self.win)
        self.skinfolabel.setText("<body style=\" font-size:12pt;\">""Schedule Information: ")
        self.gridLayout.addWidget(self.skinfolabel, 7, 8, 1, 1)
        self.intlabel = QtGui.QLabel(self.win)
        self.intlabel.setText("<body style=\" font-size:8pt;\">""int time: ")
        self.gridLayout.addWidget(self.intlabel, 8, 8, 1, 1)
        self.npairlabel = QtGui.QLabel(self.win)
        self.npairlabel.setText("<body style=\" font-size:8pt;\">""npairs: ")
        self.gridLayout.addWidget(self.npairlabel, 9, 8, 1, 1)
        self.npointlabel = QtGui.QLabel(self.win)
        self.npointlabel.setText("<body style=\" font-size:8pt;\">""npoints: ")
        self.gridLayout.addWidget(self.npointlabel, 10, 8, 1, 1)
        self.durlabel = QtGui.QLabel(self.win)
        self.durlabel.setText("<body style=\" font-size:8pt;\">""duration: ")
        self.gridLayout.addWidget(self.durlabel, 11, 8, 1, 1)
        
        self.swinfolabel = QtGui.QLabel(self.win)
        self.swinfolabel.setText("<body style=\" font-size:12pt;\">""Switcher Info: ")
        self.gridLayout.addWidget(self.swinfolabel, 21, 5, 1, 1)
        self.freqlabel = QtGui.QLabel(self.win)
        self.freqlabel.setText("Frequency: ")
        self.gridLayout.addWidget(self.freqlabel, 22, 5, 1, 1)
        self.reclabel = QtGui.QLabel(self.win)
        self.reclabel.setText("Receiver: ")
        self.gridLayout.addWidget(self.reclabel, 23, 5, 1, 1)
        self.bswlabel = QtGui.QLabel(self.win)
        self.bswlabel.setText("bsw status: ")
        self.gridLayout.addWidget(self.bswlabel, 24, 5, 1, 1)
        self.dfreqlabel = QtGui.QLabel(self.win)
        self.dfreqlabel.setText("dicke freq: ")
        self.gridLayout.addWidget(self.dfreqlabel, 25, 5, 1, 1)
        self.dbllabel = QtGui.QLabel(self.win)
        self.dbllabel.setText("dicke bl: ")
        self.gridLayout.addWidget(self.dbllabel, 22, 6, 1, 1)
        self.fswlabel = QtGui.QLabel(self.win)
        self.fswlabel.setText("freq switch: ")
        self.gridLayout.addWidget(self.fswlabel, 23, 6, 1, 1)
        self.foffslabel = QtGui.QLabel(self.win)
        self.foffslabel.setText("freq soffs: ")
        self.gridLayout.addWidget(self.foffslabel, 24, 6, 1, 1)
        
        self.swinfolabel = QtGui.QLabel(self.win)
        self.swinfolabel.setText("<body style=\" font-size:12pt;\">""Other Info: ")
        self.gridLayout.addWidget(self.swinfolabel, 21, 7, 1, 1)
        self.vclabel = QtGui.QLabel(self.win)
        self.vclabel.setText("vc offset: ")
        self.gridLayout.addWidget(self.vclabel, 22, 7, 1, 1)
        self.ifofflabel = QtGui.QLabel(self.win)
        self.ifofflabel.setText("if off: ")
        self.gridLayout.addWidget(self.ifofflabel, 23, 7, 1, 1)
        self.ifoffalabel = QtGui.QLabel(self.win)
        self.ifoffalabel.setText("if offa: ")
        self.gridLayout.addWidget(self.ifoffalabel, 24, 7, 1, 1)
        self.radecofflabel = QtGui.QLabel(self.win)
        self.radecofflabel.setText("ra dec off: ")
        self.gridLayout.addWidget(self.radecofflabel, 25, 7, 1, 1)
        self.azellabel = QtGui.QLabel(self.win)
        self.azellabel.setText("azel: ")
        self.gridLayout.addWidget(self.azellabel, 22, 8, 1, 1)
        self.callabel = QtGui.QLabel(self.win)
        self.callabel.setText("cal: ")
        self.gridLayout.addWidget(self.callabel, 23, 8, 1, 1)
        self.lorflabel = QtGui.QLabel(self.win)
        self.lorflabel.setText("lorf: ")
        self.gridLayout.addWidget(self.lorflabel, 24, 8, 1, 1)
        self.lomullabel = QtGui.QLabel(self.win)
        self.lomullabel.setText("lo mul: ")
        self.gridLayout.addWidget(self.lomullabel, 25, 8, 1, 1)
        
        #read schedule file and display with the current line colored red
        self.skdtext = QtGui.QTextEdit()
        if not newmap.skdfile == "(null)":
            skd = open(newmap.skdfile, 'r')
            textlines = skd.readlines()
            text = '<pre>'
            text2 = ''
            curr = ''
            c = 0
            atcurr = False
            for line in textlines:
                if c == newmap.skdline:
                    curr = line
                    atcurr = True
                elif not atcurr:
                    text = text + "\n" + line.rstrip() 
                elif atcurr:
                    text2 = text2  + "\n" + line.rstrip() 
                c += 1
            self.skdtext.setText('<span>%s</span><pre><span style="color: #FF0000;">%s</span><span>%s</span>' 
                                 %(text, curr, text2))
        else:
            self.skdtext.setText('No Active Schedule')
            
        self.skdtext.setFont(QtGui.QFont ("Arial", 8))
        self.skdtext.setReadOnly(True)
        self.gridLayout.addWidget(self.skdtext, 12, 8, 3, 1)
        
        #set range and labels of axes
        self.p = self.plot
        self.p.showGrid(x = True, y = True)
        self.p.addLine(y = 5, pen = "r")
        self.p.setRange(xRange=[0, 360], yRange=[0, 90], padding = 0)
        self.p.setLabels(left = "Elevation", bottom = "Azimuth")
        self.p.getViewBox().setLimits(xMin = 0, xMax = 360, yMin = -90, yMax = 90)
        self.azstrip.setLabels(left = "Az Offset")
        self.elstrip.setLabels(left = "El Offset")
        self.azstrip.getAxis('bottom').setStyle(showValues = False)
        self.elstrip.getAxis('bottom').setStyle(showValues = False)
        self.vb = self.p.plotItem.vb
        
        #button to clear selected sources
        self.clearselbut = QtGui.QPushButton("Clear")
        self.gridLayout.addWidget(self.clearselbut, 0, 0, 1, 1)
        self.clearselbut.clicked.connect(self.clear_selsources)
        
        self.win.show()
        
        self.proxy = pg.SignalProxy(self.p.scene().sigMouseClicked, rateLimit = 60, slot=self.mouseClicked)
        
        self.lastTime = time()
        self.fps = None
        self.numselitems = 0
        self.prev_skdline = newmap.skdline
        self.grid_decazs, self.grid_decels = newmap.get_const_decgrid()
        self.grid_raazs, self.grid_raels = newmap.get_const_ragrid()
        
    def pause(self):
        """Pauses the source map so that the time stays constant."""
        
        if self.newmap.paused == True:
            self.newmap.paused = False
            self.pauselabel.setText("<body style=\" font-size:8pt;\">""Paused: NO")
        else:
            self.newmap.paused = True
            self.pauselabel.setText("<body style=\" color: red;font-size:8pt;\">""Paused: YES")
            
    def set_time(self):
        """Pauses the source map and changes the time to the user specified UT."""
        
        self.newmap.paused = True
        self.pauselabel.setText("<body style=\" color: red;font-size:8pt;\">""Paused: YES")
        utyear, ok1 = QtGui.QInputDialog.getText(self.win, 'New UT 1/6', 
            'Enter Year:')
        
        utmon, ok2 = QtGui.QInputDialog.getText(self.win, 'New UT 2/6', 
            'Enter Month:')
        
        utday, ok3 = QtGui.QInputDialog.getText(self.win, 'New UT 3/6', 
            'Enter Day:')
            
        uthour, ok4 = QtGui.QInputDialog.getText(self.win, 'New UT 4/6', 
            'Enter Hour:')
        
        utmin, ok5 = QtGui.QInputDialog.getText(self.win, 'New UT 5/6', 
            'Enter Minute:')
            
        utsec, ok6 = QtGui.QInputDialog.getText(self.win, 'New UT 6/6', 
            'Enter Second:')    
            
        try:
            ntime = (datetime.datetime(int(utyear),
                                       int(utmon),
                                       int(utday),
                                       int(uthour),
                                       int(utmin),
                                       int(utsec)))    
            if ntime.year > 5520:
                raise ValueError
                
            self.newmap.time = ntime
            self.newmap.set_time(ntime)
        except ValueError:
            self.newmap.paused = False
            

    def add(self):
        """Adds a user specified celestial object to the list of sources and 
        allows for it to be plotted.
        """
        name, ok1 = QtGui.QInputDialog.getText(self.win, 'Add Celestial Object', 
                                              'Enter Name (No Spaces): ') 
        ra, ok2 = QtGui.QInputDialog.getText(self.win, 'Add Celestial Object', 
                                              'Enter Ra (hms, J2000): ') 
        dec, ok3 = QtGui.QInputDialog.getText(self.win, 'Add Celestial Object', 
                                              'Enter Dec (dms, J2000): ') 

        source = name + " " + ra + " " + dec + " 2000" + " 0.0"
        source = str(source)
        if self.newmap.is_dataline(source):        
            self.newmap.added_sources.append(source)
            self.newmap.allsources.insert(0, source)
        
    def remove(self):
        """Removes the user added celestial objects from the sky map."""
        
        l = len(self.newmap.added_sources)
        self.newmap.added_sources = []
        for i in range (0,l):
            del self.newmap.allsources[0]
            
    def reset_axes(self):
        """Resets the axes to original dimensions after user has changed them."""
        
        self.p.setRange(xRange=[0, 360], yRange=[0, 90], padding = 0)

    def clear_path(self):
        """Clears the path drawn on the plot from tracking the clicked source 
        and the antenna.
        """
        
        self.newmap.clickazpoints = []
        self.newmap.clickelpoints = []
        self.newmap.antazpoints = []
        self.newmap.antelpoints = []
    
    def clear_selsources(self):
        """Clears the source table so that no sources are selected."""
        
        self.sourcetable.clearSelection()
    
    def toggle_track(self):
        """Toggles whether or not the plot should be tracking a source"""
        
        if self.newmap.toggletrack == False:
            self.newmap.clickazpoints = []
            self.newmap.clickelpoints = []
            self.newmap.toggletrack = True
            self.tracklabel.setText("<body style=\" color: red;font-size:8pt;\">""Source Tracking: ON")
        else:
            self.newmap.toggletrack = False
            self.tracklabel.setText("<body style=\" font-size:8pt;\">""Source Tracking: OFF")

    def toggle_track_ant(self):
        """Toggles whether or not the plot should be tracking a the antenna"""
        
        if self.newmap.toggletrack_ant == False:
            self.newmap.antazpoints = []
            self.newmap.antelpoints = []
            self.newmap.toggletrack_ant = True
            self.track2label.setText("<body style=\" color: red;font-size:8pt;\">""Antenna Tracking: ON")
        else:
            self.newmap.toggletrack_ant = False
            self.track2label.setText("<body style=\" font-size:8pt;\">""Antenna Tracking: OFF")
            
    def toggle_ephems(self):
        """Toggles whether or not solar system bodies appear on the map."""
        if not len(self.newmap.tarsource.split()) > 9:
            if self.newmap.toggle_ephem == False:
                self.newmap.toggle_ephem = True
            else:
                self.newmap.toggle_ephem = False
        else:
            self.newmap.toggle_ephem = True
    
    def toggle_radecgrid(self):
        """Toggles whether or not the ra/dec grid appears on the map."""
        
        if self.newmap.togglegrid == False:
            self.newmap.togglegrid = True
        else:
            self.newmap.togglegrid = False
    
    def toggle_strips(self):
        """Toggles whether or not the strip charts are displaying the offsets."""
        
        if self.newmap.togglestrips == False:
            self.newmap.azoffset_data = [0]
            self.newmap.eloffset_data = [0]
            self.newmap.striptime = [0]
            self.newmap.togglestrips = True
        else:
            self.newmap.togglestrips = False

    def new_sourcelist(self):
        """Restarts the program so the user can choose a new source list."""
        
        import os
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
    def mouseClicked(self, evt):
        """Determines whether or not the user clicked on a source and updates the
        plot accordingly.
        
        Args:
            evt (MouseClickEvent): Specific coordinates corresponding to where
                the mouse was clicked
        """

        pos = evt[0].scenePos() 
        if self.p.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            
            #change source if user clicked on a new source
            for source in self.newmap.allsources:
                if (mousePoint.x() < self.newmap.get_source_coords(source)[1] + 1 and 
                   mousePoint.x() > self.newmap.get_source_coords(source)[1] - 1 and 
                   mousePoint.y() < self.newmap.get_source_coords(source)[2] + 1 and 
                   mousePoint.y() > self.newmap.get_source_coords(source)[2] - 1):
                    if self.newmap.is_dataline(source):
                        self.newmap.choose_source(self.newmap.get_source_coords(source)[0]) 
                        return
                    else:
                        if self.newmap.toggle_ephem:
                            self.newmap.choose_source(self.newmap.get_source_coords(source)[0])
                            return
        self.newmap.clicksource = ''                
        self.newmap.clickazpoint = ''
        self.newmap.clickelpoint = ''
                   
    def update(self):
        """Updates the sky map gui application to show sources at the correct location
        for the displayed universal time.    
        """
        
        self.counter = self.counter + 1
        #must clear plot after every update
        self.p.clear()
        self.azstrip.clear()
        self.elstrip.clear()
        
        #update the speed of the timelapse given current user settings
        self.newmap.speed = self.spdspin.value()
        
        #update coordinates and labels 
        self.newmap.update()
        
        degree_sign= u'\N{DEGREE SIGN}'
        k = self.newmap.clickra.find('.')
        self.ralabel.setText(" Clicked Ra: %s" % (self.newmap.clickra[:k] + self.newmap.clickra[k:k+4]))
        i = self.newmap.clickdec.find('.')
        self.declabel.setText(" Clicked Dec: %s" % (self.newmap.clickdec[:i] + self.newmap.clickdec[i:i+4]))
        
        j = self.newmap.tarra.find('.')
        self.tarralabel.setText(" Target Ra: %s" 
                           % (self.newmap.tarra[:j] + self.newmap.tarra[j:j+4]))
        m = self.newmap.tardec.find('.')
        self.tardeclabel.setText(" Target Dec: %s" 
                            % (self.newmap.tardec[:m] + self.newmap.tardec[m:m+4]))
        
        self.onlabel.setText("On Source: %s" % self.newmap.onsource)
        
        self.actazlabel.setText("<body style=\" color: green;\">""Actual Az-El: %.2f" 
                               % (self.newmap.antazpoint) + degree_sign + " %.2f" 
                               % (self.newmap.antelpoint) + degree_sign)
        self.cmdazlabel.setText("<body style=\" color: blue;\">""Cmd Az-El: %.2f" 
                               % (self.newmap.cmdazpoint) + degree_sign + " %.2f" 
                               % (self.newmap.cmdelpoint) + degree_sign)
        
        self.azofflabel.setText("Az-El Offset: %.3f" 
                               % (self.newmap.azoff) + degree_sign + " %.3f" 
                               % (self.newmap.eloff) + degree_sign)
        
        self.usrofflabel.setText("Usr Offset: %s" % self.newmap.usr_offs)
        
        self.azb1label.setText("azbias1: %s" % self.newmap.azbias1)
        self.azb2label.setText("azbias2: %s" % self.newmap.azbias2)
        self.elblabel.setText("elbias: %s" % self.newmap.elbias)
        
        self.subxlabel.setText("subdx: %s" % self.newmap.subdx)
        self.subylabel.setText("subdy: %s" % self.newmap.subdy)
        self.subzlabel.setText("subdz: %s" % self.newmap.subdz)
        self.subpxlabel.setText("subdpx: %s" % self.newmap.subdpx)
        self.subpylabel.setText("subdpy: %s" % self.newmap.subdpy)
        
        self.dtlabel.setText("deltdt: %s" % self.newmap.deltdt)
        self.dut1label.setText("dut1: %s" % self.newmap.dut1)
        self.atlabel.setText("deltat: %s" % self.newmap.deltat)
        
        self.tdklabel.setText("tdk: %s" % self.newmap.tdk)
        self.dewptlabel.setText("dewpt: %s" % self.newmap.dewpt)
        self.rhlabel.setText("rh: %s" % self.newmap.rh)
        self.pmblabel.setText("pmb: %s" % self.newmap.pmb)
        
        self.intlabel.setText("<body style=\" font-size:8pt;\">""int time: %s" % self.newmap.inttime)
        self.npairlabel.setText("<body style=\" font-size:8pt;\">""npairs: %s" % self.newmap.npairs)
        self.npointlabel.setText("<body style=\" font-size:8pt;\">""npoints: %s" % self.newmap.npoints)
        self.durlabel.setText("<body style=\" font-size:8pt;\">""duration: %s" % self.newmap.duration)
        
        self.freqlabel.setText("frequency: %s" % self.newmap.freq)
        self.reclabel.setText("receiver: %s" % self.newmap.rec)
        self.bswlabel.setText("bsw status: %s" % self.newmap.bsw)
        self.dfreqlabel.setText("dicke freq: %s" % self.newmap.dfreq)
        self.dbllabel.setText("dicke bl: %s" % self.newmap.dbl)
        self.fswlabel.setText("freq switch: %s" % self.newmap.fsw)
        self.foffslabel.setText("freq soffs: %s" % self.newmap.foffs)
        
        self.vclabel.setText("vc offset: %s" % self.newmap.vc)
        self.ifofflabel.setText("if off: %s" % self.newmap.ifoff)
        self.ifoffalabel.setText("ifoffa: %s" % self.newmap.ifoffa)
        self.radecofflabel.setText("ra dec off: %s" % self.newmap.radecoff)
        self.azellabel.setText("azel: %s" % self.newmap.azel)
        self.callabel.setText("cal: %s" % self.newmap.cal)
        self.lorflabel.setText("lorf: %s" % self.newmap.lorf)
        self.lomullabel.setText("lo mul: %s" % self.newmap.lomult)
        
        #read schedule file and display with the current line colored red
        if not self.newmap.skdfile == "(null)":  
            skd = open(self.newmap.skdfile, 'r')
            textlines = skd.readlines()
            text = '<pre>'
            text2 = ''
            curr = ''
            c = 0
            atcurr = False
            for line in textlines:
                if c == self.newmap.skdline:
                    curr = line
                    atcurr = True
                elif not atcurr:
                    text = text + "\n" + line.rstrip() 
                elif atcurr:
                    text2 = text2  + "\n" + line.rstrip() 
                c += 1
            
            if not self.newmap.skdline == self.prev_skdline:
                self.skdtext.setText('<span>%s</span><pre><span style="color: #FF0000;">%s</span><span>%s</span>' %(text, curr, text2))
                self.prev_skdline = self.newmap.skdline
            
        else:
            self.prev_skdline = self.newmap.skdline
            self.skdtext.setText('No Active Schedule')
        
        if not len(self.sourcetable.selectedItems()) == self.numselitems:
            self.newmap.selectedsources = []
            for cell in self.sourcetable.selectedItems():
                for source in self.newmap.allsources:
                    if cell.text(0) == source.split()[0]:
                        self.newmap.selectedsources.append(source)
        
        #plot the last 100 points of offset data contained in the source map                
        if self.newmap.togglestrips: 
            self.azstrip.setRange(yRange=[-1, 1], padding = 0)     
            self.elstrip.setRange(yRange=[-1, 1], padding = 0) 
            if np.abs(self.newmap.azoff) > 1:
                self.azstrip.getViewBox().enableAutoRange()
            if np.abs(self.newmap.eloff) > 1:
                self.elstrip.getViewBox().enableAutoRange()
                
            if len(self.newmap.azoffset_data) < 100:
                azplot = pg.PlotCurveItem(x = self.newmap.striptime, y = self.newmap.azoffset_data)
                self.azstrip.addItem(azplot)
                elplot = pg.PlotCurveItem(x = self.newmap.striptime, y = self.newmap.eloffset_data)
                self.elstrip.addItem(elplot)
            else:
                azplot = pg.PlotCurveItem(x = self.newmap.striptime[-100:], y = self.newmap.azoffset_data[-100:])
                self.azstrip.addItem(azplot)  
                elplot = pg.PlotCurveItem(x = self.newmap.striptime[-100:], y = self.newmap.eloffset_data[-100:])
                self.elstrip.addItem(elplot)               
            
        #plots ra and dec gridlines with labels
        if self.newmap.togglegrid == True:
            if self.counter%5 == 0: #update ra grid periodically (improves framerate)
                self.grid_raazs, self.grid_raels = self.newmap.get_const_ragrid()
            for i in range(0,len(self.grid_raazs)):
                grid = pg.PlotCurveItem(x = self.grid_raazs[i][:-1], y = self.grid_raels[i][:-1], 
                                        pen = pg.mkPen(color = (100,100,100)))
                self.p.addItem(grid)
            for i in range(0,len(self.grid_decazs)):
                grid2 = pg.PlotCurveItem(x = self.grid_decazs[i], y = self.grid_decels[i], 
                                         pen = pg.mkPen(color = (205,103,0)))
                self.p.addItem(grid2)
            for i in range (0,12):
                gridlabel = pg.TextItem(text = "Ra: %s" %(str(2*i)) + "h", 
                                        color = (100,100,100))
                self.p.addItem(gridlabel)
                gridlabel.setPos(self.grid_raazs[i][80], self.grid_raels[i][80])
                gridlabel2 = pg.TextItem(text = "Dec: %s" %(str(-90 + i*15)) + degree_sign, 
                                         color = (205,103,0))
                self.p.addItem(gridlabel2)
                gridlabel2.setPos(self.grid_decazs[i][40], self.grid_decels[i][40])
                
        #update the positions of all sources in the map    
        curve = pg.ScatterPlotItem(x = self.newmap.azpoints, y = self.newmap.elpoints, size = 3, 
                                   pen = 'w', brush = 'w', symbol = "o")
        
        curve.addPoints(x = [self.newmap.cmdazpoint], y = [self.newmap.cmdelpoint], size = 40,
                        pen = 'w', brush = pg.mkBrush(color = (0,0,0)), symbol = "+")                     
        curve.addPoints(x = [self.newmap.antazpoint], y = [self.newmap.antelpoint], size = 18, 
                        pen = 'g', brush = 'g', symbol = "+")
        
        #draw tick marks corresponding to antenna position information                
        azticksize = (self.p.viewRange()[1][1] - self.p.viewRange()[1][0])*.05
        elticksize = (self.p.viewRange()[0][1] - self.p.viewRange()[0][0])*.025
        cmdtick = pg.PlotCurveItem(x = [self.newmap.cmdazpoint, self.newmap.cmdazpoint], 
                                   y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], 
                                   pen= 'w')
        self.p.addItem(cmdtick)
        cmdtick2 = pg.PlotCurveItem(x = [self.p.viewRange()[0][0],self.p.viewRange()[0][0]+elticksize], 
                                    y = [self.newmap.cmdelpoint, self.newmap.cmdelpoint], 
                                    pen= 'w')
        self.p.addItem(cmdtick2)
        if 0 <= self.newmap.wrappoint <= 2*np.pi:
            anttick = pg.PlotCurveItem(x = [self.newmap.antazpoint, self.newmap.antazpoint], 
                                    y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'g')
            self.p.addItem(anttick)
        elif self.newmap.wrappoint > 2*np.pi:
            anttick = pg.PlotCurveItem(x = [self.newmap.antazpoint, self.newmap.antazpoint], 
                                    y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'y')
            self.p.addItem(anttick)
            wraplabel = pg.TextItem(text = "CW", color = 'y')
            wraplabel.setPos(self.newmap.antazpoint, self.p.viewRange()[1][0]+azticksize)
            self.p.addItem(wraplabel)
            wraptick = pg.PlotCurveItem(x = [98.8, 98.8], 
                                    y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'r')
            self.p.addItem(wraptick)
        else:
            anttick = pg.PlotCurveItem(x = [self.newmap.antazpoint, self.newmap.antazpoint], 
                                    y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'y')
            self.p.addItem(anttick)
            wraplabel = pg.TextItem(text = "CCW", color = 'y')
            wraplabel.setPos(self.newmap.antazpoint-12, self.p.viewRange()[1][0]+azticksize)
            self.p.addItem(wraplabel)
            wraptick = pg.PlotCurveItem(x = [258, 258], 
                                    y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'r')
            self.p.addItem(wraptick)
            
        anttick2 = pg.PlotCurveItem(x = [self.p.viewRange()[0][0],self.p.viewRange()[0][0]+elticksize], 
                                 y = [self.newmap.antelpoint, self.newmap.antelpoint], pen= 'g')
        self.p.addItem(anttick2)
        
        #draw the selected sources on the map 
        curve.addPoints(x = self.newmap.sel_azpoints, y = self.newmap.sel_elpoints, size = 7, 
                        pen = 'w', brush = 'b', symbol = 'o')
        
        #draw the added sources on the map
        curve.addPoints(x = self.newmap.add_azpoints, y = self.newmap.add_elpoints, size = 7, 
                        pen = 'w', brush = 'g', symbol = 'o')
        for source in self.newmap.added_sources:
            add_tracktext = pg.TextItem(text = "%s" % source.split()[0], color = 'g')
            self.p.addItem(add_tracktext)       
            add_tracktext.setPos(self.newmap.add_azpoints[self.newmap.added_sources.index(source)], 
                                                          self.newmap.add_elpoints[self.newmap.added_sources.index(source)])
            
        #update the target source information                
        self.targetlabel.setText("<body style=\" color: red;\">""Target Source: " + self.newmap.target)
        
        #if target source is a solar system body make sure they are displayed
        if len(self.newmap.tarsource.split()) > 9:
            self.newmap.toggle_ephem = True
            
        if not self.newmap.target == '':
            curve.addPoints(x = [self.newmap.tarazpoint], y = [self.newmap.tarelpoint], size = 7, 
                            pen = 'w', brush = 'r')    
            tar_tracktext = pg.TextItem(text = "%s" % self.newmap.target, color = 'r')
            self.p.addItem(tar_tracktext)       
            tar_tracktext.setPos(self.newmap.tarazpoint, self.newmap.tarelpoint)
            self.tarazlabel.setText(" Target Az: %.2f" 
                               % (self.newmap.tarazpoint) + degree_sign)
            self.tarellabel.setText(" Target El: %.2f" 
                               % (self.newmap.tarelpoint) + degree_sign)
        else:
            self.tarazlabel.setText(" Target Az: ")
            self.tarellabel.setText(" Target El: ")
            self.tarralabel.setText(" Target Ra: ")
            self.tardeclabel.setText(" Target Dec: ")
        
        #update the clicked source information     
        self.clicklabel.setText("Clicked Source: %s" % self.newmap.clicksource)
        if not self.newmap.clickazpoint == '' and not self.newmap.clickelpoint == '':
            curve.addPoints(x = [self.newmap.clickazpoint], y = [self.newmap.clickelpoint], size = 7, 
                            pen = 'w', brush = 'y')
            tracktext = pg.TextItem(text = "%s" % self.newmap.clicksource, color = 'y')
            self.p.addItem(tracktext)
            tracktext.setPos(self.newmap.clickazpoint, self.newmap.clickelpoint)
            self.azlabel.setText(" Clicked Az: %.2f" % self.newmap.clickazpoint + "%s" %degree_sign)
            self.ellabel.setText(" Clicked El: %.2f" % self.newmap.clickelpoint + "%s" %degree_sign)
        else:
            self.azlabel.setText(" Clicked Az: ")
            self.ellabel.setText(" Clicked El: ")
            self.ralabel.setText(" Clicked Ra: ")
            self.declabel.setText(" Clicked Dec: ")

        
        #update the solar system body positions    
        if self.newmap.toggle_ephem:
            for i in range (len(self.newmap.ephem_azpoints)):
                curve.addPoints(x = [self.newmap.ephem_azpoints[i]], y = [self.newmap.ephem_elpoints[i]], 
                    size = 12, pen = None, brush = pg.mkBrush(color = (int(self.newmap.ephem_colors[i][0]),
                    int(self.newmap.ephem_colors[i][1]),int(self.newmap.ephem_colors[i][2]))), symbol = 'o')
            
        #updates the tracking line of the current source
        curve2 = pg.PlotCurveItem(x = self.newmap.clickazpoints, y = self.newmap.clickelpoints, 
                                  pen = pg.mkPen('y'))
                                  
        curve3 = pg.PlotCurveItem(x = self.newmap.antazpoints, y = self.newmap.antelpoints, 
                                  pen = pg.mkPen('g'))

        self.p.addItem(curve3)
        self.p.addItem(curve2)
        self.p.addItem(curve)
        horizon = pg.LineSegmentROI([[0, 0], [360,0]], 
                                    pen= pg.mkPen('y', style=QtCore.Qt.DotLine))
        self.p.addItem(horizon)
        
        #update number of selected items
        self.numselitems = len(self.sourcetable.selectedItems()) 
            
        #calculate and display fps
        now = time()
        dt = now - self.lastTime
        self.lastTime = now
        if self.fps is None:
            fps = 1.0/dt
        else:
            s = np.clip(dt*3., 0, 1)
            fps = fps * (1-s) + (1.0/dt) * s
        self.fpslabel.setText('- - - - - - - - - - - %0.2f fps' %fps)
        
        ut = str(self.newmap.time)
        i = ut.find(".")
        if i == -1:
            self.p.setTitle("<body style=\" color: white;\">""UT: %s " % ut +
                       " ----- " + "LST: %.2f " % self.newmap.LST + "hrs")
        else:
            self.p.setTitle("<body style=\" color: white;\">""UT: %s " % ut[:i] +
                       " ----- " + "LST: %.2f " % self.newmap.LST + "hrs")
        self.p.repaint()