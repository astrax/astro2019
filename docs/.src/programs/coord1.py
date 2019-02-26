#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 23:39:39 2018

@author: ahmed
"""

from pylab import *
import ephem as ep
obs = ep.Observer()
obs.lon = "18.56406"
obs.lat = "53.09546" 
obs.elevation = 133.61

# Objet
lune = ep.Moon()

lune.compute(obs)

# coordonnées calculées
print("Position actuelle de la Lune")
print(" ------------------------------ ")
# nous affichons l'ascension droite et la déclinaison
print("RA : ", lune.ra)
print("Dec : ", lune.dec)
# nous affichons l'azimut et l'élévation
print("--------------------------------")
print("Az : ", lune.az)
print ("El : " , lune.alt)

# coordonnées azimutales en degrés sous forme d'un nombre réel
print(" -------------------------------- ")
print("Az (deg): ", degrees(lune.az))
print("El (deg): ", degrees(lune.alt))

