#!/usr/bin/env python

# Do all the jacknife assimilations for a range of times
# Just generates the commands to run - run with gnu parallel or similar.

import os
import sys
import time
import subprocess
import datetime
import DWR
from collections import OrderedDict

# Assimilate observations within this range of the field
hours_before=8
hours_after=8

# Where to put the output files
opdir="%s/images/DWR_jacknife_png" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this time+omitted station
def is_done(dte,omit):
    opfile="%s/%04d%02d%02d%02d.png" % (opdir,dte.year,dte.month,
                                        dte.day,dte.hour)
    if omit is not None:
        opfile="%s/%04d%02d%02d%02d_%s.pkl" % (opdir,dte.year,dte.month,
                                               dte.day,dte.hour,omit)
    if os.path.isfile(opfile):
        return True
    return False

f=open("run.txt","w+")

start_day=datetime.datetime(1903, 2, 27, 9)
end_day  =datetime.datetime(1903, 2, 27, 9)

dte=start_day
while dte<=end_day:

    # What stations do we need to do at this point in time?
    obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=hours_before),
                          dte+datetime.timedelta(hours=hours_after))
    # Throw out the ones already used in 20CRv3
    obs=obs[~obs['name'].isin(['ABERDEEN','VALENCIA','JERSEY','STOCKHOLM',
                               'LISBON','THEHELDER','HAPARANDA','MUNICH',
                               'BODO','HERNOSAND','WISBY','FANO','BERLIN'])]
    stations=obs.name.values.tolist()
    stations=list(OrderedDict.fromkeys(obs.name.values))
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
