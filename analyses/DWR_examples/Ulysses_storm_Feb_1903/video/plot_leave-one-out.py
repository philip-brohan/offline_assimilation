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

# Need constant list of stations over a wide time range
full_obs=DWR.load_observations('prmsl',
                          datetime.datetime(1903,2,24, 0),
                          datetime.datetime(1903,3, 1,23))
# Throw out the ones already used in 20CRv3
full_obs=full_obs[~full_obs['name'].isin(['ABERDEEN','VALENCIA','JERSEY','STOCKHOLM',
                                          'LISBON','THEHELDER','HAPARANDA','MUNICH',
                                          'BODO','HERNOSAND','WISBY','FANO','BERLIN'])]
full_obs=full_obs.sort_values(by='latitude',ascending=True)
stations=list(OrderedDict.fromkeys(full_obs.name.values))

# Assimilate observations within this range of the field
hours_before=8
hours_after=8

# Where are the precalculated fields?
ipdir="%s/images/DWR_jacknife" % os.getenv('SCRATCH')
# Where to put the plots?
opdir="%s/images/DWR_jacknife_png" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Date to show
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Hour of day (0 to 23.99)",
                    type=float,required=True)
args = parser.parse_args()

dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# load the assimilated field with interpolation where needed
def load_interpolated(dtel,omit):
    if dtel.hour%3==0 and dtel.minute==0:
        if omit is not None:
            dumpfile="%s/%04d%02d%02d%02d_%s.pkl" % (ipdir,dtel.year,dtel.month,
                                                     dtel.day,dtel.hour,omit)
            if not os.path.isfile(dumpfile):
                dumpfile="%s/%04d%02d%02d%02d.pkl" % (ipdir,dtel.year,dtel.month,
                                                         dtel.day,dtel.hour)
        else:
            dumpfile="%s/%04d%02d%02d%02d.pkl" % (ipdir,dtel.year,dtel.month,
                                                     dtel.day,dtel.hour)
        result=pickle.load( open( dumpfile, 'rb'))
        return result
    else:
        dte_prev=datetime.datetime(dtel.year,dtel.month,dtel.day,dtel.hour-dtel.hour%3,0)
        dte_next=dte_prev+datetime.timedelta(hours=3)
        r1=load_interpolated(dte_prev,omit)
        r2=load_interpolated(dte_next,omit)
        r1.attributes=r2.attributes
        r1=iris.cube.CubeList((r1,r2)).merge_cube()
        result=r1.interpolate([('time',dtel)],iris.analysis.Linear())
        return result

# Landscape page
aspect=16/9.0 # HD video size
fig=Figure(figsize=(10.8*aspect,10.8),  # Width, Height (inches)
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
        'size'   : 12}
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
              fontsize=12,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

mg.utils.plot_label(ax_left,
              '%04d-%02d-%02d:%02d' % (dte.year,dte.month,dte.day,dte.hour),
              fontsize=12,
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
prmsl2=load_interpolated(dte,None)

# Plot the obs used in 20CRv3
mg.observations.plot(ax_centre,obs_s,radius=0.1)
# Plot the obs assimilated
mg.observations.plot(ax_centre,obs,
                     radius=0.1,facecolor='red',
                     lat_label='latitude',
                     lon_label='longitude')
# Mark the stations available for the period, but with no obs close
#  enough in time to be assimilated into this field.
missing_obs=full_obs[~full_obs['name'].isin(obs.name.values)]
if not missing_obs.empty:
    mg.observations.plot(ax_centre,missing_obs,
                         radius=0.1,facecolor='black',
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
              fontsize=12,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

ax_right=fig.add_axes([0.74,0.05,0.255,0.94])
# x-axis
xrange=[940,1035]
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
   latlon[station]=DWR.get_station_location(full_obs,station)

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    try:
        (mslp,gap)=DWR.at_station_and_time_with_distance(full_obs,station,dte)
    except Exception: continue 
    if mslp is None: continue
    alpha=max(0,1-abs(gap)/3600.0)                             
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.1,y+1.9),
            linestyle='solid',
            linewidth=3,
            color=(0,0,0,alpha),
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
    prmsl2=load_interpolated(dte,station)
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
fig.savefig('%s/Leave_one_out_%04d%02d%02d%02d%02d.png' % 
                             (opdir,dte.year,dte.month,dte.day,dte.hour,dte.minute))
