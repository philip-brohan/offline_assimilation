#!/usr/bin/env python

# UK region weather plot 
# Show pressures and covariances

import math
import datetime
import numpy
import pandas

import iris
import iris.analysis
import iris.util
import iris.analysis.stats

import matplotlib
import matplotlib.colors
import matplotlib.patches
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

# Date to show
year=1903
month=2
day=27
hour=6
dte=datetime.datetime(year,month,day,hour)

# Portrait page
fig=Figure(figsize=(11/math.sqrt(2),11),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=180, pole_latitude=35)
scale=15
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Single plot
ax=fig.add_axes([0,0,1,1],projection=projection)
ax.set_axis_off()
ax.set_extent(extent, crs=projection)

# Background, grid and land for both
ax.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax)
land_img=ax.background_img(name='GreyT', resolution='low')

# load the v3 pressures
prmsl=twcr.load('prmsl',dte,version='4.5.1')

# Pressure ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
mg.pressure.plot(ax,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Calculate spread correlation compared with Fort William station
observation_at = [('latitude', [56.8]), ('longitude', [-5.1])]
at_ob=prmsl.interpolate(observation_at,iris.analysis.Linear())
at_ob=iris.util.squeeze(at_ob)
corrs=iris.analysis.stats.pearsonr(prmsl,at_ob,corr_coords='member')

mg.precipitation.plot_cmesh(ax,corrs,resolution=0.25,
                            cmap='coolwarm',
                            alpha=0.5,
                            sqrt=False,
                            vmin=-0.5,vmax=1.0)

# Add an observation
rp=ax.projection.transform_points(ccrs.PlateCarree(),
                                  numpy.array(-5.1),
                                  numpy.array(56.8))
ax.add_patch(matplotlib.patches.Circle((rp[:,0],
                                        rp[:,1]),
                                        radius=0.2,
                                        facecolor='yellow',
                                        edgecolor='black',
                                        alpha=1,
                                        zorder=100))



# Output as png
fig.savefig('logo.png')
