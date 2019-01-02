#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 16:03:38 2018

@author: ahmed
source: file:///media/ahmed/MYLINUXLIVE/PyEphem/New%20folder/Fun%20with%20the%20Sun%20and%20PyEphem%20-%20Chris%20Ramsay.html

"""

# Import some bits
import ephem, math, datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
plt.style.use('Solarize_Light2')
home = ephem.Observer()
# Set up
home.date = '2017-01-01 09:00:00'
home.lat = '53.4975'
home.lon = '-0.3154'
sun = ephem.Sun()
sun.compute(home)
rising = home.previous_rising(sun).datetime()
print('Sunrise is at {}:{}:{}'.format(rising.hour, rising.minute, rising.second))

transit = home.next_transit(sun).datetime()
print('Local noon is at {}:{}:{}'.format(transit.hour, transit.minute, transit.second))

setting = home.next_setting(sun).datetime()
print('Sunset is at {}:{}:{}'.format(setting.hour, setting.minute, setting.second))
#%% Apparent Solar Time¶
# Prepare
home.date = '2017/1/1'
sun = ephem.Sun()
times = []

def get_diff(tm):
    """Return a difference in seconds between tm and 12:00:00 on tm's date"""
    a = datetime.datetime.combine(tm, datetime.time(12, 0))
    return (a-tm).total_seconds()/60

# Prepare the data
for i in range(1, 368):
    home.date += ephem.Date(1)
    trans = home.next_transit(sun).datetime()
    times.append(get_diff(trans))

# Set up
ts = pd.Series(times, index=pd.date_range('2017/1/1', periods=len(times)))

print("\n ---- Apparent Solar Time ------")

print(ts.loc['2017-04-14':'2017-04-26'])
plt.figure()
ax = ts.plot()
plt.rcParams["figure.figsize"] = [9, 6]
ax.set_xlabel(u'Date', fontsize=11)
ax.set_ylabel(u'Variation (minutes)', fontsize=11)
# Fire
plt.show()

#%% Drawing the Analemma

# Prepare
home.date = '2017/1/1 12:00:00'
sun = ephem.Sun()
posx = []
posy = []

# Solstice altitude
phi = 90 - math.degrees(home.lat)
# Earth axial tilt
epsilon = 23.439

def get_sun_az(tm):
    """Get the azimuth based on a date"""
    sun.compute(tm)
    return math.degrees(sun.az)

def get_sun_alt(tm):
    """Get the altitude based on a date"""
    sun.compute(tm)
    return math.degrees(sun.alt)

# Prepare the data
for i in range(1, 368):
    home.date += ephem.Date(1)
    trans = home.next_transit(sun).datetime()
    posx.append(get_sun_az(home))
    posy.append(get_sun_alt(home))

# Set up
fig, ax = plt.subplots()
ax.plot(posx, posy)
ax.grid(True)
ax.set_xlabel(u'Azimuth (°)', fontsize=11)
ax.set_ylabel(u'Altitude (°)', fontsize=11)
# Add some labels, lines & resize
ax.annotate('Vernal equinox', xy=(min(posx), phi + 1), xytext=(min(posx), phi + 1))
ax.annotate('Autumnal equinox', xy=(max(posx) -2, phi + 1), xytext=(max(posx) -2, phi + 1))
ax.annotate('Nothern solstice', xy=(180.1, phi + epsilon + 1), xytext=(180.1, phi + epsilon + 1))
ax.annotate('Southern solstice', xy=(180.1, phi - epsilon - 2), xytext=(180.1, phi - epsilon - 2))
plt.plot((min(posx), max(posx)), (phi + epsilon, phi + epsilon), 'blue')
plt.plot((min(posx), max(posx)), (phi, phi), 'pink')
plt.plot((min(posx), max(posx)), (phi - epsilon, phi - epsilon), 'green')
plt.axvline(180, color='yellow')
plt.rcParams["figure.figsize"] = [9, 6]
plot_margin = 4
x0, x1, y0, y1 = plt.axis()
plt.axis((x0, x1, y0 - plot_margin, y1 + plot_margin))
# Fire
plt.show()

#%% Changing the time of day we view the analemma
# Prepare
home.date = '2017/1/1 08:30:00'
home.horizon = '0'
sun = ephem.Sun()
posy = []
posx = []

def get_sun_az(tm):
    """Get the azimuth based on a date"""
    sun.compute(tm)
    return math.degrees(sun.az)

def get_sun_alt(tm):
    """Get the altitude based on a date"""
    sun.compute(tm)
    return math.degrees(sun.alt)

# Prepare the data
for i in range(1, 368):
    home.date += ephem.Date(1)
    posy.append(get_sun_alt(home))
    posx.append(get_sun_az(home))

