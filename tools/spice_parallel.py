#!/usr/bin/env python

# Run a list of jobs on SPICE.
# Similar to Gnu parallel, except it uses SPICE

import os
import sys
import subprocess
import datetime
import time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--maxjobs", help="Max no. of jobs to queue",
                    default=500,
                    type=int,required=False)
parser.add_argument("--output", help="Sub-directory for slurm output",
                    default=None,
                    type=str,required=False)
parser.add_argument("--qos", help="Quality-of-service (high, normal, low)",
                    default='normal',
                    type=str,required=False)
parser.add_argument("--ntasks", help="Number of cores to assign",
                    default=1,
                    type=int,required=False)
parser.add_argument("--mem", help="RAM required (Mb)",
                    default=10000,
                    type=int,required=False)
parser.add_argument("--time", help="Max time per job (minutes)",
                    type=int,required=True)
args = parser.parse_args()

if args.qos not in ('high','normal','low'):
   raise ValueError("QOS must be 'normal', 'high', or 'low'")

# Make the script output directory
slopdir="%s/slurm_output/" % os.getenv('SCRATCH')
if args.output is not None:
    slopdir="%s/%s" % (slopdir,args.output)
if not os.path.isdir(slopdir):
    os.makedirs(slopdir)

jobs = sys.stdin.readlines()

i=0
while i<len(jobs):
    queued_jobs=subprocess.check_output('squeue --user hadpb',
                                         shell=True,
                                         universal_newlines=True).count('\n')
    max_new_jobs=args.maxjobs-queued_jobs
    for j in range(i,min(len(jobs),i+max_new_jobs)):
        f=open("run.slm","w+")
        f.write('#!/bin/ksh -l\n')
        f.write('#SBATCH --output=%s/%d.out\n' % 
                                         (slopdir,j))
        f.write('#SBATCH --qos=%s\n' % args.qos)
        f.write('#SBATCH --ntasks=%d\n' % args.ntasks)
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=%d\n' % args.mem)
        f.write('#SBATCH --time=%d\n' % args.time)
        f.write(jobs[j])
        f.close()
        rc=subprocess.call('sbatch run.slm',shell=True)
        os.unlink('run.slm')
    if max_new_jobs>0: i = i+max_new_jobs
    if i<len(jobs): time.sleep(30)
