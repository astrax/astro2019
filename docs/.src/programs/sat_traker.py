#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 16:40:37 2018

@author: ahmed
GPS sattelite tracking in Python using pyEphem
source: file:///media/ahmed/MYLINUXLIVE/PyEphem/New%20folder/GPS%20sattelite%20tracking%20in%20Python%20using%20pyEphem%20%E2%80%93%20The%20Telegraphic.html

"""

import numpy as np
import pylab as plt
import ephem
import datetime

# Setup lat long of telescope
oxford = ephem.Observer()
oxford.lat = np.deg2rad(51.75)
oxford.long = np.deg2rad(-1.259)
oxford.date = datetime.datetime.now()
print(oxford.date)
# Load Satellite TLE data.
# from: http://www.celestrak.com/NORAD/elements/
l1 = 'GPS BIIA-23 (PRN 18)'
l2 = '1 22877U 93068A   18361.51036958 -.00000055  00000-0  00000+0 0  9998'
l3 = '2 22877  54.5615  75.5776 0147427  78.2198 233.8890  2.00570904184420' 
biif1 = ephem.readtle(l1,l2,l3)

# Make some datetimes
midnight = datetime.datetime.replace(datetime.datetime.now(), hour=0)
dt  = [midnight + datetime.timedelta(minutes=20*x) for x in range(0, 24*3)]

# Compute satellite locations at each datetime
sat_alt, sat_az = [], []
for date in dt:
    oxford.date = date
    biif1.compute(oxford)
    sat_alt.append(np.rad2deg(biif1.alt))
    sat_az.append(np.rad2deg(biif1.az))
    
# Plot satellite tracks
plt.figure()
plt.subplot(211)
plt.plot(dt, sat_alt)
plt.ylabel("Altitude (deg)")
plt.xticks(rotation=25)
plt.subplot(212)
plt.plot(dt, sat_az)
plt.ylabel("Azimuth (deg)")
plt.xticks(rotation=25)
plt.show()

# Plot satellite track in polar coordinates
plt.figure()
plt.polar(np.deg2rad(sat_az), 90-np.array(sat_alt))
plt.ylim(0,90)
plt.show()