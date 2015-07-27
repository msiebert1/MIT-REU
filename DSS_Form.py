# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:18:03 2015

@author: msiebert
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import glob
import os 
import sys

class DSS_Form():
    """An instance sets up the basic gui layout for the discrete source scan 
    application.
    """
    
    def __init__(self, newplot, newestData):
        """Creates and lays out the widgets to be used in the gui. The contents
        of many of the widgets are changed as the application is running.
        """
        
        self.newplot = newplot
        self.newestData = newestData
        
        #main window      
        self.win = QtGui.QWidget()
        self.win.setWindowTitle('DSS Plot: %s' % self.newestData)
        self.win.setWindowIcon(QtGui.QIcon('/home/msiebert/Documents/MIT_REU/37m_GUI/Haystack_Icon.gif'))
        self.win.resize(800,500)
        self.gridLayout = QtGui.QGridLayout(self.win)
        
        #main plots
        self.azplot = pg.PlotWidget(self.win)
        self.elplot = pg.PlotWidget(self.win)
        self.gridLayout.addWidget(self.azplot, 0, 1, 8, 6)
        self.gridLayout.addWidget(self.elplot, 10, 1, 8, 6)
        
        #scan information labels
        self.source = QtGui.QLabel(self.win)
        self.source.setText("<body style=\" font-size:10pt;\">""Source: %s" %self.newplot.lines[0].split()[1])
        self.gridLayout.addWidget(self.source, 0, 0, 1, 1)
        self.f = QtGui.QLabel(self.win)
        self.f.setText("<body style=\" font-size:10pt;\">""Freq: %s" %self.newplot.lines[0].split()[2])
        self.gridLayout.addWidget(self.f, 1, 0, 1, 1)
        self.tsys = QtGui.QLabel(self.win)
        self.tsys.setText("<body style=\" font-size:10pt;\">""Tsys: %s" %self.newplot.lines[0].split()[3])
        self.gridLayout.addWidget(self.tsys, 2, 0, 1, 1)
        self.par = QtGui.QLabel(self.win)
        self.par.setText("<body style=\" font-size:10pt;\">""Parallactic Angle: %s" %self.newplot.lines[0].split()[4])
        self.gridLayout.addWidget(self.par, 3, 0, 1, 1)
        self.az = QtGui.QLabel(self.win)
        self.az.setText("<body style=\" font-size:10pt;\">""Az: %s" %self.newplot.lines[0].split()[5])
        self.gridLayout.addWidget(self.az, 4, 0, 1, 1)
        self.el = QtGui.QLabel(self.win)
        self.el.setText("<body style=\" font-size:10pt;\">""El: %s" %self.newplot.lines[0].split()[6])
        self.gridLayout.addWidget(self.el, 5, 0, 1, 1)
        self.ra = QtGui.QLabel(self.win)
        self.ra.setText("<body style=\" font-size:10pt;\">""Ra: %s" %self.newplot.lines[0].split()[7])
        self.gridLayout.addWidget(self.ra, 6, 0, 1, 1)
        self.dec = QtGui.QLabel(self.win)
        self.dec.setText("<body style=\" font-size:10pt;\">""Dec: %s" %self.newplot.lines[0].split()[8])
        self.gridLayout.addWidget(self.dec, 7, 0, 1, 1)
        self.usr = QtGui.QLabel(self.win)
        self.usr.setText("<body style=\" font-size:10pt;\">""Usroff: %s" %self.newplot.lines[0].split()[9])
        self.gridLayout.addWidget(self.usr, 10, 0, 1, 1)
        self.z = QtGui.QLabel(self.win)
        self.z.setText("<body style=\" font-size:10pt;\">""0.0: %s" %self.newplot.lines[0].split()[10])
        self.gridLayout.addWidget(self.z, 11, 0, 1, 1)
        self.eloff = QtGui.QLabel(self.win)
        self.eloff.setText("<body style=\" font-size:10pt;\">""Eloff: %s" %self.newplot.lines[0].split()[11])
        self.gridLayout.addWidget(self.eloff, 12, 0, 1, 1)
        
        #az scan gaussian fit labels
        self.fit = QtGui.QLabel(self.win)
        self.fit.setText("<body style=\" font-size:10pt;\">""Fit Quality: " )
        self.gridLayout.addWidget(self.fit, 0, 7, 1, 1)
        self.base = QtGui.QLabel(self.win)
        self.base.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.gridLayout.addWidget(self.base, 1, 7, 1, 1)
        self.off = QtGui.QLabel(self.win)
        self.off.setText("<body style=\" font-size:10pt;\">""Offset: ")
        self.gridLayout.addWidget(self.off, 2, 7, 1, 1)
        self.slop = QtGui.QLabel(self.win)
        self.slop.setText("<body style=\" font-size:10pt;\">""Slope: ")
        self.gridLayout.addWidget(self.slop, 3, 7, 1, 1)
        self.gauss = QtGui.QLabel(self.win)
        self.gauss.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.gridLayout.addWidget(self.gauss, 4, 7, 1, 1)
        self.ampl = QtGui.QLabel(self.win)
        self.ampl.setText("<body style=\" font-size:10pt;\">""Amplitude: ")
        self.gridLayout.addWidget(self.ampl, 5, 7, 1, 1)
        self.posi = QtGui.QLabel(self.win)
        self.posi.setText("<body style=\" font-size:10pt;\">""Position: ")
        self.gridLayout.addWidget(self.posi, 6, 7, 1, 1)
        self.wid = QtGui.QLabel(self.win)
        self.wid.setText("<body style=\" font-size:10pt;\">""Width: ")
        self.gridLayout.addWidget(self.wid, 7, 7, 1, 1)
        
        #el scan gaussian fit labels
        self.fit2 = QtGui.QLabel(self.win)
        self.fit2.setText("<body style=\" font-size:10pt;\">""Fit Quality: " )
        self.gridLayout.addWidget(self.fit2, 10, 7, 1, 1)
        self.base2 = QtGui.QLabel(self.win)
        self.base2.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.gridLayout.addWidget(self.base2, 11, 7, 1, 1)
        self.off2 = QtGui.QLabel(self.win)
        self.off2.setText("<body style=\" font-size:10pt;\">""Offset: ")
        self.gridLayout.addWidget(self.off2, 12, 7, 1, 1)
        self.slop2 = QtGui.QLabel(self.win)
        self.slop2.setText("<body style=\" font-size:10pt;\">""Slope: ")
        self.gridLayout.addWidget(self.slop2, 13, 7, 1, 1)
        self.gauss2 = QtGui.QLabel(self.win)
        self.gauss2.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.gridLayout.addWidget(self.gauss2, 14, 7, 1, 1)
        self.ampl2 = QtGui.QLabel(self.win)
        self.ampl2.setText("<body style=\" font-size:10pt;\">""Amplitude: ")
        self.gridLayout.addWidget(self.ampl2, 15, 7, 1, 1)
        self.posi2 = QtGui.QLabel(self.win)
        self.posi2.setText("<body style=\" font-size:10pt;\">""Position: ")
        self.gridLayout.addWidget(self.posi2, 16, 7, 1, 1)
        self.wid2 = QtGui.QLabel(self.win)
        self.wid2.setText("<body style=\" font-size:10pt;\">""Width: %f" )
        self.gridLayout.addWidget(self.wid2, 17, 7, 1, 1)
        
        #button to plot specific DSS
        self.choosebut = QtGui.QPushButton(self.win)
        self.choosebut.setText("Choose a DSS")
        self.gridLayout.addWidget(self.choosebut, 13, 0, 1, 1)
        self.choosebut.clicked.connect(self.plot_dss)
        
        #button to plot latest DSS 
        self.live = QtGui.QPushButton(self.win)
        self.live.setText("Plot Live DSS")
        self.gridLayout.addWidget(self.live, 14, 0, 1, 1)
        self.live.clicked.connect(self.latest_live_dss)
            
        #set titles and axis labels of the plots
        self.azplot.setTitle("Azimuth Cut")
        self.azplot.setLabels(left = "Temp", bottom = "Azimuth Offset")
        self.elplot.setTitle("Elevation Cut")
        self.elplot.setLabels(left = "Temp", bottom = "Elevation Offset")
        
    def update_labels(self):
        """Updates the scan information to be displayed on the left side of the 
        gui. This is useful after the user has changed the scan file.
        """
        
        self.source.setText("<body style=\" font-size:10pt;\">""Source: %s" %self.newplot.lines[0].split()[1])
        self.f.setText("<body style=\" font-size:10pt;\">""Freq: %s" %self.newplot.lines[0].split()[2])
        self.tsys.setText("<body style=\" font-size:10pt;\">""Tsys: %s" %self.newplot.lines[0].split()[3])
        self.par.setText("<body style=\" font-size:10pt;\">""Parallactic Angle: %s" %self.newplot.lines[0].split()[4])
        self.az.setText("<body style=\" font-size:10pt;\">""Az: %s" %self.newplot.lines[0].split()[5])
        self.el.setText("<body style=\" font-size:10pt;\">""El: %s" %self.newplot.lines[0].split()[6])
        self.ra.setText("<body style=\" font-size:10pt;\">""Ra: %s" %self.newplot.lines[0].split()[7])
        self.dec.setText("<body style=\" font-size:10pt;\">""Dec: %s" %self.newplot.lines[0].split()[8])
        self.usr.setText("<body style=\" font-size:10pt;\">""Usroff: %s" %self.newplot.lines[0].split()[9])
        self.z.setText("<body style=\" font-size:10pt;\">""0.0: %s" %self.newplot.lines[0].split()[10])
        self.eloff.setText("<body style=\" font-size:10pt;\">""Eloff: %s" %self.newplot.lines[0].split()[11])
    
    def update_fits(self, offset, slope, amp, pos, width, rating,
                    offset2, slope2, amp2, pos2, width2, rating2):
        """Updates the fit information to be displayed on the right side of the
        gui. This is useful after the user has changed the scan file or after a
        liveplot has finished.
        """
        
        colormap = {"GOOD": "green", "SO-SO": "yellow", "REJECT": "red"}
        s = "<body style=\" color: %s;font-size:10pt;\">" %(colormap[rating])
        s2 = "<body style=\" color: %s;font-size:10pt;\">" %(colormap[rating2])
        
        self.fit.setText(s+"Fit Quality: %s" %rating)
        self.base.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.off.setText("<body style=\" font-size:10pt;\">""Offset: %f" % offset)
        self.slop.setText("<body style=\" font-size:10pt;\">""Slope: %f" % slope)
        self.gauss.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.ampl.setText("<body style=\" font-size:10pt;\">""Amplitude: %f" % amp)
        self.posi.setText("<body style=\" font-size:10pt;\">""Position: %f" % pos)
        self.wid.setText("<body style=\" font-size:10pt;\">""Width: %f" % width)
        
        self.fit2.setText(s2+"Fit Quality: %s" %rating2)
        self.base2.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.off2.setText("<body style=\" font-size:10pt;\">""Offset: %f" % offset2)
        self.slop2.setText("<body style=\" font-size:10pt;\">""Slope: %f" % slope2)
        self.gauss2.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.ampl2.setText("<body style=\" font-size:10pt;\">""Amplitude: %f" % amp2)
        self.posi2.setText("<body style=\" font-size:10pt;\">""Position: %f" % pos2)
        self.wid2.setText("<body style=\" font-size:10pt;\">""Width: %f" % width2)    
        
    def clear_fits(self):
        """Clears the information in the fit labels. Fit labels must be 
        cleared when a liveplot starts so that no fit data is displayed while 
        a scan is currently running.
        """
        
        self.fit.setText("<body style=\" font-size:10pt;\">""Fit Quality: ")
        self.base.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.off.setText("<body style=\" font-size:10pt;\">""Offset: ")
        self.slop.setText("<body style=\" font-size:10pt;\">""Slope: ")
        self.gauss.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.ampl.setText("<body style=\" font-size:10pt;\">""Amplitude: ")
        self.posi.setText("<body style=\" font-size:10pt;\">""Position: ")
        self.wid.setText("<body style=\" font-size:10pt;\">""Width: ")
        
        self.fit2.setText("<body style=\" font-size:10pt;\">""Fit Quality: ")
        self.base2.setText("<body style=\" color: red;font-size:10pt;\">""Baseline:")
        self.off2.setText("<body style=\" font-size:10pt;\">""Offset: ")
        self.slop2.setText("<body style=\" font-size:10pt;\">""Slope: ")
        self.gauss2.setText("<body style=\" color: red;font-size:10pt;\">""Gaussian:")
        self.ampl2.setText("<body style=\" font-size:10pt;\">""Amplitude: ")
        self.posi2.setText("<body style=\" font-size:10pt;\">""Position: ")
        self.wid2.setText("<body style=\" font-size:10pt;\">""Width: ")  
            
    def plot_dss(self):
        """Plots a specific discrete source scan chosen by the user."""
        
        #prompt user for file
        fileChoice = QtGui.QFileDialog.getOpenFileName() 
        if fileChoice == '':
            sys.exit()
        
        #clear any existing scan data
        self.newplot.clear_data()
        
        #if user chose an invalid file clear the plots and change title of main window
        try:
            self.newplot.create_rawdata(fileChoice)   
        except IndexError:
            self.win.setWindowTitle("Choose a Completed Scan")
            self.azplot.clear()
            self.elplot.clear()
            return
        
        #acquire fit data and update all labels
        self.win.setWindowTitle('DSS Plot: %s' % fileChoice)
        ax, ay, aoffset, aslope, aamp, apos, awidth, arating = self.newplot.gaussianfit_az()
        ax2, ay2, aoffset2, aslope2, aamp2, apos2, awidth2, arating2 = self.newplot.gaussianfit_el()
        self.update_labels()
        self.update_fits(aoffset, aslope, aamp, apos, awidth, arating,
                         aoffset2, aslope2, aamp2, apos2, awidth2, arating2)
                  
        #clear existing plots and plot the chosen scan data
        self.azplot.clear()
        self.elplot.clear()
        curve1 = pg.PlotCurveItem(x = self.newplot.azoff_az, 
                                  y = self.newplot.tempch1_az, pen = (142, 255, 255))
        self.azplot.addItem(curve1)
    
        curve2 = pg.PlotCurveItem(x = self.newplot.eloff_el, 
                                  y = self.newplot.tempch1_el, pen = (142, 255, 255))
        self.elplot.addItem(curve2)
    
        curve3 = pg.PlotCurveItem(x = ax, y = ay, pen = 'r')
        self.azplot.addItem(curve3)
    
        curve4 = pg.PlotCurveItem(x = ax2, y = ay2, pen = 'r')
        self.elplot.addItem(curve4)
        
    def latest_live_dss(self):
        """Plots the latest discrete source scan in livetime. If the scan has 
        completed, this completes the plot and displays the fit data.
        """
        
        #find the most recent DSS scan
        self.newplot.livefile = '%s' % max(glob.glob('/tcu/contnm/*'), key=os.path.getctime)
