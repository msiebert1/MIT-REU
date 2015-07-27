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
        
        #main window      
        self.win = QtGui.QWidget()
        self.win.setWindowTitle('Radio Source Sky Map: Haystack Observatory')
        self.win.setWindowIcon(QtGui.QIcon('/home/msiebert/Documents/MIT_REU/37m_GUI/Haystack_Icon.gif'))
        
        self.win.resize(1610,700)
        self.gridLayout = QtGui.QGridLayout(self.win)
        
        #main plot and strip charts
        self.plot = pg.PlotWidget(self.win)
        self.azstrip = pg.PlotWidget(self.win)
        self.elstrip = pg.PlotWidget(self.win)
        
        #set up the general layout
        self.gridLayout.addWidget(self.plot, 0, 1, 15, 8)
        self.gridLayout.addWidget(self.azstrip, 18, 1, 4, 2)
        self.gridLayout.addWidget(self.elstrip, 18, 3, 4, 2)
        self.gridLayout.setColumnStretch(0,0)
        self.gridLayout.setColumnMinimumWidth(0,130)
        self.gridLayout.setColumnStretch(1,0)
        self.gridLayout.setColumnMinimumWidth(1,200)
        self.gridLayout.setColumnStretch(2,0)
        self.gridLayout.setColumnMinimumWidth(2,200)
        self.gridLayout.setColumnStretch(3,0)
        self.gridLayout.setColumnMinimumWidth(3,200)
        self.gridLayout.setColumnStretch(4,0)
        self.gridLayout.setColumnMinimumWidth(4,200)
        
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
        self.gridLayout.addWidget(self.sourcetable, 0, 0, 21, 1)
        
        #spinbox for user to change the speed of the timelapse
        self.spdlabel = QtGui.QLabel(self.win)
        self.spdlabel.setText("Time-lapse Speed (0 = Live)")
        self.gridLayout.addWidget(self.spdlabel, 15, 1, 1, 1)
        self.spdspin = pg.SpinBox(value=0, int=True, minStep=1, step=1)
        self.gridLayout.addWidget(self.spdspin, 15, 2, 1, 1)
        
        #frames per second label in order to see performance
        self.fpslabel = QtGui.QLabel(self.win)
        self.fpslabel.setText("")
        self.gridLayout.addWidget(self.fpslabel, 21, 9, 1, 1)
        
        #labels for az, el, ra, dec of source/antenna/target
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
        self.antlabel.setText("<body style=\" color: green;font-size:10pt;\">""Antenna Information:")
        self.gridLayout.addWidget(self.antlabel, 0, 9, 1, 1)
        self.cmdazlabel = QtGui.QLabel(self.win)
        self.cmdazlabel.setText("<body style=\" font-size:8pt;\">""Cmd Az-El: 00.00 00.00")
        self.gridLayout.addWidget(self.cmdazlabel, 1, 9, 1, 1)
        self.actazlabel = QtGui.QLabel(self.win)
        self.actazlabel.setText("<body style=\" font-size:8pt;\">""Actual Az-El: 00.00 00.00")
        self.gridLayout.addWidget(self.actazlabel, 2, 9, 1, 1)
        self.azofflabel = QtGui.QLabel(self.win)
        self.azofflabel.setText("<body style=\" font-size:8pt;\">""Az-El Offset: 00.00 00.00")
        self.gridLayout.addWidget(self.azofflabel, 3, 9, 1, 1)
        
        self.targetlabel = QtGui.QLabel(self.win)
        self.targetlabel.setText("<body style=\" color: red;\">""Target Source: ")
        self.gridLayout.addWidget(self.targetlabel, 15, 3, 1, 1)
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
        
        #read schedule file and display with the current line colored red
        self.skdtext = QtGui.QTextEdit()
        if not newmap.skdfile == "N/A":
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
        self.gridLayout.addWidget(self.skdtext, 4, 9, 17, 1)
        
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
        
        #pause button to stop the plot from updating
        self.pausebut = QtGui.QPushButton(self.win)
        self.pausebut.setText("Paused: NO")
        self.gridLayout.addWidget(self.pausebut, 15, 5, 1, 1)
        self.pausebut.clicked.connect(self.pause)

        #button to set the new UT
        self.utbut = QtGui.QPushButton()
        self.utbut.setText("- - - Enter New UT - - -")
        self.gridLayout.addWidget(self.utbut, 15, 6, 1, 1)
        self.utbut.clicked.connect(self.set_time)     
        
        #button to enter Umbrella commands
        self.utbut = QtGui.QPushButton()
        self.utbut.setText("- - - Enter Command - - -")
        self.gridLayout.addWidget(self.utbut, 16, 6, 1, 1)
        self.utbut.clicked.connect(self.command)
        
        #button to reset axes    
        self.resetbut = QtGui.QPushButton("Reset Axes")
        self.gridLayout.addWidget(self.resetbut, 16, 5, 1, 1)
        self.resetbut.clicked.connect(self.reset_Axes)
        
        #button to clear track path
        self.clearbut = QtGui.QPushButton("Clear Path")
        self.gridLayout.addWidget(self.clearbut, 17, 5, 1, 1)
        self.clearbut.clicked.connect(self.clear_path)    
        
        #button to clear selected sources
        self.clearselbut = QtGui.QPushButton("Clear")
        self.gridLayout.addWidget(self.clearselbut, 21, 0, 1, 1)
        self.clearselbut.clicked.connect(self.clear_selsources)
        
        #button to toggle tracking        
        self.trackbut = QtGui.QPushButton("Toggle Track: OFF")
        self.gridLayout.addWidget(self.trackbut, 18, 5, 1, 1)
        self.trackbut.clicked.connect(self.toggle_track)
        
        #button to toggle solar system bodies
        self.ephembut = QtGui.QPushButton("Toggle Ephem")
        self.gridLayout.addWidget(self.ephembut, 20, 5, 1, 1)
        self.ephembut.clicked.connect(self.toggle_ephems)
        
        #button to toggle ra/dec grid
        self.gridbut = QtGui.QPushButton("Toggle Ra-Dec Grid")
        self.gridLayout.addWidget(self.gridbut, 19, 5, 1, 1)
        self.gridbut.clicked.connect(self.toggle_radecgrid)
        
        #button to toggle strip charts        
        self.stripbut = QtGui.QPushButton("Toggle Strip Charts")
        self.gridLayout.addWidget(self.stripbut, 21, 5, 1, 1)
        self.stripbut.clicked.connect(self.toggle_strips)
        
        #button to change the source list being displayed
        self.filebut = QtGui.QPushButton("Change Source List")
        self.gridLayout.addWidget(self.filebut, 15, 4, 1, 1)
        self.filebut.clicked.connect(self.new_sourcelist)
        
        self.win.show()
        
        self.proxy = pg.SignalProxy(self.p.scene().sigMouseClicked, rateLimit = 60, slot=self.mouseClicked)
        
        self.lastTime = time()
        self.fps = None
        self.numselitems = 0
        self.prev_skdline = newmap.skdline
        self.grid_decazs, self.grid_decels = newmap.get_const_decgrid()
        
    def pause(self):
        """Pauses the source map so that the time stays constant."""
        
        if self.newmap.paused == True:
            self.newmap.paused = False
            self.pausebut.setText("Paused: NO")
        else:
            self.newmap.paused = True
            self.pausebut.setText("Paused: YES")
            
    def set_time(self):
        """Pauses the source map and changes the time to the user specified UT."""
        
        self.newmap.paused = True
        
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
            self.pausebut.setText("Paused: YES")
        except ValueError:
            self.newmap.paused = False
        
    def command(self):
        
        cmd, ok1 = QtGui.QInputDialog.getText(self.win, 'Umbrella Command', 
            'Enter Command:')
        sys.stdout.write(cmd)
        
            
    def reset_Axes(self):
        """Resets the axes to original dimensions after user has changed them."""
        
        self.p.setRange(xRange=[0, 360], yRange=[0, 90], padding = 0)

    def clear_path(self):
        """Clears the path drawn on the plot from tracking the clicked source."""
        
        self.newmap.clickazpoints = []
        self.newmap.clickelpoints = []
    
    def clear_selsources(self):
        """Clears the source table so that no sources are selected."""
        
        self.sourcetable.clearSelection()
    
    def toggle_track(self):
        """Toggles whether or not the plot should be tracking a source"""
        
        if self.newmap.toggletrack == False:
            self.newmap.toggletrack = True
        else:
            self.newmap.toggletrack = False

    def toggle_ephems(self):
        """Toggles whether or not solar system bodies appear on the map."""
        
        if self.newmap.toggle_ephem == False:
            self.newmap.toggle_ephem = True
        else:
            self.newmap.toggle_ephem = False
    
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
        self.ralabel.setText("Clicked Ra: %s" % (self.newmap.clickra[:k] + self.newmap.clickra[k:k+4]))
        i = self.newmap.clickdec.find('.')
        self.declabel.setText("Clicked Dec: %s" % (self.newmap.clickdec[:i] + self.newmap.clickdec[i:i+4]))
        
        j = self.newmap.tarra.find('.')
        self.tarralabel.setText("Target Ra: %s" 
                           % (self.newmap.tarra[:j] + self.newmap.tarra[j:j+4]))
        m = self.newmap.tardec.find('.')
        self.tardeclabel.setText("Target Dec: %s" 
                            % (self.newmap.tardec[:m] + self.newmap.tardec[m:m+4]))
        
        self.actazlabel.setText("<body style=\" font-size:8pt;\">""Actual Az-El: %.2f" 
                               % (self.newmap.antazpoint) + degree_sign + " %.2f" 
                               % (self.newmap.antelpoint) + degree_sign)
        self.cmdazlabel.setText("<body style=\" font-size:8pt;\">""Cmd Az-El: %.2f" 
                               % (self.newmap.cmdazpoint) + degree_sign + " %.2f" 
                               % (self.newmap.cmdelpoint) + degree_sign)
        
        #read schedule file and display with the current line colored red
        if not self.newmap.skdfile == "N/A":                       
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
            self.skdtext.setText('No Active Schedule')
            
        if not len(self.sourcetable.selectedItems()) == self.numselitems:
            self.newmap.selectedsources = []
            for cell in self.sourcetable.selectedItems():
                for source in self.newmap.allsources:
                    if cell.text(0) == source.split()[0]:
                        self.newmap.selectedsources.append(source)
        
        #plot the last 100 points of offset data contained in the source map                
        if self.newmap.togglestrips:                 
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
            grid_raazs, grid_raels = self.newmap.get_const_ragrid()
            for i in range(0,len(grid_raazs)):
                grid = pg.PlotCurveItem(x = grid_raazs[i][:-1], y = grid_raels[i][:-1], 
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
                gridlabel.setPos(grid_raazs[i][80], grid_raels[i][80])
                gridlabel2 = pg.TextItem(text = "Dec: %s" %(str(-90 + i*15)) + degree_sign, 
                                         color = (205,103,0))
                self.p.addItem(gridlabel2)
                gridlabel2.setPos(self.grid_decazs[i][40], self.grid_decels[i][40])
                
        #update the positions of all sources in the map    
        curve = pg.ScatterPlotItem(x = self.newmap.azpoints, y = self.newmap.elpoints, size = 3, 
                                   pen = 'w', brush = 'w', symbol = "o")
        
        curve.addPoints(x = [self.newmap.cmdazpoint], y = [self.newmap.cmdelpoint], size = 30,
                        pen = pg.mkPen(color = (0,151,255)), brush = pg.mkBrush(color = (0,0,0)), symbol = "+")                     
        curve.addPoints(x = [self.newmap.antazpoint], y = [self.newmap.antelpoint], size = 17, 
                        pen = 'g', brush = 'g', symbol = "+")
        
        #draw tick marks corresponding to antenna position information                
        azticksize = (self.p.viewRange()[1][1] - self.p.viewRange()[1][0])*.05
        elticksize = (self.p.viewRange()[0][1] - self.p.viewRange()[0][0])*.025
        cmdtick = pg.PlotCurveItem(x = [self.newmap.cmdazpoint, self.newmap.cmdazpoint], 
                                   y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], 
                                   pen= pg.mkPen(color = (0,151,255)))
        self.p.addItem(cmdtick)
        cmdtick2 = pg.PlotCurveItem(x = [self.p.viewRange()[0][0],self.p.viewRange()[0][0]+elticksize], 
                                    y = [self.newmap.cmdelpoint, self.newmap.cmdelpoint], 
                                    pen= pg.mkPen(color = (0,151,255)))
        self.p.addItem(cmdtick2)
        anttick = pg.PlotCurveItem(x = [self.newmap.antazpoint, self.newmap.antazpoint], 
                                y = [self.p.viewRange()[1][0],self.p.viewRange()[1][0]+azticksize], pen= 'g')
        self.p.addItem(anttick)
        anttick2 = pg.PlotCurveItem(x = [self.p.viewRange()[0][0],self.p.viewRange()[0][0]+elticksize], 
                                 y = [self.newmap.antelpoint, self.newmap.antelpoint], pen= 'g')
        self.p.addItem(anttick2)
        
        #draw the selected sources on the map 
        curve.addPoints(x = self.newmap.sel_azpoints, y = self.newmap.sel_elpoints, size = 7, 
                        pen = 'w', brush = 'b', symbol = 'o')
        
        #update the target source information                
        self.targetlabel.setText("<body style=\" color: red;\">""Target Source: " + self.newmap.target)
        
        #if target source is a solar system body do not allow user to toggle ephem
        if len(self.newmap.tarsource.split()) > 9:
            self.newmap.toggle_ephem = True
            self.ephembut.setEnabled(False)
        else:
            self.ephembut.setEnabled(True)
            
        if not self.newmap.target == '':
            curve.addPoints(x = [self.newmap.tarazpoint], y = [self.newmap.tarelpoint], size = 7, 
                            pen = 'w', brush = 'r')    
            tar_tracktext = pg.TextItem(text = "%s" % self.newmap.target, color = 'r')
            self.p.addItem(tar_tracktext)       
            tar_tracktext.setPos(self.newmap.tarazpoint, self.newmap.tarelpoint)
            self.tarazlabel.setText("Target Az: %.2f" 
                               % (self.newmap.tarazpoint) + degree_sign)
            self.tarellabel.setText("Target El: %.2f" 
                               % (self.newmap.tarelpoint) + degree_sign)
            self.azofflabel.setText("<body style=\" font-size:8pt;\">""Az-El Offset: %.2f" 
                               % (self.newmap.azoff) + degree_sign + " %.2f" 
                               % (self.newmap.eloff) + degree_sign)
        
        #update the clicked source information     
        if not self.newmap.clickazpoint == '' and not self.newmap.clickelpoint == '':
            curve.addPoints(x = [self.newmap.clickazpoint], y = [self.newmap.clickelpoint], size = 7, 
                            pen = 'w', brush = 'y')
            tracktext = pg.TextItem(text = "%s" % self.newmap.clicksource, color = 'y')
            self.p.addItem(tracktext)
            tracktext.setPos(self.newmap.clickazpoint, self.newmap.clickelpoint)
            self.azlabel.setText("Clicked Az: %.2f" % self.newmap.clickazpoint + "%s" %degree_sign)
            self.ellabel.setText("Clicked El: %.2f" % self.newmap.clickelpoint + "%s" %degree_sign)
        else:
            self.azlabel.setText("Clicked Az: ")
            self.ellabel.setText("Clicked El: ")
            self.ralabel.setText("Clicked Ra: ")
            self.declabel.setText("Clicked Dec: ")

        
        #update the solar system body positions    
        if self.newmap.toggle_ephem:
            for i in range (len(self.newmap.ephem_azpoints)):
                curve.addPoints(x = [self.newmap.ephem_azpoints[i]], y = [self.newmap.ephem_elpoints[i]], 
                    size = 12, pen = None, brush = pg.mkBrush(color = (int(self.newmap.ephem_colors[i][0]),
                    int(self.newmap.ephem_colors[i][1]),int(self.newmap.ephem_colors[i][2]))), symbol = 'o')
            
        #check to see if user changed tracking settings
        if not self.newmap.toggletrack:
            self.trackbut.setText("Toggle Track: OFF")
        else:
            self.trackbut.setText("Toggle Track: ON  ")
            
        #updates the tracking line of the current source
        curve2 = pg.PlotCurveItem(x = self.newmap.clickazpoints, y = self.newmap.clickelpoints, 
                                  pen = pg.mkPen('y'))
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