#!/usr/bin/env python

# Make all the individual frames for a movie

import os
import sys
import subprocess
import datetime

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

f=open("run.txt","w+")

start_day=datetime.datetime(1903, 2, 25,  3)
end_day  =datetime.datetime(1903, 2, 28, 21)

dte=start_day
while dte<=end_day:
    for minutes in (0,7,15,22):
        if is_done(dte+datetime.timedelta(minutes=minutes)):
            continue
        cmd="./plot_leave-one-out.py --year=%d --month=%d --day=%d --hour=%f &\n" % (
               dte.year,dte.month,dte.day,
               dte.hour+(dte.minute+minutes)/60.0)
        f.write(cmd)
    dte=dte+datetime.timedelta(minutes=30)
f.close()
