# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:42:12 2015

@author: Matt Siebert
"""

import numpy as np
import datetime
from tail import tail
from novas import compat as novas
from novas.compat import eph_manager
from pyqtgraph.Qt import QtGui, QtCore
from GUI_Form import GUI_Form
import sys


class SourceMap():
    """An instance contains information needed in the mapping of various
    radio sources given by a sourcelist. Also includes methods and fields useful
    for the source map gui application.        
    """
    
    def __init__(self, afile):
        """Constructor reads the source list file and initilizes fields to contain
        coordinate data for the sources.
        
        Args: 
            afile (str): A path to the file containing the sourcelist to be 
                displayed
        """
        
        #read the file and acquire lines of data
        thefile = open(afile, 'r')
        self.datafile = thefile
        self.lines = self.datafile.readlines()
        for aline in self.lines:
            if aline.rstrip() == '':
                self.lines.remove(aline)
        
        #fields to contain coordinate data of all sources
        self.azpoints = []
        self.elpoints = []
        self.time = datetime.datetime.utcnow()
        
        #fields to contain coordinate data of clicked source
        self.toggletrack = False
        self.clicksource = ""
        self.clickazpoint = ''
        self.clickelpoint = ''
        self.clickazpoints = []
        self.clickelpoints = []
        self.clickra = ''
        self.clickdec = ''
        
        #fields to contain coordinate data of selected sources
        self.selectedsources = []   
        self.sel_azpoints = []
        self.sel_elpoints = []
        
        #fields to contain coordinate data of added sources
        self.added_sources = []
        self.add_azpoints = []
        self.add_elpoints = []
        
        #fields to contain coordinate data of solar system bodies
        self.toggle_ephem = True
        self.ephems = []
        self.ephem_azpoints = []
        self.ephem_elpoints = []
        self.ephem_colors = []
        
        #fields to contain coordinate data of the antenna and target source
        self.toggletrack_ant = False
        self.antazpoint = 181
        self.antazpoints = []
        self.antelpoints = []
        self.antelpoint = 45
        self.cmdazpoint = 0
        self.cmdelpoint = 0
        self.skdfile = ''
        self.skdline = 0
        self.wrappoint = 0
        self.azoff = 0
        self.eloff = 0
        self.usr_offs = ''
        self.azoffset_data = [0]
        self.eloffset_data = [0]
        self.striptime = [0]
        self.togglestrips = False
        
        self.azbias1 = ''
        self.azbias2 = ''
        self.elbias = '' 
        
        self.subdx = ''
        self.subdy = ''
        self.subdz = ''
        self.subdpx = ''
        self.subdpy = ''
        
        self.deltdt = ''
        self.dut1 = ''
        self.deltat = ''
        
        self.tdk = ''
        self.dewpt = ''
        self.rh = ''
        self.pmb = ''
        
        self.target = ''
        self.tarsource = ''
        self.tarra = ''
        self.tardec = ''
        self.tarazpoint = ''
        self.tarelpoint = ''
        self.onsource = ''
        
        #fields useful for gui application
        self.namelist = []
        self.allsources = []
        self.location = novas.OnSurface(latitude = 42.62322, 
                                        longitude = -71.488210, height = 56.241)
        self.speed = 1
        self.paused = False
        self.uthrs = 0
        self.jd_tt = ''
        self.LST = ''
        self.togglegrid = False
        self.equ_grid_constra = [[],[],[],[],[],[],[],[],[],[],[],[]]
        self.equ_grid_constdec = [[],[],[],[],[],[],[],[],[],[],[],[]]
        
    def map_livetime(self):
        """Acquires the current time and lines of the datafile that include 
        sources with their coordinates.        
        """
        
        self.acquire_allsources()
        jd_start, jd_end, number = eph_manager.ephem_open()
        self.update()
        
    def set_time(self, time):
        """Sets the three time parameters of the source map (univeral time in
        hours, julian date, and local sidereal time) appropriately given a
        datetime object.
        
        Args: 
            time (datetime.datetime): The time to be used in synchronizing
                all time parameters of the SourceMap.
        """
        
        ut = str(time)
        self.uthrs = ((float(ut.split()[1].split(":")[0]) + 
                      (float(ut.split()[1].split(":")[1]) + 
                      float(ut.split()[1].split(":")[2])/60)/60))
        self.jd_tt = novas.julian_date(time.year, time.month, time.day, self.uthrs)
        
        gst = novas.sidereal_time(int(self.jd_tt), self.jd_tt%1, 68)
        self.LST = gst - 71.488210/15
        if self.LST < 0:
            self.LST = 23.934444444 + self.LST
        
    def update(self):
        """ Updates the time of the SourceMap for the current map state 
        (paused, unpaused/live, unpaused/timelapse). Then updates the coordinates 
        of each source, the coordinates of the solar system bodies, the antenna 
        status, and the strip chart data according to this time.
        """
        
        self.azpoints = []
        self.elpoints = []
        self.sel_azpoints = []
        self.sel_elpoints = []
        self.add_azpoints = []
        self.add_elpoints = []
        self.ephem_azpoints = []
        self.ephem_elpoints = []
        
        #don't change time if application is paused
        if self.paused:
            self.time = self.time
        #use live time if timelapse speed is 0
        elif not self.paused and self.speed == 0:
            self.time = datetime.datetime.utcnow()
        #speed up time if timelapse speed is nonzero
        else:
            self.time = self.time + datetime.timedelta(0,10*self.speed)
        
        #calculate the julian date and lst
        self.set_time(self.time)
        
        #update solar system body coordinates if user has them turned on
        if self.toggle_ephem:
            self.update_ephem()        
        
        #update antenna status and strip charts
        self.update_antenna()
        if self.togglestrips:
            self.update_strips()
        
        #update all source coordinates given the updated time
        for source in self.allsources:
            if not source.split()[0] == self.clicksource and len(source.split()) < 10:
                self.azpoints.append(self.get_source_coords(source)[1])
                self.elpoints.append(self.get_source_coords(source)[2])
                
            elif source.split()[0] == self.clicksource:
                self.clicksource, self.clickazpoint, self.clickelpoint = \
                                  self.get_source_coords(source)
                if self.toggletrack:
                    self.clickazpoints.append(self.clickazpoint)
                    self.clickelpoints.append(self.clickelpoint)
            
            if len(source.split()) > 9 and self.toggle_ephem:
                self.ephem_azpoints.append(self.get_source_coords(source)[1])
                self.ephem_elpoints.append(self.get_source_coords(source)[2])
                self.ephem_colors.append(source.split()[-3:])
                
        for source in self.selectedsources:
            self.sel_azpoints.append(self.get_source_coords(source)[1])
            self.sel_elpoints.append(self.get_source_coords(source)[2])
        
        for source in self.added_sources:
            self.add_azpoints.append(self.get_source_coords(source)[1])
            self.add_elpoints.append(self.get_source_coords(source)[2])

        
    def get_source_coords(self, source):
        """Uses pynovas to convert from ra and dec (given in the source list) 
        to azimuth and elevation at Haystack. This is done for the current time 
        of the map.
        
        Args:
            source (str): A string in the format of a source in the sourcelist.
            
        Returns:
            name (str): name of the source with these coordinates
            
            az (float): azimuth (degrees) of source
            
            el (float): elevation (degrees) of source
        """
        
        name = source.split()[0]
        ra = source.split()[1] + " " + source.split()[2] + " " + source.split()[3]
        dec = source.split()[4] + " " + source.split()[5] + " " + source.split()[6]
        
        #acquire ra and dec of the source. There is a typo in the sourcelist
        if not ra.split()[2] == "01.37s":
            ra1, ra2, ra3 = (float(ra.split()[0]), 
                            float(ra.split()[1]), 
                            float(ra.split()[2]))
        else:
            ra1, ra2, ra3 = (float(ra.split()[0]), 
                             float(ra.split()[1]), 
                             float(ra.split()[2][0:5]))
        dec1, dec2, dec3 = (float(dec.split()[0]), 
                            float(dec.split()[1]), 
                            float(dec.split()[2]))
        rahrs = (ra1 + (ra2 + ra3/60)/60)
        if dec1 > 0:
            decdeg = dec1 + (dec2 + dec3/60)/60
        else:
            decdeg = dec1 - (dec2 + dec3/60)/60
        new_rahrs = rahrs
        new_decdeg = decdeg
        
        #calculate the true to date ra and dec
        rtodeg = np.pi/180
        if len(source.split()) < 10:
            years_since2000 = ((self.time.year - 2000) 
                               + float(self.time.month)/12 
                               + float(self.time.day  
                               + float(self.time.hour)/24)/self.year_days())
            #see Radio Astronomy by John D. Kraus pg. 2-25
            new_rahrs = (rahrs + (.000853944 + .000371081*np.sin(rahrs*15*rtodeg)
                                  *np.tan(decdeg*rtodeg))*years_since2000)%24
            new_decdeg = decdeg + .005566194*np.cos(rahrs*15*rtodeg)*years_since2000      
        
        #update fields used to display true to date ra and dec
        degree_sign= u'\N{DEGREE SIGN}'
        if source.split()[0] == self.clicksource:
            updated_source = self.to_source_format(new_rahrs, new_decdeg, source.split()[0])
            self.clickra = (updated_source.split()[1] + "h " + updated_source.split()[2] + 
                               "m " + "%.2f" %float(updated_source.split()[3]) + "s")
            self.clickdec = (updated_source.split()[4] + "%s " %degree_sign 
                             + updated_source.split()[5] 
                             + "' " + "%.2f" %float(updated_source.split()[6]) + "\"")
        
        if source.split()[0] == self.target:
            updatedtar_source = self.to_source_format(new_rahrs, new_decdeg, source.split()[0])
            self.tarsource = source
            self.tarra = (updatedtar_source.split()[1] + "h " + updatedtar_source.split()[2] + 
                         "m " + "%.2f" %float(updatedtar_source.split()[3]) + "s")
            self.tardec = (updatedtar_source.split()[4] + "%s " % degree_sign 
                           + updatedtar_source.split()[5]  
                           + "' " + "%.2f" %float(updatedtar_source.split()[6]) + "\"")
                             
        #find azimuth and elevation for a given ra and dec and haystack's location
        horiz, equ = novas.equ2hor(self.jd_tt, 68, 1, 0, self.location, 
                                   new_rahrs, new_decdeg, ref_option=0, accuracy=0)
        az = horiz[1]
        el = 90 - horiz[0]
        
        return name, az, el
    
    def year_days(self):
        """Calculates the number of days in the current year.
        
        Returns:
            int: 365 if not a leapyear, 366 if a leapyear
        """
        
        i = self.time.year
        if i%4 == 0:
            if i%100 == 0:
                if i%400 == 0:
                    yeardays = 366
                else:
                    yeardays =365
            else:
                yeardays = 366
        else:
            yeardays = 365
        return yeardays
        
    def get_source_coordsgrid(self, coords, time):
        """Converts equatorial coordinates to horizontal coordinates at a 
        specific time.
        
        Args:
            coords (tuple (float,float)): A ra (hours) and a dec (degrees) to be
                converted to az and el.
                
            time (datetime.datetime): Contains the specific datetime object 
                to be used in coordinate conversion.
                
        Returns:
            az (float): azimuth (degrees)
            
            el (float): elevation (degrees) 
            
        This is necessary when calculating the ra and dec gridlines
        because ra and dec values are systematically determined and supplied 
        in tuples (not specified by a sourcelist). 
        """
        
        rahrs = coords[0]
        decdeg = coords[1]
        
        # calculate the time parameters associated with the given time
        ut = str(time)
        uthrs = (float(ut.split()[1].split(":")[0]) + 
                (float(ut.split()[1].split(":")[1]) + 
                float(ut.split()[1].split(":")[2])/60)/60)
        ajd_tt = novas.julian_date(time.year, time.month, time.day, uthrs)
        
        #find azimuth and elevation for a given ra and dec and haystack's location
        horiz, equ = novas.equ2hor(ajd_tt, 65, 0, 0, self.location, 
                                   rahrs, decdeg, ref_option=0, accuracy=0)
        az = horiz[1]
        el = 90 - horiz[0]
        
        return az, el
        
    def update_ephem(self):
        """Using pynovas, updates the equatorial positions of the solar system 
        bodies given a time. Also asigns each solar system body a color, therefore, 
        after calling split(), the solar system body sources are always longer than 
        regular sources.
        """
        
        #the solar system bodies are the last 10 sources
        self.allsources = self.allsources[:-10]
        
        #create sources containing solar system body coordinate and color information
        #add them to a list of sources 
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[0])
        self.allsources.append(self.to_source_format(ra,dec,"Mercury") + " 255 120 0")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[1])
        self.allsources.append(self.to_source_format(ra,dec,"Venus") + " 255 211 155")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[2])
        self.allsources.append(self.to_source_format(ra,dec,"Mars") + " 255 0 0")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[3])
        self.allsources.append(self.to_source_format(ra,dec,"Jupiter") + " 160 82 45")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[4])
        self.allsources.append(self.to_source_format(ra,dec,"Saturn") + " 192 255 62")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[5])
        self.allsources.append(self.to_source_format(ra,dec,"Uranus") + " 142 255 255")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[6])
        self.allsources.append(self.to_source_format(ra,dec,"Neptune") + " 153 50 204")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[7])
        self.allsources.append(self.to_source_format(ra,dec,"Pluto") + " 0 0 204")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[8])
        self.allsources.append(self.to_source_format(ra,dec,"Sun") + " 255 255 0")
        
        ra, dec, dis = novas.astro_planet(self.jd_tt, self.ephems[9])
        self.allsources.append(self.to_source_format(ra,dec,"Moon") + " 205 201 201")
    
    def update_antenna(self):
        """Tails the end of a file that supplies various information regarding
        antenna status and the target source. Assigns these values to variables.
        This will eventually process a message instead of a file.
        """
        
        cmdfile = open('/tcu/rt/acu-cmd', 'r')
        cmdlines = tail(cmdfile, lines = 36)
        
        statfile = open('/tcu/rt/acu-status', 'r')
        antlines = tail(statfile, lines = 14)
        
        stat2file = open('/tcu/rt/status', 'r')
        stats = tail(stat2file, lines = 108)
        statlines = stats.split('\n')
        
        #target source
        if len (statlines[6]) == 3:
            self.target = statlines[6].split()[2]
        self.tarsource = ""
        
        #find the target in the source list and determine the ra and dec
        for source in self.allsources:
            if source.split()[0].lower() == self.target.lower():
                self.tarsource = source 
                             
        #reset target source to default if it was not in the source list
        if self.tarsource == "":
            self.target = ""
        #otherwise calculate the position on the map    
        else:       
            self.target, self.tarazpoint, self.tarelpoint = \
                                      self.get_source_coords(self.tarsource)
                                      
        self.cmdazpoint = float(cmdlines.split()[21])*(180/np.pi)

        if self.cmdazpoint < 0:
            self.cmdazpoint = 360 + self.cmdazpoint
                
        elif self.cmdazpoint > 360:
            self.cmdazpoint = self.cmdazpoint - 360
        
        self.cmdelpoint = float(cmdlines.split()[30])*(180/np.pi)
        
        self.antazpoint = float(antlines.split()[21])*(180/np.pi)
        if self.antazpoint < 0:
            self.antazpoint = 360 + self.antazpoint
        elif self.antazpoint > 360:
            self.antazpoint = self.antazpoint - 360
        
        self.antelpoint = float(antlines.split()[33])*(180/np.pi)
        
        if self.toggletrack_ant:
            self.antazpoints.append(self.antazpoint)
            self.antelpoints.append(self.antelpoint)
            
        self.skdfile = statlines[48].split()[2]
        self.skdline = statlines[49].split()[2]
        self.wrappoint = float(antlines.split()[21])
        
        #calculate the offsets in antenna position
        self.azoff = self.antazpoint - self.cmdazpoint
        self.eloff = self.antelpoint - self.cmdelpoint
        self.usr_offs = statlines[31].split()[3] + " " + statlines[31].split()[4]
        
        self.onsource = statlines[59].split()[2]
        
        #obtain various status information
        self.azbias1 = statlines[65].split()[2]
        self.azbias2 = statlines[66].split()[2]
        self.elbias = statlines[67].split()[2]
        
        self.subdx = statlines[76].split()[2]
        self.subdy = statlines[77].split()[2]
        self.subdz = statlines[78].split()[2]
        self.subdpx = statlines[79].split()[2]
        self.subdpy = statlines[80].split()[2]
        
        self.deltdt = statlines[61].split()[2]
        self.dut1 = statlines[62].split()[2]
        self.deltat = statlines[63].split()[2]
        
        self.tdk = statlines[71].split()[2] + " " + statlines[71].split()[3]
        self.dewpt = statlines[72].split()[2] + " " + statlines[72].split()[3]
        self.rh = statlines[73].split()[2] 
        self.pmb = statlines[74].split()[2] + " " + statlines[74].split()[3]

    def update_strips(self):
         """Called after update_antenna therefore it updates the strip chart 
         data with latest offset data.
         """
         
         self.azoffset_data.append(self.azoff)    
         self.eloffset_data.append(self.eloff) 
         self.striptime.append(self.striptime[-1] + 1)
#         self.striptime.append(self.LST)
        
    def choose_source(self, name):
        """Changes the source to be highlighted and updates the necessary fields.
        
        Args: 
            name (str): The name of the source to be highlighted.
        
        This method is only called when the user clicks on a source.
        """
        
        self.clicksource = name
        self.clickazpoint = 0.0
        self.clickelpoint = 0.0
        self.clickazpoints = []
        self.clickelpoints = []
        for source in self.allsources:
            if source.split()[0] == self.clicksource:
                self.clicksource, self.clickazpoint, self.clickelpoint = self.get_source_coords(source)
                self.clickazpoints.append(self.clickazpoint)
                self.clickelpoints.append(self.clickelpoint)
    
    def to_source_format(self, rahrs, decdeg, name):
        """Converts a name, a right ascension, and a declination into a string 
        with correct source formatting. 
        
        Args:
            rahrs (float): ra (hours)
            
            decdeg (float): dec (degrees)
            
            name (str): The name to be assigned to this source
            
        Returns:
            str: A string in the format of a source in the sourcelist
        
        This is useful for creating sources for ephemeride data, and updating
        equatorial coordinates for other sources.
        """
        
        #convert hours into dms
        ramin = (rahrs%1)*60
        rasec = (ramin%1)*60
        rahrs = int(rahrs)
        ramin = int(ramin)
        
        #convert degrees into dms
        decmin = (np.abs(decdeg)%1)*60
        decsec = (decmin%1)*60
        decdeg = int(decdeg)
        decmin = int(decmin)
        
        return ("%s  " %(name) + str(rahrs) + " " + str(ramin) + " " + str(rasec) + "  "
                + str(decdeg) + " " + str(decmin) + " " + str(decsec) + "  " + "2000  " + "0.0")
        
    def get_const_ragrid(self):
        """Constructs data for a grid with 12 constant right ascension values 
        to be overlayed and updated as time changes.
        
        Returns:
            ra_azpoints (nested list (float)): 12 lists of azimuth points, each list
                corresponding to a constant value of right ascension
                
            ra_elpoints (nested list (float)): 12 lists of elevation points, each list
                corresponding to a constant value of right ascension
        
        Each list in ra_azpoints will be plotted against the corresponding list
        in ra_elpoints. This will be called periodically so thatthe gridlines 
        reflect the current time of the map.
        """
        
        ra_azpoints = [[],[],[],[],[],[],[],[],[],[],[],[]]
        ra_elpoints = [[],[],[],[],[],[],[],[],[],[],[],[]]
                
        #convert these values to azimuth and elevation and add them to the nested list
        for k in range(0, len(self.equ_grid_constra)):    
            for source in self.equ_grid_constra[k]:
                ra_azpoints[k].append(self.get_source_coordsgrid(source, self.time)[0])
                ra_elpoints[k].append(self.get_source_coordsgrid(source, self.time)[1])

        return ra_azpoints, ra_elpoints
    
    def get_const_decgrid(self):
        """Constructs data for a grid with 12 constant declination values to be 
        overlayed. These do not change with time so they do not need to be 
        updated.
        
        Returns:
            dec_azpoints (nested list (float)): 12 lists of azimuth points, each list
                corresponding to a constant value of declination
                
            dec_elpoints (nested list (float)): 12 lists of elevation points, each list
                corresponding to a constant value of declination
        
        Each list in dec_azpoints will be plotted against the corresponding list
        in dec_elpoints.
        """
        
        dec_azpoints = [[],[],[],[],[],[],[],[],[],[],[],[]]
        dec_elpoints = [[],[],[],[],[],[],[],[],[],[],[],[]]
        
        now = datetime.datetime.now()
        atime = datetime.datetime(now.year, now.month, now.day, 12, 0, 0)

        #convert these values to azimuth and elevation and add them to the nested list
        for k in range(0,len(self.equ_grid_constdec)):
            for source in self.equ_grid_constdec[k]:
                dec_azpoints[k].append(self.get_source_coordsgrid(source, atime)[0])
                dec_elpoints[k].append(self.get_source_coordsgrid(source, atime)[1])
            
        temp = dec_azpoints[:]
        temp2 = dec_elpoints[:]
        redo = []
        redo2 = []
        
        #account for the fact that if azimuth changes from 0 to 360 or vice versa, 
        #the plotcurve will draw a line across the screen
        for k in range(0,len(temp)):
            for i in range(0, len(temp[k])-1):
                if temp[k][i] >300 and temp[k][i+1] < 50:
                    dec_azpoints[k] = dec_azpoints[k][:i+1]
                    dec_elpoints[k] = dec_elpoints[k][:i+1]
                    redo.append(temp[k][i+1:])
                    redo2.append(temp2[k][i+1:])
                if temp[k][i] < 50 and temp[k][i+1] > 300:
                    dec_azpoints[k] = dec_azpoints[k][:i+1]
                    dec_elpoints[k] = dec_elpoints[k][:i+1]
                    dec_azpoints.append(temp[k][i+1:])
                    dec_elpoints.append(temp2[k][i+1:])
                    
        for k in range(0, len(redo)):
            for i in range(0,len(redo[k])-1):
                if redo[k][i] < 50 and redo[k][i+1] > 300:
                    dec_azpoints.append(redo[k][:i+1])
                    dec_elpoints.append(redo2[k][:i+1])
                    dec_azpoints.append(redo[k][i+1:])
                    dec_elpoints.append(redo2[k][i+1:])

        return dec_azpoints, dec_elpoints
                    
                
    def acquire_allsources(self):
        """Iterates through source list and acquires all lines containing a 
        source with coordinates. Also adds on solar system bodies using the same format
        and creates lists of equatorial coordinates needed for grid calculation.        
        """
        
        for aline in self.lines:
            if self.is_dataline(aline):
                self.allsources.append(aline)
                self.namelist.append(aline.split()[0])
        
        #create a list of all solar system body objects
        self.ephems = [novas.make_object(0, 1, 'Mercury', None), novas.make_object(0, 2, 'Venus', None),
                       novas.make_object(0, 4, 'Mars', None), novas.make_object(0, 5, 'Jupiter', None),
                       novas.make_object(0, 6, 'Saturn', None), novas.make_object(0, 7, 'Uranus', None),
                       novas.make_object(0, 8, 'Neptune', None), novas.make_object(0, 9, 'Pluto', None),
                       novas.make_object(0, 10, 'Sun', None), novas.make_object(0, 11, 'Moon', None)]
        
        #add temorary solar system body sources to allsources               
        self.allsources.append("Mercury	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Venus	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Mars	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Jupiter	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Saturn	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Uranus	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Neptune	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Pluto	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Sun	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        self.allsources.append("Moon	     0 0 0.0  +0 0 0.0		  2000   0.0   0 0 0")
        
        def my_range(start, end, step):
            while start <= end:
                yield start
                start += step
        
        #create lists of fake source coordinates that can be used to find gridlines
        #for constant right ascension and declination
        for k in range(0, len(self.equ_grid_constra)):        
            for i in my_range(-90, 90, 1.5):
                self.equ_grid_constra[k].append([2*k, i])
                
        for k in range(0,len(self.equ_grid_constdec)):
            for i in my_range(0, 24, .025):
                self.equ_grid_constdec[k].append([i, -90 + k*15])
        
    def is_dataline(self, aline):
        """Determines whether a given line in a source list contains a source 
        and its coordinates.   
        
        Args:
            aline (str): a line from a sourcelist that may contain a source
                with coordinate information.
                
        Returns:
            bool: True if line contains a source, False if the line contains
                other information
        """
        
        if len(aline.split()) == 9 and aline.split()[7] == "2000":
            return True
        else:
            return False  
            
if __name__ == '__main__':
    
    #create an application            
    app = app = QtGui.QApplication([])
    app.setGraphicsSystem('raster') 
    fileChoice = QtGui.QFileDialog.getOpenFileName(filter = "*.lst") 
    
    if not fileChoice == '':    
        #create instance of SourceMap and collect coordinate data
        newmap = SourceMap(fileChoice)
        newmap.map_livetime()
        
        #setup the gui
        gui = GUI_Form(newmap)
        
        #connect timer so plot continuously updates   
        timer = QtCore.QTimer()
        timer.timeout.connect(gui.update)
        timer.start(0)
    
        #start Qt event loop unless running in interactive mode.
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()  