# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 22:06:05 2017

@author: ahmed
"""

# IMPORTATION
from pylab import *
plt.style.use('dark_background')
import ephem as ep
# OBSERVATEUR
obs = ep.Observer()
# TUNIS
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
# CRÉER DES OBJETS
Slonce = ep.Sun()
Ksiezyc = ep.Moon()
# intervalle de temps - 20 minutes
dt = ep.hour/4.
# TEMPS DE DÉBUT 
ts = ep.Date("2027-08-02 08:00:00")
obs.date = ts

# nous calculons les coordonnées
Slonce.compute(obs)
Ksiezyc.compute(obs)
rs = degrees(Slonce.radius)
rk = degrees(Ksiezyc.radius )

# Nous créons un graphique en l'attribuant à un pl COMME variable
fig=plt.figure(figsize=(5,5))
pl = subplot(111, aspect ="equal")
# titre du graphique avec date et heure
pl.set_title (u"TUNIS \n début en (TU): "+str(ep.Date(ts)))
# Nous nous plaçons le soleil dans le centre
sc=Circle((0 ,0), rs, facecolor ="yellow",
            edgecolor ="red", lw =2)

pl.add_artist(sc)
# les coordonnées du Soleil
pl.text(0, rs+0.1, "Az: %.1f, El: %.1f"%(degrees(Slonce.az), degrees(Slonce.alt)),
        ha='center', fontsize =14)

# Nous plaçons la Lune dans la figure 
for i in range(10):
    print("time UT: ", ep.Date(ts))
    obs.date = ts
    # nous calculons les coordonnées
    Slonce.compute(obs)
    Ksiezyc.compute(obs)
    # Nous calculons la différence de position
    az = degrees(Slonce.az - Ksiezyc.az)
    el = degrees(Slonce.alt - Ksiezyc.alt)
    # dessiner et la position réelle en empillements d'image de Lune; le Soleil estau centre 
    kc = Circle((az , el), rk , facecolor ="gray",
                edgecolor ="black", lw =2, alpha =0.3)
    pl.add_artist(kc)
    # augmenter le temps de 20 minutes
    ts += dt
    
pl.set_xlim (-1.0, 1.0)
pl.set_ylim (-1.0, 1.0)
pl.set_xlabel (u"degré")
pl. set_ylabel (u"degré")
plt.tight_layout()
savefig("../figs/eclipse_sol_" + str(ts) +".pdf"); savefig("../figs/eclipse_sol_" + str(ts) +".png")
show ()