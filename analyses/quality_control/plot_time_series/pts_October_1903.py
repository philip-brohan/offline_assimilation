# Monthly station time-series plot

import math
import datetime
from dateutil.relativedelta import relativedelta
import collections
import numpy

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import DWR
import DIYA

# Month to show
year=1903
month=10
dte=datetime.datetime(year,month,1,0)

# Get the DWR observations within +- 15 hours
obs=DWR.load_observations('prmsl',dte,
       dte+relativedelta(days=1)-relativedelta(minutes=1))
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

# Add quality control flags
obs['plausible']=DIYA.qc_plausible_range(obs,min=880,max=1060)
obs['background']=DIYA.qc_first_guess(obs,nsd=3,osd=1,version='2c')

# Portrait page
fig=Figure(figsize=(15,len(stations)),  # Width, Height (inches)
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
        'size'   : 16}
matplotlib.rc('font', **font)

# Fill plot with single figure
ax_scp=fig.add_axes([0.15,0.05,0.85,0.95])

# x-axis
ax_scp.set_xlim(dte,dte+relativedelta(months=1))
ax_scp.set_xlabel('Date')

# y-axis
ax_scp.set_ylim([1,len(stations)+2])
y_locations=[x+1 for x in range(1,len(stations)+1)]
ax_scp.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_scp.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
                  [DWR.pretty_name(s) for s in stations]))
ax_scp.set_ylabel('MSLP (hPa) for station')

# Custom grid spacing
for y in range(0,len(stations)):
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(dte,dte+relativedelta(months=1)),
            ydata=(y+2,y+2),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))
# Station obs
for y in range(0,len(stations)):
    station=stations[y]
    s_obs=obs[obs['name']==station].sort_values('dtm')
    omn=numpy.mean(s_obs.value.values)
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=s_obs.dtm.values,
            ydata=y+2+(s_obs.value.values-omn)/50.0,
            linestyle='solid',
            linewidth=0.2,
            color='black',
            zorder=4))
    # all obs in blue
    ax_scp.scatter(s_obs.dtm.values,
               y+2+(s_obs.value.values-omn)/50.0,
               25,
               'blue', # Color
               marker='.',
               edgecolors='face',
               linewidths=1.0,
               alpha=1.0,
               zorder=5)
    # implausible obs in red
    s_implausible=s_obs[s_obs.plausible==False]
    ax_scp.scatter(s_implausible.dtm.values,
               y+2+(s_implausible.value.values-omn)/50.0,
               25,
               'red', # Color
               marker='.',
               edgecolors='face',
               linewidths=1.0,
               alpha=1.0,
               zorder=6)
    # obs far from background in grey
    s_background=s_obs[s_obs.background==False]
    ax_scp.scatter(s_background.dtm.values,
               y+2+(s_background.value.values-omn)/50.0,
               25,
               'grey', # Color
               marker='.',
               edgecolors='face',
               linewidths=1.0,
               alpha=1.0,
               zorder=6)

# Output as png
fig.savefig('pts_%04d%02d.png' % (year,month))
