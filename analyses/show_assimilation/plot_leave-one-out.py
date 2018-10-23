#!/usr/bin/env python

# Assimilation of many stations.
# Plot the precalculated leave-one-out assimilation results

import os
import math
import datetime
import numpy
import pandas
import pickle
from collections import OrderedDict

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

import DWR

# Assimilate observations within this range of the field
hours_before=6
hours_after=6

# Where are the precalculated fields?
ipdir="%s/images/DWR_jacknife" % os.getenv('SCRATCH')

# Date to show
year=1905
month=3
day=15
hour=9
dte=datetime.datetime(year,month,day,hour)

# Landscape page
aspect=16/9.0
fig=Figure(figsize=(22,22/aspect),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 14}
matplotlib.rc('font', **font)

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
scale=15
extent=[scale*-1*aspect/3.0,scale*aspect/3.0,scale*-1,scale]

# On the left - spaghetti-contour plot of original 20CRv3
ax_left=fig.add_axes([0.005,0.01,0.323,0.98],projection=projection)
ax_left.set_axis_off()
ax_left.set_extent(extent, crs=projection)
ax_left.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_left)
land_img_left=ax_left.background_img(name='GreyT', resolution='low')

# 20CRv3 data
prmsl=twcr.load('prmsl',dte,version='4.5.1')

# 20CRv3 data
prmsl=twcr.load('prmsl',dte,version='4.5.1')
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those assimilated and near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                 (obs_t['Latitude']<90)) &
              ((obs_t['Longitude']>240) | 
                 (obs_t['Longitude']<100))].copy()

# Plot the observations
mg.observations.plot(ax_left,obs_s,radius=0.1)

# PRMSL spaghetti plot
mg.pressure.plot(ax_left,prmsl,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_left,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_left,
              '20CRv3',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

mg.utils.plot_label(ax_left,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.96,
              horizontalalignment='right')

# In the centre - spaghetti-contour plot of 20CRv3 with DWR assimilated
ax_centre=fig.add_axes([0.335,0.01,0.323,0.98],projection=projection)
ax_centre.set_axis_off()
ax_centre.set_extent(extent, crs=projection)
ax_centre.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_centre)
land_img_centre=ax_centre.background_img(name='GreyT', resolution='low')

# Get the DWR observations for that afternoon
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=hours_before),
                          dte+datetime.timedelta(hours=hours_after))

# Throw out the ones already used in 20CRv3
obs=obs[~obs['name'].isin(['ABERDEEN','VALENCIA','JERSEY','STOCKHOLM',
                           'LISBON','THEHELDER','HAPARANDA','MUNICH',
                           'BODO','HERNOSAND','WISBY','FANO','BERLIN'])]
obs.value=obs.value*100

# Load the all-stations-assimilated mslp
prmsl2=pickle.load( open( "%s/%04d%02d%02d%02d.pkl" % 
                          (ipdir,dte.year,dte.month,
                                    dte.day,dte.hour), "rb" ) )

mg.observations.plot(ax_centre,obs_s,radius=0.1)
mg.observations.plot(ax_centre,obs,
                     radius=0.1,facecolor='red',
                     lat_label='latitude',
                     lon_label='longitude')

# PRMSL spaghetti plot
mg.pressure.plot(ax_centre,prmsl2,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_centre,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_centre,
              '+DWR obs',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')


# Validation scatterplot on the right
obs=obs.sort_values(by='latitude',ascending=True)
stations=list(OrderedDict.fromkeys(obs.name.values))
# Need obs from a wider time-range to interpolate observed pressures
interpolate_obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=13),
                          dte+datetime.timedelta(hours=13))

ax_right=fig.add_axes([0.74,0.05,0.255,0.94])
# x-axis
xrange=[940,1025]
ax_right.set_xlim(xrange)
ax_right.set_xlabel('')

# y-axis
ax_right.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_right.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_right.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
                  [DWR.pretty_name(s) for s in stations]))

# Custom grid spacing
for y in range(0,len(stations)):
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=xrange,
            ydata=(y+1,y+1),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

latlon={}
for station in stations:
   latlon[station]=DWR.get_station_location(obs,station)

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    try:
        mslp=DWR.at_station_and_time(interpolate_obs,station,dte)
    except StandardError: continue 
    if mslp is None: continue                              
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.1,y+1.9),
            linestyle='solid',
            linewidth=3,
            color=(0,0,0,1),
            zorder=1))

# for each station, plot the reanalysis ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
for y in range(len(stations)):
    station=stations[y]
    ensemble=interpolator([latlon[station]['latitude'],
                           latlon[station]['longitude']])

    ax_right.scatter(ensemble.data/100.0,
                numpy.linspace(y+1.5,y+1.9,
                              num=len(ensemble.data)),
                20,
                'blue', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# For each station, assimilate all but that station, and plot the resulting ensemble
for y in range(len(stations)):
    station=stations[y]
    prmsl2=pickle.load( open( "%s/%04d%02d%02d%02d_%s.pkl" % 
                                   (ipdir,dte.year,dte.month,
                                    dte.day,dte.hour,station), "rb" ) )
    interpolator = iris.analysis.Linear().interpolator(prmsl2, 
                                   ['latitude', 'longitude'])
    ensemble=interpolator([latlon[station]['latitude'],
                           latlon[station]['longitude']])
    ax_right.scatter(ensemble.data/100.0,
                numpy.linspace(y+1.1,y+1.5,
                              num=len(ensemble.data)),
                20,
                'red', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

def pos_left(idx):
    station=stations[idx]
    ll=latlon[station]
    rp=ax_centre.projection.transform_points(ccrs.PlateCarree(),
                              numpy.asarray(ll['longitude']),
                              numpy.asarray(ll['latitude']))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.335+0.323*(new_lon-(scale*-1)*aspect/3.0)/(scale*2*aspect/3.0)
    result['y']=0.01+0.98*(new_lat-(scale*-1))/(scale*2)
    return result

# Label location of a station in ax_full coordinates
def pos_right(idx):
    result={}
    result['x']=0.668
    result['y']=0.05+(0.94/len(stations))*(idx+0.5)
    return result

for i in range(len(stations)):
    p_left=pos_left(i)
    if p_left['x']<0.335 or p_left['x']>(0.335+0.323): continue
    if p_left['y']<0.005 or p_left['y']>(0.005+0.94): continue
    p_right=pos_right(i)
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,1.0),
            zorder=1))

# Output as png
fig.savefig('Leave_one_out_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
