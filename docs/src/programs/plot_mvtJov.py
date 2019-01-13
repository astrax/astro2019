#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 22:06:24 2018
@author: ahmed
help arabe lang: https://stackoverflow.com/questions/15421746/matplotlib-writing-right-to-left-text-hebrew-arabic-etc
"""
# IMPORTATION
from pylab import *
import ephem as ep
# ARABE
import arabic_reshaper
from bidi.algorithm import get_display
# NOUS CRÉONS UN OBJET
Io = ep.Io()
Eu = ep.Europa()
Ga = ep.Ganymede()
Ca = ep.Callisto()
# Créons des tableaux vide pour
# SAUVEGARDER LES COORDONNEES 
y = [] 
xIo = []
xEu = []
xGa = []  
xCa = []

# pas de temps - heure
dt = ep.hour
# temps initial
ts = ep.now()
# heure actuelle
tm = ts
N=2*24
for i in range(N):
    # nous calculons des valeurs y
    y.append((tm - ts)*24.0)
    # nous calculons des valeurs x
    Io.compute(tm)
    Eu.compute(tm)
    Ga.compute(tm)
    Ca.compute(tm)
    # nous ajoutons des calculs aux tableaux
    xIo.append(Io.x)
    xEu.append(Eu.x)
    xGa.append(Ga.x)
    xCa.append(Ca.x)
    # on augmente le temps d'une heure
    tm += dt
    
fig1 = plt.figure()
plot(xIo, y, marker ="o", label ="Io")
plot(xEu, y, marker ="o", label ="Europa")
plot(xGa, y, marker ="o", label ="Ganimedes")
plot(xCa, y, marker ="o", label ="Callisto")
plot(zeros(len(y)),y ,marker =r"$\mathcircled{J}$", markersize =15,
     label ="Jupiter",color ="orange", fillstyle= 'none')
xlabel(u"position par rapport à Jupiter")
ylabel("Heures à partir de (%s TU)"% ts)
ylim(0,N+3)
title(u"Mouvement des lunes galiléennes")
grid()
legend(loc =1)

tight_layout()
savefig("../figs/mvtjov.pdf"); savefig("../figs/mvtjov.png")
show()

#fig2 = plt.figure()
#
#jup_ar = arabic_reshaper.reshape(u"المشتري")
#jupiter = get_display(jup_ar)
#io_ar = get_display(arabic_reshaper.reshape(u"آيو"))
#ga_ar = get_display(arabic_reshaper.reshape(u"غانيميد"))
#ca_ar = get_display(arabic_reshaper.reshape(u"كاليستو"))
#eu_ar = get_display(arabic_reshaper.reshape(u"أوروبا"))
#xlabel_ar = get_display(arabic_reshaper.reshape(u"الموقع  بالنسبة إلى المشتري"))
#ylabel_ar = get_display(arabic_reshaper.reshape(u"عدد الساعات بداية من"))
#title_ar = get_display(arabic_reshaper.reshape(u"حركة أقمار غاليليو"))
#with plt.style.context('dark_background'):
#    plot(xIo, y, marker ="o", label =io_ar)
#    plot(xEu, y, marker ="o", label =eu_ar)
#    plot(xGa, y, marker ="o", label =ga_ar)
#    plot(xCa, y, marker ="o", label =ca_ar)
#    plot(zeros(len(y)),y ,marker =r"$\mathcircled{J}$", markersize =15,
#         label =jupiter,color ="orange", fillstyle= 'none')
#    xlabel(xlabel_ar)
#    ylabel(ylabel_ar+"\n (%s TU)"% ts)
#    ylim(0,N+3)
#    title(title_ar, fontsize=16, weight='bold')
#    grid()
#    legend(loc =1)
#    tight_layout()
#    savefig("../figs/mvtjov_ar.pdf"); savefig("../figs/mvtjov_ar.png")
#    show()
    