#        self.newplot.livefile = '%s' % max(glob.glob('*.dss'), key=os.path.getctime)
        #set title, update scan info, clear existing plots
        self.win.setWindowTitle('Latest DSS Plot: %s' % self.newplot.livefile)
        self.newplot.clear_data()
        self.update_labels()
        self.clear_fits()
        
        #plots the available DSS data
        #plots the fits and updates the fit data when scan finishes
        def update():
            self.newplot.animate()
            self.azplot.clear()
            self.elplot.clear()
            curve1 = pg.PlotCurveItem(x = self.newplot.azoff_az, 
                                      y = self.newplot.tempch1_az, pen = (142, 255, 255))
            self.azplot.addItem(curve1)
        
            curve2 = pg.PlotCurveItem(x = self.newplot.eloff_el, 
                                      y = self.newplot.tempch1_el, pen = (142, 255, 255))
            self.elplot.addItem(curve2)
            
            if self.newplot.scan_complete:
                ax, ay, aoffset, aslope, aamp, apos, awidth, arating = self.newplot.gaussianfit_az()
                ax2, ay2, aoffset2, aslope2, aamp2, apos2, awidth2, arating2 = self.newplot.gaussianfit_el()
                self.update_fits(aoffset, aslope, aamp, apos, awidth, arating,
                                 aoffset2, aslope2, aamp2, apos2, awidth2, arating2)
                curve3 = pg.PlotCurveItem(x = ax, y = ay, pen = 'r')
                self.azplot.addItem(curve3)
            
                curve4 = pg.PlotCurveItem(x = ax2, y = ay2, pen = 'r')
                self.elplot.addItem(curve4)
                timer.stop()
    
        #connect timer so plot continuously updates   
        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(0)