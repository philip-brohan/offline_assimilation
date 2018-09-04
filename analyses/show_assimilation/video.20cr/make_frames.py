#!/usr/bin/env python

# Make all the individual frames for a movie
#  run the jobs on SPICE.

import os
import subprocess
import datetime

max_jobs_in_queue=500
# Where to put the output files
opdir="%s/slurm_output" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(count):
    op_file_name="%s/images/DWR/assimilate.20CRv3/Assimilated.20CRv3.%02d.%03d.png" % (
                 os.getenv('SCRATCH'),int(count),int((count-int(count))*100))
    if os.path.isfile(op_file_name):
        return True
    return False

count=0
while count<37.1:
    queued_jobs=subprocess.check_output('squeue --user hadpb',
                                         shell=True).count('\n')
    max_new_jobs=max_jobs_in_queue-queued_jobs
    while max_new_jobs>0 and count<37.1:
        f=open("multirun.slm","w+")
        f.write('#!/bin/ksh -l\n')
        f.write('#SBATCH --output=%s/slurm_output/as_20cr_frame_%d.out\n' %
                   (os.getenv('SCRATCH'),count))
        f.write('#SBATCH --qos=normal\n')
        f.write('#SBATCH --ntasks=4\n')
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=40000\n')
        f.write('#SBATCH --time=20\n')
        jcount=0
        for fraction in (0,0.025,0.05,0.075):
            if is_done(count+fraction):
                continue
            cmd="./assimilation_20cr.py --count=%f &\n" % (
                   count+fraction)
            f.write(cmd)
            jcount=jcount+1
        f.write('wait\n')
        f.close()
        if jcount>0:
            max_new_jobs=max_new_jobs-1
            rc=subprocess.call('sbatch multirun.slm',shell=True)
        os.unlink('multirun.slm')
        count=count+0.1
