# Compare assimilation of one station and three stations.

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

import Meteorographica.weathermap as wm
import Meteorographica.data.twcr as twcr

import DWR
import DIYA
import sklearn
import collections
RANDOM_SEED = 5

# Date to show
year=1903
month=10
day=22
hour=6
dte=datetime.datetime(year,month,day,hour)

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
wm.add_grid(ax_one)
wm.add_grid(ax_three)
land_img_one=ax_one.background_img(name='GreyT', resolution='low')
land_img_three=ax_three.background_img(name='GreyT', resolution='low')

# Get the DWR observations for that morning
#  only those at 8 for simplicity
obs=DWR.load_observations('prmsl',
                          dte+datetime.timedelta(hours=1.9),
                          dte+datetime.timedelta(hours=2.1))
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

# Reduce to 1/3 of stations
to_assimilate=stations[::3]
obs_assimilate=obs[obs.name.isin(to_assimilate)]
obs_assimilate.value=obs_assimilate.value*100 # to Pa

# 20CR2c data
prmsl=twcr.load('prmsl',year,month,day,hour,
                             version='2c')
# Get the observations used in 20CR2c
obs_t=twcr.load_observations(dte-datetime.timedelta(hours=24),dte,
                                                    version='2c')
# Filter to those assimilated and near the UK
obs_s=obs_t.loc[(obs_t['Assimilation.indicator']==1) &
              ((obs_t['Latitude']>0) & 
                 (obs_t['Latitude']<90)) &
              ((obs_t['Longitude']>240) | 
                 (obs_t['Longitude']<100))].copy()

# Update mslp by assimilating Fort William ob.
prmsl2=DIYA.constrain_cube(prmsl,prmsl,
                           obs=obs_assimilate,
                           obs_error=0.1,
                           random_state=RANDOM_SEED,
                           model=sklearn.linear_model.LinearRegression(),
                           lat_range=(20,85),
                           lon_range=(280,60))

wm.plot_obs(ax_one,obs_s,radius=0.1)
wm.plot_obs(ax_one,obs_assimilate,lat_label='latitude',
            lon_label='longitude',radius=0.1,facecolor='red')

# For each ensemble member, make a contour plot
for m in prmsl2.coord('member').points:
    prmsl_e=prmsl2.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_one,prmsl_e,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.2)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_one,prmsl_m,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Now use 2/3 of stations
obs_assimilate=obs[~obs.name.isin(to_assimilate)]
obs_assimilate.value=obs_assimilate.value*100 # to Pa

# Plot the selected stations
wm.plot_obs(ax_three,obs_s,radius=0.1)
wm.plot_obs(ax_three,obs_assimilate,lat_label='latitude',
            lon_label='longitude',radius=0.1,facecolor='red')

# Update mslp by assimilating three obs.
prmsl2=DIYA.constrain_cube(prmsl,prmsl,
                           obs=obs_assimilate,
                           obs_error=0.1,
                           random_state=RANDOM_SEED,
                           model=sklearn.linear_model.LinearRegression(),
                           lat_range=(20,85),
                           lon_range=(280,60))

# For each ensemble member, make a contour plot
for m in prmsl2.coord('member').points:
    prmsl_e=prmsl2.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_three,prmsl_e,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.2)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_three,prmsl_m,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

wm.plot_label(ax_three,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              horizontalalignment='right')

# Output as png
fig.savefig('multi_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