# Set up
fig, ax = plt.subplots()
ax.plot(posx, posy)
# Add some labels & resize
ax.set_xlabel(u'Azimuth (°)', fontsize=11)
ax.set_ylabel(u'Altitude (°)', fontsize=11)
plt.rcParams["figure.figsize"] = [9, 6]
# Fire
plt.show()
#%% Calculating Twilights
initial_set = home.next_setting(sun).datetime() # zero edge
next_set = home.next_setting(sun, use_center=True).datetime() # zero centre
print("\n ---- Calculating Twilights ------")
print('Centre sunset is at {}:{}:{}'.format(next_set.hour, next_set.minute, next_set.second))
print('Edge sunset is at {}:{}:{}'.format(initial_set.hour, initial_set.minute, initial_set.second))

delta = initial_set - next_set

print('Time difference is {} mins, {} secs'.format(delta.seconds/60, delta.seconds%60))


def get_setting_twilights(obs, body):
    """Returns a list of twilight datetimes in epoch format"""
    results = []
    # Twilights, their horizons and whether to use the centre of the Sun or not
    twilights = [('0', False), ('-6', True), ('-12', True), ('-18', True)]
    for twi in twilights:
        # Zero the horizon
        obs.horizon = twi[0]
        try:
            # Get the setting time and date
            now = obs.next_setting(body, use_center=twi[1]).datetime()
            # Get seconds elapsed since midnight
            results.append(
                (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            )
        except ephem.AlwaysUpError:
            # There will be occasions where the sun stays up, make that max seconds
            results.append(86400.0)
    return results

home.horizon = '0'
twilights = get_setting_twilights(home, sun)
print(twilights)

# Prepare
home.date = '2017/01/01 12:00:00'
home.horizon = '0'
sun = ephem.Sun()
twidataset = []

# Calculate just over a year of data
for i in range(1, 368):
    home.date += ephem.Date(1)
    twidataset.append(get_setting_twilights(home, sun))
    
print(twidataset[150:160])

df = pd.DataFrame(twidataset, columns=['Sunset', 'Civil', 'Nautical', 'Astronomical'])

print(df[150:160])

#%% Plot Twilights¶
def timeformatter(x, pos):
    """The two args are the value and tick position"""
    return '{}:{}:{:02d}'.format(int(x/3600), int(x/24/60), int(x%60))

def dateformatter(x, pos):
    """The two args are the value and tick position"""
    dto = datetime.date.fromordinal(datetime.date(2017, 1, 1).toordinal() + int(x) - 1)
    return '{}-{:02d}'.format(dto.year, dto.month)

plt.rcParams["figure.figsize"] = [9, 6]
ax = df.plot.area(stacked=False, color=['#e60000', '#80ccff', '#33adff', '#008ae6'], alpha=0.2)
# Sort out x-axis
# Demarcate months
dim = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ax.xaxis.set_ticks(np.cumsum(dim))
ax.xaxis.set_major_formatter(FuncFormatter(dateformatter))
ax.set_xlabel(u'Date', fontsize=11)
# Sort out y-axis
ax.yaxis.set_major_formatter(FuncFormatter(timeformatter))
ax.set_ylim([55000, 86400])
ax.set_ylabel(u'Time', fontsize=11)
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30, fontsize=9)
# Done
plt.show()

#%% Sunset length throughout the year
# Prepare
home.date = '2017/04/01 12:00:00'
home.horizon = '0'
sun = ephem.Sun()
print("\n ---- Sunset length throughout the year ------")
# Starting with the 0 degrees
s_start = home.next_setting(sun, use_center=False).datetime()

print(s_start)

# Now the -0.53 degrees
home.horizon = '-0.53'
s_end = home.next_setting(sun, use_center=False).datetime()
print(s_end)

# The difference is...
delta = s_end - s_start
print(delta.total_seconds())

# Let's go for a little run and finish off with a pandas Series containing some data
home.date = '2017/01/01 12:00:00'
settings = []
sun = ephem.Sun()
for i in range(1, 368):
    home.date += ephem.Date(1)
    home.horizon = '0'
    start = home.next_setting(sun, use_center=False).datetime()
    home.horizon = '-0.53'
    end = home.next_setting(sun, use_center=False).datetime()
    settings.append((end - start).total_seconds())
    
ts = pd.Series(settings, index=pd.date_range('2017/1/1', periods=len(settings)))

print(ts[0:12])
plt.figure()
ax = ts.plot.area(alpha=0.2)
plt.rcParams["figure.figsize"] = [9, 6]
ax.set_xlabel(u'Date', fontsize=11)
ax.set_ylabel(u'Sunset length (seconds)', fontsize=11)
ax.set_ylim([math.floor(ts.min()) - 15, math.floor(ts.max()) + 15])
# Fire
plt.show()

