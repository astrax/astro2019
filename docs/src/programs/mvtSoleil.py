#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 19:53:30 2018

@author: ahmed
"""
# IMPORTATION
from pylab import *
import ephem as ep
# OBSERVATEUR
obs = ep.Observer()
# TUNIS
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
obs.name= "SAT-TUNIS"
# OBJET
soleil = ep.Sun()
# TEMPS
tm = linspace(0 , 24 , 25)
# POLOGNE PAYS POLONAIS
plt = subplot(111 , polar= True )

# FEUILLE PRINCIPALE
for t in tm :
    # changement de temps
    obs.date = "2019/06/21 %02d:00:00 "%t
    # on calcule les coordonnées
    soleil.compute(obs)
    # coordonnées azimutales - azimut en radians
    az = float(repr(soleil.az))
    el = degrees(float(repr(soleil.alt)))
    # graphique - on change l'élévation par une distance zénithale
    plt.plot([az], [90 - el], ls ="", marker= "o", c ="yellow", \
    markersize =10, label = "été")
    # heure locale UTC +2 heures en été
    if el > 0:
        plt.text (az, 90 - el, "%02d"%(t+2), fontsize =10, \
        ha = 'left' , va = 'center')
    # TRANSFERT HIVERNAL - nous répétons les calculs "en décembre"
    obs.date = "2019/12/22 %02d:00:00" % t
    soleil.compute(obs)
    az = float(repr(soleil.az))
    el = degrees(float(repr(soleil.alt)))
    plt.plot([az], [90 - el], ls ="", marker= "o", c ="blue", \
             markersize =10, label = "hiver")
    # heure locale UTC +1 heures en hiver
    if el > 0:
        plt.text (az, 90 - el, "%02d"%(t+1), fontsize =10, \
        ha = 'left' , va = 'center')
        
#nous limitons la distance zénithale à 90 degrés - horizon
plt.set_rmax(90.0)
# nous plaçons le nord en haut du graphique
plt.set_theta_zero_location("N")
title("Mouvement apparent du Soleil à " + obs.name)

savefig("../figs/mvtSoleil.pdf"); savefig("../figs/mvtSoleil.png")
show()