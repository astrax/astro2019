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
# OBSERWATOR
obs = ep.city("Warsaw")
# TWORZYMY OBIEKTY
soleil = ep.Sun() # sprawdzamy czy jest pod horyzontem
lune = ep.Moon()
venus = ep.Venus()
mars = ep.Mars()
jupiter = ep.Jupiter()
# krok czasowy - godzina
dt = ep.hour
# czas pocz ą tkowy
ts = ep.now()
# czas aktualny
tm = ts

# G Ł Ó WNA P Ę TLA PROGRAMU
for i in range (365*24*1):
# ustawiamy aktualny czas
    obs.date = tm
    # obliczamy wsp ó ł rz ę dne
    soleil.compute(obs)
    lune.compute(obs)
    venus.compute(obs)
    mars.compute(obs)
    jupiter.compute(obs)
    # obliczamy separacj ę
    s1 = ep.separation(venus , lune)
    s2 = ep.separation(mars , lune)
    s3 = ep.separation(jupiter , lune)
    # separacja ma byc mniejsza jak 5 stopni
    if degrees(s1) < 5:
        # sprawdzamy czy Ksi ę ż yc b ę dzie nad
        # horyzontem a S ł o ń ce pod horyzontem
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
        # zwi ę kszamy czas o godzin ę
    tm += dt