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
from cartopy.feature.nightshade import Nightshade

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


def get_eclipse(t0, lats=n.linspace(30, 75, num=50), lons=n.linspace(0, 20, num=50)):
    # Location
    obs = ephem.Observer()
    n_lats = len(lats)
    n_lons = len(lons)

    p = n.zeros([n_lats, n_lons])
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
                (sun.az, sun.alt), (moon.az, moon.alt)))
            percent_eclipse = 0.0

            if s < (r_moon + r_sun):
                #                        print("eclipsed")
                if s < 1e-3:
                    percent_eclipse = 1.0
                else:
                    percent_eclipse = intersection(r_moon, r_sun, s, n_s=100)

            if n.degrees(sun.alt) <= r_sun:
                if n.degrees(sun.alt) <= -r_sun:
                    percent_eclipse = 1.0
                else:
                    percent_eclipse = 1.0 - \
                        ((n.degrees(sun.alt) + r_sun) / (2.0 * r_sun)) * \
                        (1.0 - percent_eclipse)

            p[lai, loi] = percent_eclipse

    return(p)

#%% Then a small function to plot eclipse fraction as a colormesh using basemap and matplotlib


def plot_map(p, lons, lats, t0, alt=0, lat_0=69, lon_0=16):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

#    date = datetime(2015, 3, 20, 7, 00, 0)
    
#    ax.set_title('Night time shading for {}'.format(date))
    ax.stock_img()
#    ax.add_feature(Nightshade(date, alpha=0.2))

    lon, lat = n.meshgrid(lons, lats)
    # draw filled contours.
    cs = ax.contourf(lon, lat, 1.0 - p, transform=ccrs.PlateCarree(),
                cmap='inferno', alpha = 0.6)
    cl = ax.contour(lon, lat, p, levels = n.arange(0, 1, 0.1),
                    colors='k',origin='lower',extent=(-10, 60, 0, 90), alpha=.5, linewidth = .5)
#    plt.clabel(cl, inline=True, fmt='%1.1f', fontsize=8)
    # add colorbar.
    fig.colorbar(cs, ax=ax)
    ax.set_title("Fraction of sunlight at %1.2f km\n%s (UTC)" % (alt / 1e3, ephem.Date(t0)))
    fname = "eclipse-%f.jpg" % (t0)
    plt.text(1e5, 1e5, "Ahmed Ammar c 2018", color="k")
    print("saving %s" % (fname))
    plt.tight_layout()
    plt.savefig(fname)
#%% Create images with 900 second time step


if __name__ == "__main__":
    for i in range(20):
        p = get_eclipse(ephem.date((2015, 3, 20, 7, 30, 0)) + ephem.second * 900 * i,
                        lats=n.linspace(-90, 90, num=300), lons=n.linspace(-180, 180, num=300))

        plot_map(p, lats=n.linspace(-90, 90, num=300), lons=n.linspace(-180, 180, num=300),
                 t0=ephem.date((2015, 3, 20, 7, 00, 0)) + ephem.second * 900 * i, alt=0, lat_0=45, lon_0=10)
