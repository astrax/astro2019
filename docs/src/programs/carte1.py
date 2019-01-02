#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 01:50:20 2018

@author: ahmed
"""

from pylab import *
plt.style.use('Solarize_Light2')
import ephem as ep
from ephem import stars # KATALOG JASNYCH GWIAZD
# OBSERVATEUR
obs = ep.Observer()
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
obs.name = "Tunis"
# KOLORY PLANET
ko = ["yellow","grey","brown","cyan","red",
      "orange","orange","cyan","blue"]
# LISTA OBIEKT Ó W
ob = []
ob.append(ep.Sun())
ob.append(ep.Moon())
ob.append(ep.Mercury())
ob.append(ep.Venus())
ob.append(ep.Mars())
ob.append(ep.Jupiter())
ob.append(ep.Saturn())
ob.append(ep.Uranus())
ob.append(ep.Neptune())
plt.figure(figsize=(10, 6))
# DODAJEMY KATALOG JASNYCH GWIAZD
for x in stars.db.split("\n"):
    if x !="" : ob.append(ep.readdb(x))
# OBLICZANIE WSP Ó Ł RZ Ę DNYCH
for x in ob : x.compute(obs)
# G Ł Ó WNA P Ę TLA PROGRAMU
i = 0
for x in ob :
    # obliczamy wsp.azymutalne
    az = degrees(x.az)
    el = degrees(x.alt)
    # kolory dla planet
    if i <= 8:
        plot([az] , [el] , markersize = int(- x.mag +9) ,
        ls ="" , marker ="o",
        color = ko [i] , label = x.name)
        
    else :
        plot([az] , [el] , markersize = int(-x.mag +5) , ls ="",
             marker ="o")
        print(x.mag)
        # opisy obiekt ó w
        text(az , el , x.name , fontsize =8)
    i += 1


# szary cie ń pod horyzontem
xd = [0 , 360]
y1 = [-90 , -90]
y2 = [0 , 0]
fill_between(xd , y1 , y2 , color ="black",
             facecolor ="grey", alpha =0.25)
# opis rysunku
xlabel("azymut")
ylabel("elewacja")
title("%s , %s - carte du ciel"%(obs.name , ep.now()))
legend(loc='upper center', bbox_to_anchor=(1.1, 0.7),
          fancybox=True, shadow=True, ncol=1)
xlim(0 , 360)
ylim(-90 , 90)
grid()
tight_layout()
savefig("../figs/carte1.pdf"); savefig("../figs/carte1.png")
show()