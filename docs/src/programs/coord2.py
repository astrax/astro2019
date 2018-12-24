#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 19:37:06 2018

@author: ahmed
"""
from pylab import *
import ephem as ep

# OBSERVATEUR
obs = ep.city("Paris")
print("longitude : ", obs.lon)
print ("latitude : ", obs.lat)

# PROPRE DATE ET HEURE TU
obs.date = "2019/01/13 10:00:00"
