#!/usr/bin/env python

# Do all the jacknife assimilations for a range of times

import os
import sys
import time
import subprocess
import datetime
import pandas

# Where to put the output files
opdir="%s/images/DWR_fake" % os.getenv('SCRATCH')
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

start_day=datetime.datetime(1811, 12, 23, 12)
end_day  =datetime.datetime(1811, 12, 23, 12)

f=open("run.txt","w+")

dte=start_day
while dte<=end_day:

    # Fake the stations for this point in time?
    obs=pandas.read_csv('stations.csv',header=None,
                        names=('name','latitude','longitude'))
    obs=obs.assign(dtm=pandas.to_datetime(dte))
    # Throw out the ones already used in 20CRv3
    obs=obs[~obs['name'].isin(['Ylitornio','Paris','Turin','Geneva',
                           'Barcelona','Stockholm'])]
    stations=obs.name.values.tolist()
    stations.append(None) # Also do case with all stations

    for station in stations:

        if is_done(dte,station): continue
        cmd="./leave-one-out.py --year=%d --month=%d --day=%d --hour=%d" % (
                  dte.year,dte.month,dte.day,dte.hour)
        if station is not None:
            cmd="%s --omit=%s" % (cmd,station)
        cmd="%s\n" % cmd
        f.write(cmd)
    dte=dte+datetime.timedelta(hours=6)
f.close()
