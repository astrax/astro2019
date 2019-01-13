#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 13:55:58 2017

@author: ahmed
"""

# IMPORTATION
from pylab import *
import ephem as ep
# OBSERVATEUR
obs = ep.Observer()
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
obs.name = "SAT-TUNIS"
# OBJETS
soleil = ep.Sun()
lune = ep.Moon()
# pas de temps - heure
dt = ep.hour
# temps initial
#ts = ep.now()
ts=ep.Date("2019-01-01 00:00:00")
# heure actuelle
tm = ts

for i in range (365*24*10):
    # nous fixons l'heure actuelle
    obs.date = tm
    # nous calculons les coordonnées
    soleil.compute(obs)
    lune.compute(obs)
    # rayons
    rs = soleil.radius
    rl = lune.radius
    # on calcule la distance angulaire
    sp = ep.separation(soleil, lune)
    # on vérifie si la somme des rayons sera inférieure
    # à la séparation calculée
    if sp < rs + rl :
    # nous vérifions si le soleil sera au-dessus de l'horizon
        if soleil.alt > 0.0:
            print ("Date de l'eclipse UT: " , ep.Date(tm) , "Separation: " , sp)
    # on augmente le temps par pas d'une heure
    tm += dt
