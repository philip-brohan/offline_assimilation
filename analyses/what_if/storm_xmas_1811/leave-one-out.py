#!/usr/bin/env python

# Make fake station observations for a set of locations
# Assimilate all but one station
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

import DIYA
import sklearn
RANDOM_SEED = 5

# Try and get round thread errors on spice
import dask
dask.config.set(scheduler='single-threaded')

obs_error=5 # Pa
model=sklearn.linear_model.Lasso(normalize=True)

opdir="%s/images/DWR_fake" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

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

# Fake the DWR observations for that time
obs=pandas.read_csv('stations.csv',header=None,
                    names=('name','latitude','longitude'))
obs=obs.assign(dtm=pandas.to_datetime(dte))
# Throw out the ones already used in 20CRv3
obs=obs[~obs['name'].isin(['Ylitornio','Paris','Turin','Geneva',
                           'Barcelona','Stockholm' ])]
# Also throw out the specified station
if args.omit is not None:
   obs=obs[~obs['name'].isin([args.omit])]
# Fill in the value for each ob from ens member 1
prmsl_r=prmsl.extract(iris.Constraint(member=1))
interpolator = iris.analysis.Linear().interpolator(prmsl_r, 
                                   ['latitude', 'longitude'])
value=numpy.zeros(len(obs))
for i in range(len(obs)):
    value[i]=interpolator([obs.latitude.values[i],
                           obs.longitude.values[i]]).data
# Add some simulated obs error - 100hPa normal
value=value+numpy.random.normal(loc=0.0, scale=100.0, size=len(value))
obs['value'] = pandas.Series(value, index=obs.index)

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
