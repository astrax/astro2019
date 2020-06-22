#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 13:05:17 2018

@author: ahmed
"""

# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Calculate the totality of the eclipse.
#
import ephem
from datetime import datetime
import numpy as n
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
import pandas as pd

# load data
df1 = pd.read_excel('central_path.xlsx', sheet_name='central')
lons_c = df1['Lons']
lats_c = df1['Lats']

df2 = pd.read_excel('central_path.xlsx', sheet_name='lim_N')
lons_N = df2['Lons']
lats_N = df2['Lats']
df3 = pd.read_excel('central_path.xlsx', sheet_name='lim_S')
lons_S = df3['Lons']
lats_S = df3['Lats']

#%% numerically approximate eclipse fraction

def intersection(r0, r1, d, n_s=100):
    A1 = n.zeros([n_s, n_s])
    A2 = n.zeros([n_s, n_s])
    I = n.zeros([n_s, n_s])
    x = n.linspace(-2.0 * r0, 2.0 * r0, num=n_s)
    y = n.linspace(-2.0 * r0, 2.0 * r0, num=n_s)
    xx, yy = n.meshgrid(x, y)
    A1[n.sqrt((xx + d)**2.0 + yy**2.0) < r0] = 1.0
    n_sun = n.sum(A1)
    A2[n.sqrt(xx**2.0 + yy**2.0) < r1] = 1.0
    S = A1 + A2
    I[S > 1] = 1.0
    eclipse = n.sum(I) / n_sun
    return(eclipse)
#%%calculate the fraction that sun is eclipsed at given altitudes, latitude, and longitude
# returns eclipse fraction (0..1) and time (seconds after t0)

def get_eclipse(t0, lats=n.linspace(30, 75, num=50,dtype=n.float64), lons=n.linspace(0, 20, num=50,dtype=n.float64)):
    # Location
    obs = ephem.Observer()
    n_lats = len(lats)
    n_lons = len(lons)

    p = n.zeros([n_lats, n_lons],dtype=n.float64)
    for lai, lat in enumerate(lats):
        for loi, lon in enumerate(lons):
            # obs.lon, obs.lat = '-1.268304', '51.753101'#'16.02', '78.15' # ESR
            obs.lon, obs.lat = '%1.2f' % (lon), '%1.2f' % (lat)  # ESR
            obs.elevation = 0
            obs.date = t0  # (ephem.date(ephem.date(t0)+t*ephem.second))
            sun, moon = ephem.Sun(), ephem.Moon()
            # Output list
            sun.compute(obs)
            moon.compute(obs)
            r_sun = (sun.size / 2.0) / 3600.0
            r_moon = (moon.size / 2.0) / 3600.0
            s = n.degrees(ephem.separation(
                (sun.az, sun.alt), (moon.az, moon.alt)),dtype=n.float64)
            percent_eclipse = 0.0

            if s < (r_moon + r_sun):
                #                        print("eclipsed")
                if s < 1e-3:
                    percent_eclipse = 1.0
                else:
                    percent_eclipse = intersection(r_moon, r_sun, s, n_s=100)

            if n.degrees(sun.alt) <= r_sun:
                if n.degrees(sun.alt,dtype=n.float64) <= -r_sun:
                    percent_eclipse = 1.0
                else:
                    percent_eclipse = 1.0 - \
                        ((n.degrees(sun.alt,dtype=n.float64) + r_sun) / (2.0 * r_sun)) * \
                        (1.0 - percent_eclipse)

            p[lai, loi] = percent_eclipse

    return(p)

#%% Then a small function to plot eclipse fraction as a colormesh using basemap and matplotlib


def plot_map(p, lons, lats, t0, alt=0, lat_0=69, lon_0=16):
    fig = plt.figure(figsize=(7,5), dpi = 100)
    ax = fig.add_axes([0, 0, 1, 1],projection=ccrs.Robinson())
    ax.set_extent([3, 61, 38, 2], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle='-')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
#    date = datetime(2015, 3, 20, 7, 00, 0)
    
#    ax.set_title('Night time shading for {}'.format(date))
#    ax.stock_img()
#    ax.add_feature(Nightshade(date, alpha=0.2))

    lon, lat = n.meshgrid(lons, lats)
    # draw filled contours.
    cs = ax.contourf(lon, lat, 1.0 - p, transform=ccrs.PlateCarree(),
                cmap='inferno', alpha = 0.5)
    cl = ax.contour(lon, lat, p, levels = n.arange(0, 1, 0.1),vmin = 0., vmax = 1.,
                    colors='k',origin='lower',extent=(0, 65, 0, 45),lw = .5,transform=ccrs.PlateCarree(), alpha=.3)
    ax.plot(-lons_c,lats_c, color = "r", transform=ccrs.PlateCarree())
    ax.plot(-lons_N,lats_N, color = "g", transform=ccrs.PlateCarree())
    ax.plot(-lons_S,lats_S, color = "g", transform=ccrs.PlateCarree())
#    ax.plot([10,114.16],[36.4, -21], color='red', transform=ccrs.Geodetic())
#    plt.clabel(cl, inline=True, fmt='%1.1f', fontsize=8)
    # add colorbar.
    cs.set_clim(0., 1.)
    fig.colorbar(cs, ax=ax, pad=0.05, boundaries=n.linspace(0, 1, 8), shrink = .7)
    ax.set_title("Fraction de la lumière du soleil à %1.2f km\n%s (UTC)" % (alt / 1e3, ephem.Date(t0)))
    fname = "eclipse-%f.jpg" % (t0)
    #plt.text(1e5, 1e5, "Ahmed Ammar c 2018", color="k")
    print("saving %s" % (fname))
#    plt.tight_layout()
    plt.savefig(fname)
#%% Create images with 900 second time step


if __name__ == "__main__":
    for i in range(20):
        p = get_eclipse(ephem.date((2020, 6, 21, 3, 00, 0)) + ephem.second * 1200 * i,
                        lats=n.linspace(0, 90, num=800,dtype=n.float64), lons=n.linspace(0, 180, num=800,dtype=n.float64))

        plot_map(p, lats=n.linspace(0, 90, num=800,dtype=n.float64), lons=n.linspace(0, 180, num=800,dtype=n.float64),
                 t0=ephem.date((2020, 6, 21, 3, 00, 0)) + ephem.second * 1200 * i, alt=0, lat_0=36, lon_0=10)
