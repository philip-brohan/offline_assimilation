#!/usr/bin/env python

# Assimilation of many stations.

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

import DWR
import DIYA
import sklearn
RANDOM_SEED = 5

# Date to show
year=1903
month=10
day=22
hour=18
dte=datetime.datetime(year,month,day,hour)

# model to fit
model=sklearn.linear_model.Lasso()
# Assumed observation error (Pa)
obs_error=5 

# Landscape page
fig=Figure(figsize=(22,22/math.sqrt(2)),  # Width, Height (inches)
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
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Two side-by-side plots
ax_one=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_one.set_axis_off()
ax_one.set_extent(extent, crs=projection)
ax_three=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_three.set_axis_off()
ax_three.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_one.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_three.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_one)
mg.background.add_grid(ax_three)
land_img_one=ax_one.background_img(name='GreyT', resolution='low')
land_img_three=ax_three.background_img(name='GreyT', resolution='low')

# Get the DWR observations for that afternoon
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=0.1),
                          dte+datetime.timedelta(hours=0.1))
# Throw out the ones already used in 20CRv3
obs=obs[~obs['name'].isin(['ABERDEEN','VALENCIA','JERSEY'])]

# 20CRv3 data
prmsl=twcr.load('prmsl',dte,version='4.5.1')
# Get the observations used in 20CRv3
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those assimilated and near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                 (obs_t['Latitude']<90)) &
              ((obs_t['Longitude']>240) | 
                 (obs_t['Longitude']<100))].copy()


mg.observations.plot(ax_one,obs_s,radius=0.15)

# For each ensemble member, make a contour plot
mg.pressure.plot(ax_one,prmsl,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_one,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_one,'20CRv3',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

obs_assimilate=obs
obs_assimilate.value=obs_assimilate.value*100 # to Pa

# Plot the selected stations
mg.observations.plot(ax_three,obs_s,radius=0.15)
mg.observations.plot(ax_three,obs_assimilate,
                     radius=0.15,facecolor='red',
                     lat_label='latitude',
                     lon_label='longitude')

# Update mslp by assimilating obs.
prmsl2=DIYA.constrain_cube(prmsl,prmsl,
                           obs=obs_assimilate,
                           obs_error=obs_error,
                           random_state=RANDOM_SEED,
                           model=model,
                           lat_range=(20,85),
                           lon_range=(280,60))

# For each ensemble member, make a contour plot
mg.pressure.plot(ax_three,prmsl2,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_three,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_three,'With all DWR observations',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

mg.utils.plot_label(ax_three,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              horizontalalignment='right')

# Output as png
fig.savefig('none+all_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
