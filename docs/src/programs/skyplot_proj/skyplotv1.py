# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import astropy
from scipy.spatial import cKDTree

import numpy as np
import matplotlib.pyplot as plt
data=np.genfromtxt('ybs.degbv',names=True)
messier=np.genfromtxt('Messierdec.txt',names=True)

vlim=4.5
magscale=10
starsize=magscale*(vlim-data['v'])
#norm = ((-data['v'])-( (-data['v'])).min())/(data['v'].max()-data['v'].min())
#starsize=vlim+norm*starsize

import astropy

from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

starcoords=SkyCoord(ra=data['ra']*u.degree,dec=data['dec']*u.degree)
mcoords=SkyCoord(ra=messier['Mra']*15.*u.degree,dec=messier['Mdec']*u.degree)

CT=EarthLocation(lat=-30.159*u.deg,lon=-70.809*u.deg,height=2207.*u.m)
KP=EarthLocation(lat=31.98*u.deg,lon=-111.60*u.deg,height=2097.*u.m)
RM=EarthLocation(lat=28.7569*u.deg,lon=-17.8925*u.deg,height=2267.*u.m)
sitecodes=['CT','KP','RM']
sitenames=['Cerro Tololo','Kitt Peak', 'La Palma']


for site in range(0,2):
    if site==0:
        obsloc=CT
    if site==1:
        obsloc=KP
    utcoffset=-5.0*u.hour
    showtime = Time('2015-7-21 22:00:00') - utcoffset
    showtime=Time.now()
    print(showtime.iso)
    staraltaz=starcoords.transform_to(AltAz(obstime=showtime,location=obsloc))
    az2plot=np.pi/2.+np.array((3.1415926/180.)*u.degree*staraltaz.az)
    zd2plot=np.array(90.*u.degree-staraltaz.alt)
    #pos4kd=np.array([[az2plot],[zd2plot]])
    upind=(zd2plot < 90.).nonzero()
    plt.clf()
    plt.figure(site+1)
    ax=plt.subplot(111,polar=True)
    ax.grid(False)
    ax.set_xticklabels(['W', '', 'N', '', 'E', '', 'S', ''])
    
    #plt.fill_between([0,90],[0,0],[360,360],facecolor='0')
    plt.scatter(az2plot[upind],zd2plot[upind],s=starsize[upind],c=data['bv'][upind],cmap='rainbow',linewidth=0,vmax=1.2,vmin=-0.5)
    plt.ylim([0.,90.])
    cb=plt.colorbar(pad=0.10)
    cb.set_label('Star color, B-V')
    #plt.tick_params(axis='x',labelbottom='off')
    plt.tick_params(axis='y',labelleft='off')
    ax.set_xticklabels(['W', '', 'N', '', 'E', '', 'S', ''])
    # add parallels of declination every 30 degrees
    for jdec in range(5):
        pardeg=60.-30.*jdec
        parra=np.array(range(361))
        skpar=SkyCoord(ra=parra*u.degree,dec=pardeg*u.degree)
        paraltaz=skpar.transform_to(AltAz(obstime=showtime,location=obsloc))
        paraz2plot=np.pi/2.+np.array((3.14159265/180.)*u.degree*paraltaz.az)
        parzd2plot=np.array(90.*u.degree-paraltaz.alt)
        plt.plot(paraz2plot,parzd2plot,linewidth=1,color='gray',linestyle=':')
        
    # plot Messier objects
    maltaz=mcoords.transform_to(AltAz(obstime=showtime,location=obsloc))
    maz2plot=np.pi/2.+np.array((3.1415926/180.)*u.degree*maltaz.az)
    mzd2plot=np.array(90.*u.degree-maltaz.alt)
    upm=(mzd2plot < 90.).nonzero()
    
    #plt.scatter(maz2plot[upm],mzd2plot[upm],s=100,c=messier['Mclass'][upm],cmap='rainbow',alpha=0.4,linewidth=0)
    plt.title(str(sitenames[site])+' '+showtime.iso+' UT\n')
    labelcolors=np.array(['blue','blue','green','orange','red'])
    mlabels=np.array(['{0}'.format(i+1) for i in range(110)])
    for j in range(110):
        plt.annotate(mlabels[j],xy=(maz2plot[j],mzd2plot[j]),xytext=(0,0),textcoords='offset points',color=labelcolors[messier['Mclass'][j]],size='small')
    #add Magellanic clouds
    sklmc=SkyCoord(ra=15.0*5.25*u.degree,dec=-68.7*u.degree)
    sksmc=SkyCoord(ra=0.77*15.0*u.degree,dec=-73.0*u.degree)
    lmcaltaz=sklmc.transform_to(AltAz(obstime=showtime,location=obsloc))
    smcaltaz=sksmc.transform_to(AltAz(obstime=showtime,location=obsloc))
    plt.scatter(np.pi/2.+np.array((3.1415926/180.)*u.degree*lmcaltaz.az),90.*u.degree-lmcaltaz.alt,s=250,c='green',alpha=0.3)
    plt.scatter(np.pi/2.+np.array((3.1415926/180.)*u.degree*smcaltaz.az),90.*u.degree-smcaltaz.alt,s=120,c='green',alpha=0.3)
    
    #add constellation lines
    conlines=np.genfromtxt('constellations.txt',names="star1, star2")
    nstar1=np.array(conlines['star1'])
    nstar2=np.array(conlines['star2'])
    nstars=nstar1.size
    starnumbers=np.array(data['starnum'])
    for jstar in range(nstars):
            indexstar1=np.where(starnumbers==nstar1[jstar])[0]
            indexstar2=np.where(data['starnum']==nstar2[jstar])[0]
            plotx=np.array((az2plot[indexstar1],az2plot[indexstar2]))
            ploty=np.array((zd2plot[indexstar1],zd2plot[indexstar2]))
            plt.plot(plotx,ploty,linewidth=1,color='black',zorder=0)
    
    plt.annotate('Messier Objects:',xy=(0.04,0.18),xycoords='figure fraction')
    plt.annotate('Nebula',xy=(0.05,0.145),xycoords='figure fraction',color='blue')
    plt.annotate('Galaxy',xy=(0.05,0.11),xycoords='figure fraction',color='green')
    plt.annotate('Open cluster',xy=(0.05,0.075),xycoords='figure fraction',color='orange')
    plt.annotate('Globular cluster',xy=(0.05,0.04),xycoords='figure fraction',color='red')
    plt.show()
    if site==0:
        plt.savefig('SkyplotCTIO.png')
    if site==1:
        plt.savefig('SkyplotKPNO.png')


    
        
