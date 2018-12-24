#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:14:48 2018

@author: ahmed
"""

# IMPORTATION
from pylab import *
import ephem as ep
# deux fonctions supplémentaires du module datetime sont nécessaires
from datetime import datetime , timedelta

# OBSERVATEUR
obs = ep.city("Warsaw")
# MARS
mr = ep.Mars()

for i in range (0 , 181):
    # nous changeons la date d'un jour pendant six mois
    dt = datetime (2014, 1, 1) + timedelta(i)
    ds = "%d/%02d/%02d"%(dt.year, dt.month, dt.day)
    print(" jour de l'année: ", i +1 , ds)
    # fixer la date de l'observateur et calculer les coordonnées
    obs.date = ds
    mr.compute(obs)
    ra = degrees(float(repr(mr.ra)))
    de = degrees(float(repr(mr.dec)))
    # on dessine des objets
    plot([ra], [de], c = "orange", marker = "o")
    # nous ajoutons une description de la date en moyenne tous les 10 jours
    if (dt.day % 10) == 0: text(ra, de, ds, fontsize =8)
# conversion RA donné en degrés
# sur les formats heure, minute et seconde
def RAd2hms (x, loc):
    h = x//15
    m = int(((x - h * 15.0) / 15.0) * 60.0)
    s = ((x - h *15 - m / 4.0) / 15.0) * 3600.0
    return "%02dh%02dm%02ds"%(h, m, s)
# changement de déclinaison donné en degrés
# le format du degré, minute, second arc
def DEd2dms (x , loc ):
    d = int(fabs(x))
    m = int((fabs(x) - d)*60)
    s = (fabs(x) - d - m /60.0)*3600.0
    if x <0: d = -1 * d
    return " %02dd%02dm%02ds"%(d, m, s)

# description du dessin
xlabel(r"$\alpha$")
gca().xaxis.set_major_formatter(FuncFormatter(RAd2hms))
ylabel(r"$\delta$")
gca().yaxis.set_major_formatter(FuncFormatter(DEd2dms))
title("Mouvement retrograde de Mars en 2014")

savefig("../figs/retrogradeMars.pdf"); savefig("../figs/retrogradeMars.png")
show()