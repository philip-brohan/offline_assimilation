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

start_day=datetime.datetime(1903, 02, 27,  0)
end_day  =datetime.datetime(1903, 02, 28,  0)

# Function to check if the job is already done for this timepoint
def is_done(year,month,day,hour):
    op_file_name=("%s/images/DWR/Add_FW_20CR/" +
                  "Add_FW_%04d%02d%02d%02d%02d.png") % (
                            os.getenv('SCRATCH'),
                            year,month,day,int(hour),
                                        int(hour%1*60))
    if os.path.isfile(op_file_name):
        return True
    return False

current_day=start_day
while current_day<=end_day:
    queued_jobs=subprocess.check_output('squeue --user hadpb',
                                         shell=True).count('\n')
    max_new_jobs=max_jobs_in_queue-queued_jobs
    while max_new_jobs>0 and current_day<=end_day:
        f=open("multirun.slm","w+")
        f.write('#!/bin/ksh -l\n')
        f.write('#SBATCH --output=%s/Add_FW_20CR_%04d%02d%02d%02d.out\n' %
                   (opdir,
                    current_day.year,current_day.month,
                    current_day.day,current_day.hour))
        f.write('#SBATCH --qos=normal\n')
        f.write('#SBATCH --ntasks=4\n')
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=40000\n')
        f.write('#SBATCH --time=10\n')
        count=0
        for fraction in (0,.25/4,.5/4,.75/4):
            if is_done(current_day.year,current_day.month,
                       current_day.day,
                       current_day.hour+current_day.minute/60.0+fraction):
                continue
            cmd=("./add_FW_20CR.py --year=%d --month=%d" +
                " --day=%d --hour=%f &\n") % (
                   current_day.year,current_day.month,
                   current_day.day,
                   current_day.hour+current_day.minute/60.0+fraction)
            f.write(cmd)
            count=count+1
        f.write('wait\n')
        f.close()
        current_day=current_day+datetime.timedelta(hours=0.25)
        if count>0:
            max_new_jobs=max_new_jobs-1
            rc=subprocess.call('sbatch multirun.slm',shell=True)
        os.unlink('multirun.slm')
