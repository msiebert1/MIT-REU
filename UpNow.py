# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:07:25 2015

@author: Matt Siebert
"""
from sourcemap import SourceMap
import pyqtgraph as pg
import datetime
from pyqtgraph.Qt import QtGui, QtCore
import sys

class UpNow():
    """An instance displays source trajectories in the sky over the period of 
    the current day. The plots are designed to give the user an idea of what 
    sources are up when. The curves are flat when the source is below the horizon.
    A green curve indicates a source that is currently above the horizon and a
    red curve indicates a source that is currently below the horizon. This class
    relies on functions from the sourcemap application.
    """
    
    def __init__(self, newmap):
        """Constructor sets up the gui and allocates fields to contain source
        names, elevation, time, and upnow information. Then plots the source
        trajecories.
        """
        
        #source data fields
        self.newmap = newmap
        self.allnames = []
        self.allels = []
        self.alltimes = []
        self.upnow = []
        
        self.acquire_source_data()
        
        #main window (scroll area)
        self.sa = pg.QtGui.QScrollArea() 
        self.sa.setWindowTitle("UpNow Plots")
        self.sa.setWindowIcon(QtGui.QIcon('/home/msiebert/Documents/MIT_REU/37m_GUI/Haystack_Icon.gif'))
        self.sa.resize(655,350)                                                                                                                             
        self.w = pg.GraphicsLayoutWidget()                                                                                                                      
        self.w.setFixedHeight(len(self.allnames)*174)
        self.sa.setWidget(self.w)
        
        #plot trajectories
        self.plot_sources()
        
        self.sa.show()
        
    def acquire_source_data(self):
        """Populates the fields, allels, and alltimes with nested lists. Each 
        list contains lists of el data or time data that correspond to a 
        specific source. El and time data for each source will eventually be 
        plotted. The names and upnow info for each source are also stored in lists.
        """
        
        def my_range(start, end, step):
            while start <= end:
                yield start
                start += step
        
        #iterate through sources (ignore ephemerides)                
        for source in newmap.allsources[:-10]:
            els = []
            times = []
            now = datetime.datetime.utcnow()
            
            #start time at the beginning of the current day
            newmap.time = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
            newmap.set_time(newmap.time)
            
            #get coordinates of the source for different times in the day
            #if elevation is below 0, a 0 is appended instead so curve is flat when 
            #the source is below the horizon
            for i in my_range(0,24,.1):       
                name, az, el = newmap.get_source_coords(source)
                if el >= 0:
                    els.append(el)
                    times.append(newmap.uthrs)
                else:
                    els.append(0)
                    times.append(newmap.uthrs)
                newmap.time = newmap.time + datetime.timedelta(seconds = 360) 
                newmap.set_time(newmap.time)
            
            #store trajectory info in nested lists
            self.allels.append(els)
            self.alltimes.append(times)
            
            #store corresponding source name info
            self.allnames.append(source.split()[0])
            newmap.time = datetime.datetime.utcnow()
            newmap.set_time(newmap.time)
            
            #determine whether or not source is up now and store that info
            if newmap.get_source_coords(source)[2] > 0:
                self.upnow.append(True)
            else:
                self.upnow.append(False)
                
    def plot_sources(self):
        """Plots elevation vs time for all sources in the sourcelist. Curve is 
        green if source is upnow, red if it is below the horizon.
        """
        
        for i in range(len(self.alltimes)):
            p = self.w.addPlot(row=i, col=0, title = self.allnames[i])
            if self.upnow[i] == True:
                c = pg.PlotCurveItem(x = self.alltimes[i], y = self.allels[i], pen = 'g')
            else:
                c = pg.PlotCurveItem(x = self.alltimes[i], y = self.allels[i], pen = 'r')
            p.addItem(c)
            p.setYRange(0, 90)
            p.setXRange(0, 24)
            p.getViewBox().setLimits(xMin = 0, xMax = 24, minXRange = 24)
            p.setLabels(bottom = "UT", left = "Elevation")
        
if __name__ == '__main__':
    app = app = QtGui.QApplication([]) 

    fileChoice = QtGui.QFileDialog.getOpenFileName(filter = "*.lst") 
    
    if not fileChoice == '':
        newmap = SourceMap(fileChoice)
        newmap.paused = True
        now  = datetime.datetime.now()
        newmap.time = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        newmap.map_livetime()
        un = UpNow(newmap)
        
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()                                                                                                                           

