"""
Ref:
    http://mathworld.wolfram.com/Lune.html
"""
import ephem as ep
from pylab import *
from operator import itemgetter

def check_non_zero(x):
    return x > 0
# OBSERVATEUR
obs = ep.Observer()
obs.lon, obs.lat, obs.elev = '10.08', '36.4', 100.0
obs.name = "SAT-TUNIS"
# Objets
soleil, lune = ep.Sun(), ep.Moon()
# temps initial
ts = (2027, 8, 2, 8, 00, 00)
obs.date=ts



# Output list
results=[]

for x in range(0,11000):
    obs.date= (ep.date(ep.date(ts)+x*ep.second))
    soleil.compute(obs)
    lune.compute(obs)
    r_soleil=soleil.size/2
    r_lune=lune.size/2
    s=degrees(ep.separation((soleil.az, soleil.alt),
                            (lune.az, lune.alt)))*60*60

    # Calculate the size of the lune in arcsec^2
    if s<(r_lune+r_lune):
        lunedelta=0.25*sqrt((r_lune+r_lune+s)*(r_lune+s-r_lune)*
                            (s+r_lune-r_lune)*(r_lune+r_lune-s))
    else: # If s>r_lune+r_lune there is no eclipse taking place
        lunedelta=None
        percent_eclipse=0
    if lunedelta: 
        lune_area=2*lunedelta + r_lune*r_lune*(arccos(((r_lune*r_lune)
        -(r_lune*r_lune)-(s*s))/(2*r_lune*s))) - r_lune*r_lune*(arccos(((r_lune*r_lune)+(s*s)-(r_lune*r_lune))/(2*r_lune*s)))
        percent_eclipse=(1-(lune_area/(pi*r_lune*r_lune)))*100 # Calculate percentage of lune's disc eclipsed using lune area and sun size
    results.append([obs.date.datetime(),s,lune.size,lune.size,
                    lune_area if lunedelta else 0, percent_eclipse]) ### Append to list of lists
gen=(x for x in results) # Find Max percentage of eclipse...
max_eclipse=max(gen, key=itemgetter(5))
print(obs.name +", république tunisienne\n")
print("Max eclipse at: " + str(max_eclipse[0])) # ...and return the time
print("Max percent: " + '%.2f' % max_eclipse[5]) # ...and return the percentage
gen=(x for x in results)
print("First contact: " + str(next(x for x in gen if check_non_zero(x[5]))[0])) # Find first contact...
print("Last contact: " + str(next(x for x in gen if x[5]==0)[0])) ### ...and last contact

