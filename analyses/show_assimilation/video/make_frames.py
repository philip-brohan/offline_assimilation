#!/usr/bin/env python

# Make all the individual frames for a movie
#  run the jobs on SPICE.

import os
import sys
import subprocess
import datetime

max_jobs_in_queue=500

# Where to put the output files
opdir="%s/images/DWR_jacknife_png" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(dte):
    op_file_name=('%s/Leave_one_out_%04d%02d%02d%02d%02d.png' % 
                             (opdir,dte.year,dte.month,dte.day,dte.hour,dte.minute))
    if os.path.isfile(op_file_name):
        return True
    return False

start_day=datetime.datetime(1905, 3, 15, 3)
end_day  =datetime.datetime(1905, 3, 16, 21)

dte=start_day
while dte<=end_day:
    queued_jobs=subprocess.check_output('squeue --user hadpb',
                                         shell=True).count('\n')
    max_new_jobs=max_jobs_in_queue-queued_jobs
    while max_new_jobs>0 and dte<=end_day:
        f=open("multirun.slm","w+")
        f.write('#!/bin/ksh -l\n')
        slopf="%04d%02d%02d%02d" % (dte.year,dte.month,dte.day,dte.hour)
        f.write('#SBATCH --output=%s/slurm_output/l_o_o_%s\n' % 
                                         (os.getenv('SCRATCH'),slopf))
        f.write('#SBATCH --qos=normal\n')
        f.write('#SBATCH --ntasks=4\n')
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=40000\n')
        f.write('#SBATCH --time=10\n')
        jcount=0
        for minutes in (0,7,15,23):
            if is_done(dte+datetime.timedelta(minutes=minutes)):
                continue
            cmd="./plot_leave-one-out.py --year=%d --month=%d --day=%d --hour=%f &\n" % (
                   dte.year,dte.month,dte.day,dte.hour+minutes/60.0)
            f.write(cmd)
            jcount=jcount+1
        f.write('wait\n')
        f.close()
        if jcount>0:
            max_new_jobs=max_new_jobs-1
            rc=subprocess.call('sbatch multirun.slm',shell=True)
        os.unlink('multirun.slm')
        dte=dte+datetime.timedelta(minutes=30)
