#!/usr/bin/env python

# Do all the jacknife assimilations for a range of times

import os
import sys
import time
import subprocess
import datetime
import DWR

max_jobs_in_queue=500

# Assimilate observations within this range of the field
hours_before=6
hours_after=6

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

start_day=datetime.datetime(1905, 3, 10,  3)
end_day  =datetime.datetime(1905, 3, 20, 21)

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
    stations.append(None) # Also do case with all stations

    # Don't put too many jobs in the queue at once
    free_jobs=max_jobs_in_queue-subprocess.check_output('squeue --user hadpb',
                                             shell=True).count('\n')
    while free_jobs<len(stations):
        time.sleep(30)
        free_jobs=max_jobs_in_queue-subprocess.check_output('squeue --user hadpb',
                                             shell=True).count('\n')

    for station in stations:

        if is_done(dte,station): continue

        f=open("run.slm","w+")
        f.write('#!/bin/ksh -l\n')
        slopf="%04d%02d%02d%02d" % (dte.year,dte.month,dte.day,dte.hour)
        if station is not None: slopf="%s_%s" % (slopf,station)
        f.write('#SBATCH --output=%s/slurm_output/jacknife_%s\n' % 
                                         (os.getenv('SCRATCH'),slopf))
        f.write('#SBATCH --qos=normal\n')
        f.write('#SBATCH --ntasks=1\n')
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=10000\n')
        f.write('#SBATCH --time=10\n')
        cmd="./leave-one-out.py --year=%d --month=%d --day=%d --hour=%d" % (
                  dte.year,dte.month,dte.day,dte.hour)
        if station is not None:
            cmd="%s --omit=%s" % (cmd,station)
        cmd="%s\n" % cmd
        f.write(cmd)
        f.close()
        rc=subprocess.call('sbatch run.slm',shell=True)
        #sys.exit()
        os.unlink('run.slm')
    dte=dte+datetime.timedelta(hours=3)
