#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 01:23:33 2018

@author: ahmed
Conjonction de la lune et des planètes
"""

# IMPORTOWANIE
from pylab import *
import ephem as ep
# OBSERVATEUR
obs = ep.Observer()
# TUNIS
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
obs.name= "SAT-TUNIS"
# NOUS CRÉONS UN OBJET
# on vérifie si c'est sous l'horizon
soleil = ep.Sun() 
lune = ep.Moon()
venus = ep.Venus()
mars = ep.Mars()
jupiter = ep.Jupiter()
# pas de temps - heure
dt = ep.hour
# temps initial
ts = ep.now()
# heure actuelle
tm = ts

# BOUCLE PRINCIPAL DU PROGRAMME
for i in range (365*24*2):
# nous fixons l'heure actuelle
    obs.date = tm
    # nous calculons des coordonnées
    soleil.compute(obs)
    lune.compute(obs)
    venus.compute(obs)
    mars.compute(obs)
    jupiter.compute(obs)
    # on calcule la séparation
    s1 = ep.separation(venus , lune)
    s2 = ep.separation(mars , lune)
    s3 = ep.separation(jupiter , lune)
    # la séparation doit être inférieure à 5 degrés
    if degrees(s1) < 5:
        # nous vérifions si la lune sera au-dessus de l'horizon
        # et si le soleil est au-dessous de l'horizon
        if degrees(lune.alt) > 5.0 and degrees(soleil.alt) < -5.0:
            print("-------------------------------------------------------------")
            print(u"précédente nouvelle lune , UT :", ep.previous_new_moon(ep.Date(tm)))
            print(u"Vénus - Lune , UT :", ep.Date(tm) ,"séparation :", s1)
            print(u"pos. Lune :", lune.az ,"El :", lune.alt)
            
    if degrees(s2) < 5:
        if degrees(lune.alt) > 5.0 and degrees(soleil.alt) < -5.0:
            print("------------------------------------------------------------------")
            print(u"précédente nouvelle lune , UT :", ep.previous_new_moon(ep.Date(tm)))
            print(u"Mars - Lune , UT :", ep.Date(tm) ,"séparation :", s2)
            print(u"Pos. Lune, Az :", lune.az ,"El :", lune.alt)
    if degrees(s3) < 5:
        if degrees(lune.alt) > 5.0 and degrees(soleil.alt) < -5.0:
            print("--------------------------------------------------------------")
            print(u"précédente nouvelle lune , UT :", ep.previous_new_moon(ep.Date(tm)))
            print(u"Jupiter - Lune , UT :", ep.Date(tm) ,"séparation :", s3)
            print(u"Pos. Lune, Az :", lune.az ,"El :", lune.alt)
        # on augmente le temps d'une heure
    tm += dt