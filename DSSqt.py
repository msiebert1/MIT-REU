# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:21:05 2015

@author: Matt Siebert
"""
from scipy import exp
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from DSS_Form import DSS_Form
import sys
import os
import glob

class DSSqt():
    """An instance of a gui that contains plots of temperature vs azimuth
    and temperature vs elevation for their respective DSS scans.
    """
       
    def __init__(self):
        """Constructor calls the parent class constructor and initializes 
        fields that will contain the various lists of data. Also sets
        up both plots to be used in the window.
        """
        
        self.datafile = ''
        
        #initialize various fields needed in the creation of plots
        self.num_nondatalines = 0   
        self.datalines_az = []
        self.datalines_el = []
        self.scan_complete = False
        self.animating = False
        self.pointing = False
        
        #az scan data fields
        self.day_az = []
        self.time_az = []
        self.tempch1_az = []
        self.tempch2_az = []
        self.tempch3_az = []
        self.tempch4_az = []
        self.azoff_az = []
        self.eloff_az = []
        self.raoff_az = []
        self.decoff_az = []  
        
        #el scan data fields
        self.day_el = []
        self.time_el = []
        self.tempch1_el = []
        self.tempch2_el = []
        self.tempch3_el = []
        self.tempch4_el = []
        self.azoff_el = []
        self.eloff_el = []
        self.raoff_el = []
        self.decoff_el = []
        
    def create_rawdata(self, afile):
        """Given a file of a particular format, parses through
        the file and updates the datafields that are useful for plotting.
        
        Args:
            afile (str): a path to a file containing complete dss scan
        """        
        
        #initialize field to contain lines of data
        self.datafile = open(afile, 'r')
        self.lines = self.datafile.readlines()
        #determine index range that contain the az scan data (starts at index 2)
        self.endline_az = 2
        for aline in self.lines[2:]:
            if aline.split()[0] == "umbrla":
                break
            self.endline_az += 1
        
        #contains lines of az scan data
        self.datalines_az = self.lines[2:self.endline_az]
        
        #split up each line and append the data values to their respective fields
        for datum in self.datalines_az:
            if len(datum.split()) == 10:
                aday, atime, atempch1, atempch2, atempch3, atempch4, aazoff, \
                    aeloff, araoff, adecoff = datum.split()
                self.day_az.append(aday)
                self.time_az.append(atime)
                self.tempch1_az.append(float(atempch1))
                self.tempch2_az.append(float(atempch2))
                self.tempch3_az.append(float(atempch3))
                self.tempch4_az.append(float(atempch4))
                self.azoff_az.append(float(aazoff))
                self.eloff_az.append(float(aeloff))
                self.raoff_az.append(float(araoff))
                self.decoff_az.append(float(adecoff))
        
        #determine index range that contain the el scan data 
        self.endline_el  = self.endline_az + 6
        for aline in self.lines[self.endline_el:]:
            if aline.split()[0] == "umbrla":
                break
            self.endline_el += 1
        
        #contains lines of el scan data
        self.datalines_el = self.lines[self.endline_az + 6:self.endline_el]
        
        #split up each line and append the data values to their respective fields
        for datum in self.datalines_el:
            if len(datum.split()) == 10:
                aday, atime, atempch1, atempch2, atempch3, atempch4, aazoff, \
                    aeloff, araoff, adecoff = datum.split()
                self.day_el.append(aday)
                self.time_el.append(atime)
                self.tempch1_el.append(float(atempch1))
                self.tempch2_el.append(float(atempch2))
                self.tempch3_el.append(float(atempch3))
                self.tempch4_el.append(float(atempch4))
                self.azoff_el.append(float(aazoff))
                self.eloff_el.append(float(aeloff))
                self.raoff_el.append(float(araoff))
                self.decoff_el.append(float(adecoff))
    
    def animate(self):
        """Called continuously until az and el scans are complete. Finds the
        available raw data.
        """
        
        #read datafile lines and clears the data from the last animation call
        self.scan_complete = False
        self.lines = []
        thefile = open(self.datafile, 'r')
        self.lines = thefile.readlines()
        self.num_nondatalines = 0
        self.clear_data()
        
        #identify the current az scan and el scan datalines
        for aline in self.lines:
            if self.is_dataline(aline) and self.num_nondatalines <= 2:
                self.datalines_az.append(aline)
            elif not self.is_dataline(aline):
                self.num_nondatalines = self.num_nondatalines + 1
                if self.num_nondatalines == 14:
                    self.scan_complete = True
            elif self.is_dataline(aline) and self.num_nondatalines > 2:
                self.datalines_el.append(aline)

        #split up each line and append the data values to their respective fields
        for datum in self.datalines_az:
            if len(datum.split()) == 10:
                aday, atime, atempch1, atempch2, atempch3, atempch4, aazoff, \
                    aeloff, araoff, adecoff = datum.split()
                self.day_az.append(aday)
                self.time_az.append(atime)
                self.tempch1_az.append(float(atempch1))
                self.tempch2_az.append(float(atempch2))
                self.tempch3_az.append(float(atempch3))
                self.tempch4_az.append(float(atempch4))
                self.azoff_az.append(float(aazoff))
                self.eloff_az.append(float(aeloff))
                self.raoff_az.append(float(araoff))
                self.decoff_az.append(float(adecoff))
        
        #split up each line and append the data values to their respective fields
        for datum in self.datalines_el:
            if len(datum.split()) == 10:
                aday, atime, atempch1, atempch2, atempch3, atempch4, aazoff, \
                    aeloff, araoff, adecoff = datum.split()
                self.day_el.append(aday)
                self.time_el.append(atime)
                self.tempch1_el.append(float(atempch1))
                self.tempch2_el.append(float(atempch2))
                self.tempch3_el.append(float(atempch3))
                self.tempch4_el.append(float(atempch4))
                self.azoff_el.append(float(aazoff))
                self.eloff_el.append(float(aeloff))
                self.raoff_el.append(float(araoff))
                self.decoff_el.append(float(adecoff))
            
    def clear_data(self):
        """Clears the contents of each data field."""
        
        self.scan_complete = False
        #az scan data fields
        self.day_az = []
        self.time_az = []
        self.tempch1_az = []
        self.tempch2_az = []
        self.tempch3_az = []
        self.tempch4_az = []
        self.azoff_az = []
        self.eloff_az = []
        self.raoff_az = []
        self.decoff_az = []
        self.datalines_az = []
        
        #el scan data fields
        self.day_el = []
        self.time_el = []
        self.tempch1_el = []
        self.tempch2_el = []
        self.tempch3_el = []
        self.tempch4_el = []
        self.azoff_el = []
        self.eloff_el = []
        self.raoff_el = []
        self.decoff_el = []
        self.datalines_el = []
        
    def gaussianfit_az(self):
        """Uses parameters given by the data file to create a gaussian fit for 
        the az data.
        
        Returns:
            x (list (float)): x values of the gaussian fit
            
            y (list (float)): y values of the gaussian fit
            
            offset (float): offset of the baseline for the gaussian fit
            
            slope (float): slope of the baseline for the gaussian fit
            
            amp (float): amplitude of the gaussian fit
            
            pos (float): position of the gaussian fit
            
            width (float): width of the gaussian fit
            
            rating (str): rating of the gaussian fit (GOOD, SO-SO, REJECT)
        """
        
        #assign gaussian parameters
        offset, slope, amp, pos, width = map(float, self.lines[self.endline_az+3].split()[0:5])
        numrate, rating = self.lines[self.endline_az+3].split()[5:7]
            
        #given the x axis range, create a list of 100 evenly spaced x values
        lower = min(self.azoff_az)
        upper = max(self.azoff_az)
        step = (upper - lower)/100
        x = np.arange(lower, upper, step)
        
        #determine the corresponding y values using the gaussian parameters
        y = amp * exp(-(x - pos)**2 / width**2)
        
        #add the calculated baseline to the gaussian to account for noise
        baseline = offset + slope*x
        y = y + baseline
        
        return x, y, offset, slope, amp, pos, width, rating
        
    def gaussianfit_el(self):
        """Uses parameters given by the data file to create a gaussian fit for 
        the el data. 
        
        Returns:
            x (list (float)): x values of the gaussian fit
            
            y (list (float)): y values of the gaussian fit
            
            offset (float): offset of the baseline for the gaussian fit
            
            slope (float): slope of the baseline for the gaussian fit
            
            amp (float): amplitude of the gaussian fit
            
            pos (float): position of the gaussian fit
            
            width (float): width of the gaussian fit
            
            rating (str): rating of the gaussian fit (GOOD, SO-SO, REJECT)
        """
        
        #assign gaussian parameters
        offset, slope, amp, pos, width = map(float, self.lines[self.endline_el+3].split()[0:5])
        numrate, rating = self.lines[self.endline_el+3].split()[5:7]
            
        #given the x axis range, create a list of 100 evenly spaced x values
        lower = min(self.eloff_el)
        upper = max(self.eloff_el)
        step = (upper - lower)/100
        x = np.arange(lower, upper, step)
        
        #determine the corresponding y values using the gaussian parameters
        y = amp * exp(-(x - pos)**2 / width**2)
        
        #add the calculated baseline to the gaussian to account for noise
        baseline = offset + slope*x
        y = y + baseline
        
        return x, y, offset, slope, amp, pos, width, rating

    def is_dataline(self, aline):
        """Determines whether a given line in a datafile contains scan data.
        
        Args:
            aline (str): a line from the datafile that may contain scan data
            
        Returns:
            bool: True if the line contains scan data, False if the line contains
                other information.
        """
        
        #scan data will contain 10 separate data elements (this might be too general)
        if len(aline.split()) == 10:
            return True
        else:
            return False
            
if __name__ == '__main__':
    
    #create application, set up the plot data            
    app = app = QtGui.QApplication([])
    app.setGraphicsSystem('raster') 
    newplot = DSSqt()
    
    #layout the gui
    gui = DSS_Form(newplot)
    
    #plot the latest DSS in the gui
    gui.latest_live_dss()
    gui.win.show()
    
    #start Qt event loop unless running in interactive mode.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()        
    
    
    
    
    
    