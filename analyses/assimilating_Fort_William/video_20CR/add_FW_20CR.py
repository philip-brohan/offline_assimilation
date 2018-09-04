#!/usr/bin/env python

# Show effect of assimilating Fort William observation
# Video frame version

import os
import math
import datetime
import numpy
import pandas

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

import DIYA
RANDOM_SEED = 5

# Get the datetime to plot from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Time of day (0 to 23.99)",
                    type=float,required=True)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/images/DWR/Add_FW_20CR" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

if (args.year!=1903 or args.month!=2):
   raise StandardError("Obs only available for Feb 1903.")

dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# HD video size 1920x1080
aspect=16.0/9.0
fig=Figure(figsize=(10.8*aspect,10.8),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
scale=12
extent=[scale*-1*aspect/2,scale*aspect/2,scale*-1,scale]

# Two side-by-side plots
ax_20C=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_20C.set_axis_off()
ax_20C.set_extent(extent, crs=projection)
ax_wFW=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_wFW.set_axis_off()
ax_wFW.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_wFW.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_20C)
mg.background.add_grid(ax_wFW)
land_img_20C=ax_20C.background_img(name='GreyT', resolution='low')
land_img_DWR=ax_wFW.background_img(name='GreyT', resolution='low')

# 20CR2c data
prmsl=twcr.load('prmsl',dte,version='2c')

# Get the observations used in 20CR2c
obs=twcr.load_observations_fortime(dte,version='2c')
# Filter to those assimilated and near the UK
obs_s=obs.loc[(obs['Assimilation.indicator']==1) &
              ((obs['Latitude']>0) & 
                 (obs['Latitude']<90)) &
              ((obs['Longitude']>240) | 
                 (obs['Longitude']<100))].copy()
mg.observations.plot(ax_20C,obs_s,radius=0.1)

# Contour spaghetti plot of ensemble members
mg.pressure.plot(ax_20C,prmsl,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.2)

# Add the ensemble mean - with labels
# Mask out mean where uncertainties large
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_20C,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_20C,'20CR2c',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# Get the Fort William ob
station_lat=56.82
station_lon= -5.1
FW_data=pandas.read_table('../FW_pressure_Feb_1903.dat',
                          header=None,
                          delim_whitespace=True)
i_day=args.day
i_hour=int(args.hour)
if i_hour==0: # 0 is 24 the previous day in table
    i_day=i_day-1
    i_hour=24
FW_ob_p=FW_data.iloc[i_day-1,i_hour+2]*1
i_hour=i_hour+1
if i_hour==25:
    i_day=i_day+1
    i_hour=1
FW_ob_n=FW_data.iloc[i_day-1,i_hour+2]*1
weight_n=args.hour%1
if weight_n==1: weight_n=0
FW_ob=FW_ob_n*weight_n+FW_ob_p*(1-weight_n)
obs_assimilate=pandas.DataFrame(data={'year': args.year,
                                      'month': args.month, 
                                      'day': args.day,
                                      'hour': int(args.hour),
                                      'minute': int((args.hour%1)*60),
                                      'latitude': station_lat,
                                      'longitude': station_lon,
                                      'value': FW_ob, 
                                      'name': 'Fort William'},
                                       index=[0])
obs_assimilate=obs_assimilate.assign(dtm=pandas.to_datetime(
                   obs_assimilate[['year','month',
                                     'day','hour','minute']]))

# Update mslp by assimilating Fort William ob.
prmsl2=DIYA.constrain_cube(prmsl,prmsl,
                           obs=obs_assimilate,obs_error=10,
                           random_state=RANDOM_SEED,
                           lat_range=(20,85),
                           lon_range=(280,60))

# Plot the assimilated obs
mg.observations.plot(ax_wFW,obs_s,radius=0.1)
# Plot the Fort William ob
mg.observations.plot(ax_wFW,obs_assimilate,lat_label='latitude',
            lon_label='longitude',radius=0.1,facecolor='red')

# Contour spaghetti plot of ensemble members
mg.pressure.plot(ax_wFW,prmsl2,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.2)

# Add the ensemble mean - with labels
# Mask out mean where uncertainties large
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_wFW,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_wFW,'With Fort William observation',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

mg.utils.plot_label(ax_wFW,
              ('%04d-%02d-%02d:%02d' % 
                (args.year,args.month,args.day,args.hour)),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              horizontalalignment='right')

# Output as png
fig.savefig('%s/Add_FW_%04d%02d%02d%02d%02d.png' % 
                      (args.opdir,args.year,args.month,args.day,
                       int(args.hour),int(args.hour%1*60)))
