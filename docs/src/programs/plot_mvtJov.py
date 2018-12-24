#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 22:06:24 2018

@author: ahmed
"""
# IMPORTATION
from pylab import *
import ephem as ep
# NOUS CRÉONS UN OBJET
Io = ep.Io()
Eu = ep.Europa()
Ga = ep.Ganymede()
Ca = ep.Callisto()
# Créons des tableaux vide pour
# SAUVEGARDER LES COORDONNEES 
y = [] # wsp ó lna wsp . y
xIo = [] # wsp ó ł rz ę dna x dla
xEu = [] # ka ż dego ksi ę ż yca
xGa = [] # osobno
xCa = []