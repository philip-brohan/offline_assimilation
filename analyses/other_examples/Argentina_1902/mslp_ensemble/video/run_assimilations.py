#!/usr/bin/env python

# Do all the jacknife assimilations for a range of times
# Just generates the commands to run - run with gnu parallel or similar.

import os
import sys
import time
import subprocess
import datetime
import glob
import SEF
import pandas
import numpy
from collections import OrderedDict

# Assimilate observations within this range of the field
hours_before=12
hours_after=12

# Where to put the output files
opdir="%s/images/ADWR_jacknife" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this time+omitted station
def is_done(dte,omit):
    opfile="%s/%04d%02d%02d%02d.pkl" % (opdir,dte.year,dte.month,
                                        dte.day,dte.hour)
    if omit is not None:
        opfile="%s/%04d%02d%02d%02d_%s.pkl" % (opdir,dte.year,dte.month,
                                               dte.day,dte.hour,omit)
    if os.path.isfile(opfile):
        return True
    return False

f=open("run.txt","w+")

start_day=datetime.datetime(1902, 8, 10, 18)
end_day  =datetime.datetime(1902, 8, 25, 18)

dte=start_day
while dte<=end_day:

    # What stations do we need to do at this point in time?
    # Load all the Argentine DWR pressures at this time
    adf=glob.glob('../../../../../../station-data/ToDo/sef/Argentinian_DWR/1902/DWR_*_MSLP.tsv')
    obs={'Name': [], 'Latitude': [], 'Longitude': [], 'mslp' : []}
    for file in adf:
       stobs=SEF.read_file(file)
       df=stobs['Data']
       #hhmm=int("%2d%02d" % (dte.hour,17))
       mslp=df.loc[(df['Year'] == dte.year) & 
                   (df['Month'] == dte.month) &
                   (df['Day'] == dte.day)]
       if mslp.empty: continue
       if mslp['Value'].values[0]==mslp['Value'].values[0]:
           obs['Name'].append(stobs['ID'])
           obs['Latitude'].append(stobs['Lat'])
           obs['Longitude'].append(stobs['Lon'])
           obs['mslp'].append(mslp['Value'].values[0])
    obs=pandas.DataFrame(obs)
    stations=obs.Name.values.tolist()
    stations=list(OrderedDict.fromkeys(obs.Name.values))
    stations.append(None) # Also do case with all stations

    for station in stations:

        if is_done(dte,station): continue

        cmd="./leave-one-out.py --year=%d --month=%d --day=%d --hour=%d" % (
                  dte.year,dte.month,dte.day,dte.hour)
        if station is not None:
            cmd="%s --omit=%s" % (cmd,station)
        cmd="%s\n" % cmd
        f.write(cmd)

    dte=dte+datetime.timedelta(hours=3)

f.close()
