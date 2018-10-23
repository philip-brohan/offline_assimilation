#!/usr/bin/env python

# Assimilate all but one station for a given date
#   and store the resulting field.

import os
import math
import datetime
import numpy
import pandas
import pickle

import iris
import iris.analysis

import IRData.twcr as twcr

import DWR
import DIYA
import sklearn
RANDOM_SEED = 5

obs_error=5 # Pa
model=sklearn.linear_model.Lasso(normalize=True)

opdir="%s/images/DWR_jacknife" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Assimilate observations within this range of the field
hours_before=6
hours_after=6

# Get the datetime, and station to omit, from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Time of day (0,3,6,9,12,18,or 21)",
                    type=int,required=True)
parser.add_argument("--omit", help="Name of station to be left out",
                    default=None,
                    type=str,required=False)
args = parser.parse_args()

dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# 20CRv3 data
prmsl=twcr.load('prmsl',dte,version='4.5.1')

# Get the DWR observations for that afternoon
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=hours_before),
                          dte+datetime.timedelta(hours=hours_after))

# Throw out the ones already used in 20CRv3
obs=obs[~obs['name'].isin(['ABERDEEN','VALENCIA','JERSEY','STOCKHOLM',
                           'LISBON','THEHELDER','HAPARANDA','MUNICH',
                           'BODO','HERNOSAND','WISBY','FANO','BERLIN'])]
# Also throw out the specified station
if args.omit is not None:
   obs=obs[~obs['name'].isin([args.omit])]

# Convert to normalised value same as reanalysis
obs.value=obs.value*100

# Update mslp by assimilating all obs.
prmsl2=DIYA.constrain_cube(prmsl,
                           lambda dte: twcr.load('prmsl',dte,version='4.5.1'),
                           obs=obs,
                           obs_error=obs_error,
                           random_state=RANDOM_SEED,
                           model=model,
                           lat_range=(20,85),
                           lon_range=(280,60))

dumpfile="%s/%04d%02d%02d%02d.pkl" % (opdir,args.year,args.month,
                                      args.day,args.hour)
if args.omit is not None:
    dumpfile="%s/%04d%02d%02d%02d_%s.pkl" % (opdir,args.year,args.month,
                                             args.day,args.hour,args.omit)

pickle.dump( prmsl2, open( dumpfile, "wb" ) )
