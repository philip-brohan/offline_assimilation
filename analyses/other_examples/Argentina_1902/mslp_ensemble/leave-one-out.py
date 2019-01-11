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

import SEF
import glob
import DIYA
import sklearn
RANDOM_SEED = 5

# Try and get round thread errors on spice
import dask
dask.config.set(scheduler='single-threaded')

obs_error=5 # Pa
model=sklearn.linear_model.Lasso(normalize=True)
skip_stations=['DWR_Roca_Rio_N.','DWR_Sierra_Grnde',
               'DWR_Villa_Maria','DWR_Santo_Tome','DWR_Corrientes-C',
               'DWR_Santa_Fa-Cp','DWR_San_Lorenzo','DWR_Carcarana',
               'DWR_Estc_Pereyra','DWR_Puerto_Mili.']

opdir="%s/images/ADWR_jacknife" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Assimilate observations within this range of the field
hours_before=12
hours_after=12

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

# Get the DWR observations close to the selected time
ob_start=dte-datetime.timedelta(hours=hours_before)
ob_end=dte+datetime.timedelta(hours=hours_after)
adf=glob.glob('../../../../../station-data/ToDo/sef/Argentinian_DWR/1902/DWR_*_MSLP.tsv')
obs={'name': [], 'latitude': [], 'longitude': [], 'value' : [], 'dtm' : []}
for file in adf:
   stobs=SEF.read_file(file)
   df=stobs['Data']
   # Add the datetime
   df=df.assign(Hour=(df['HHMM']/100).astype(int))
   df=df.assign(Minute=(df['HHMM']%100).astype(int))
   df=df.assign(dtm=pandas.to_datetime(df[['Year','Month','Day','Hour','Minute']]))
   # Select the subset close to the selected time
   mslp=df[(df.dtm>=ob_start) & (df.dtm<ob_end)]
   if mslp.empty: continue
   if mslp['Value'].values[0]==mslp['Value'].values[0]:
       obs['name'].append(stobs['ID'])
       obs['latitude'].append(stobs['Lat'])
       obs['longitude'].append(stobs['Lon'])
       obs['value'].append(mslp['Value'].values[0])
       obs['dtm'].append(mslp['dtm'].values[0])
obs=pandas.DataFrame(obs)

# Throw out the suspected duds
obs=obs[~obs['name'].isin(skip_stations)]
# Throw out the specified station
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
                           lat_range=(-80,10),
                           lon_range=(250,350))

dumpfile="%s/%04d%02d%02d%02d.pkl" % (opdir,args.year,args.month,
                                      args.day,args.hour)
if args.omit is not None:
    dumpfile="%s/%04d%02d%02d%02d_%s.pkl" % (opdir,args.year,args.month,
                                             args.day,args.hour,args.omit)

pickle.dump( prmsl2, open( dumpfile, "wb" ) )
