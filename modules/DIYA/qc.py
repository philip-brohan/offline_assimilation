# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

# Replicate the 20CR2c observations quality control

import math
import iris
import numpy
import pandas
import datetime
import IRData.twcr as twcr

def qc_plausible_range(obs,min=880.0,max=1060.0):
    """Checks the obs value for plausibility.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have column 'value', and value should have same units as max and min.
        min (:obj:`float`): Minimum plausible value, defaults to 880.
        max (:obj:`float`): Maximum plausible value, defaults to 1060.

    Returns:
        (:obj:`pandas.Series`): True where obs['value' between min and max, False otherwise.

    |
    """

    plausible = (obs['value']>=min) & (obs['value']<=max)
    return plausible

def qc_compare_reanalysis(obs,variable='prmsl',version='2c'):
    """Get 20CR ensemble values at the time and place of each observation.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude', 'longitude', and 'dtm' - the last a datetime.datetime.
        variable (:obj:`str`): Which 20CR variable to compare to. Defaults to 'prmsl'
        version (:obj:`str`): Which 20CR version to load data from. Defaults to '2c'

    Returns
        :obj:`pandas.Series`: Reanalyis ensemble associated with each observation.

    |
    """

    old_idx=obs.index
    obs=obs.reset_index() # index values 0-n
    ob_times=obs['dtm'].unique()
    results=[None]*len(obs)
    for ob_time in ob_times:
        ot=pandas.to_datetime(ob_time)
        ensemble=twcr.load(variable,ot,version=version)
        # Units hack - assumes obs in hPa (if prmsl)
        if variable=='prmsl': 
            ensemble.data=ensemble.data/100.0 # to hPa
        interpolator = iris.analysis.Linear().interpolator(ensemble, 
                                       ['latitude', 'longitude'])
        this_time=obs['dtm'][obs['dtm']==ob_time].index
        for ob_idx in this_time:
            ensemble=interpolator([obs.latitude[ob_idx],obs.longitude[ob_idx]])
            results[ob_idx]=ensemble.data

    return pandas.Series(results,index=old_idx)

def qc_first_guess(obs,nsd=3,osd=2,comparison=None,variable='prmsl',version='2c'):
    """Checks the obs value against the 20CR ensemble.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude', 'longitude', 'value', and 'dtm' - the last a datetime.datetime.
        nsd (:obj:`float`): Number of standard deviations for rejection threshold. Defaults to 3.
        osd (:obj:`float`): Observation standard deviation. Defaults to 2.
        comparison (:obj:`pandas.Series`): Reanalysis ensemble values at the time and place of each observation. Defaults to None - calculate them.
        variable (:obj:`str`): Which 20CR variable to compare to. Defaults to 'prmsl'
        version (:obj:`str`): Which 20CR version to load data from. Defaults to '2c'

    For each observation, loads the 20CR ensemble at the time of observation, extracts the mean and standard deviation at the time and place of observation, and compares ob-ensemble mean with the expected difference given the ensemble spread and observation error sqrt(ensemble sd**2 + osd**2). If the observed difference is greater than nsd times the expected difference, mark ob with false, otherwise with true.

    Returns:
        (:obj:`pandas.Series`): True where ob-ensemble mean within expected difference from 20CR spread, False otherwise.

    |
    """

    results=[None]*len(obs)

    if comparison is None:
        comparison=qc_compare_reanalysis(obs,variable=variable,version=version)

    for idx in range(len(obs)):
        ens_mean  = numpy.mean(comparison.values[idx])
        ens_sd    = numpy.std(comparison.values[idx],ddof=1)
        expected  = numpy.sqrt(osd**2+ens_sd**2)
        deviation = abs(obs.value.values[idx]-ens_mean)
        if (deviation/expected)<nsd:
            results[idx]=True
        else:
            results[idx]=False

    return pandas.Series(results,index=obs.index)
    
        
# Analagous to DWR.at_station_and_time, but gets QC status instead of value
def qc_at_station_and_time(obs,station,dte):
    """Get, from these observations, the quality of value at the selected station and time.

    This is analagous to :func:`DWR.at_station_and_time` except it gets the QC status of the observation instead of its value. If the value is interpolated, it will fail QC if either of the values it's interpolated from fails.

    Args:
        obs (:obj:`pandas.DataFrame`): Batch of observations for the period around the desired time. Should have extra columns 'plausible' and 'first_guess', giving results of those QC checks.
        station (:obj:`str`): Name of station, as used in obs.name.
        dte (:obj:`datetime.datetime`): Time of required observed value.

    Returns:
        :obj:`bool`: True if this selected data has passed QC checks.


    Raises:
        StandardError: obs does not contain at least two values for selected station, one before and one after specified time. So interpolation not possible.

    |
    """
    quality=True
    at_station=obs.loc[obs['name']==station]
    if at_station.empty:
        raise StandardError('No data for station %s' % station)
    at_station=at_station.sort_values(by='dtm',ascending=True)
    hit=at_station.loc[at_station['dtm']==dte]
    if not hit.empty:
        hit=hit.iloc[0]
        if 'plausible' in hit: 
            quality=quality & hit['plausible']
        if 'first_guess' in hit: 
            quality=quality & hit['first_guess']
        return quality
    before=at_station.loc[at_station['dtm']<dte]
    if before.empty:
        raise StandardError('No data for station %s before %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    before=before.iloc[-1] # last row
    if 'plausible' in before: 
        quality=quality & before['plausible']
    if 'first_guess' in before: 
        quality=quality & before['first_guess']
    after=at_station.loc[at_station['dtm']>dte]
    if after.empty:
        raise StandardError('No data for station %s after %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    after=after.iloc[0] # first row
    if 'plausible' in after: 
        quality=quality & after['plausible']
    if 'first_guess' in after: 
        quality=quality & after['first_guess']
    return quality


def haversine(origin, destination):
    """Calculate distance between two observations.

    Args:
        origin (:obj:`pandas.DataFrame`): 1 row from an observations dataframe. Must have columns 'latitude' and 'longitude'.
        destination (:obj:`pandas.DataFrame`): 1 row from an observations dataframe. Must have columns 'latitude' and 'longitude'.

    Returns:
        :obj:`float`: Distance between origin and destination in km.

    |
    """

    dlat = math.radians(origin.latitude-destination.latitude)
    dlon = math.radians(origin.longitude-destination.longitude)
    a = math.sin(dlat/2) * math.sin(dlat/2) + \
              math.cos(math.radians(origin.latitude)) \
        * math.cos(math.radians(destination.latitude)) \
        * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = 6371 * c # Earth radius in km

    return d

def nearby_observations(observations,target,distance):
    """Find the subset of observations within a given distance of a target.

    Args:
        observations (:obj:`pandas.DataFrame`): Observations dataframe. Must have columns 'latitude' and 'longitude'.
        target (:obj:`pandas.DataFrame`): 1 row from an observations dataframe. Must have columns 'latitude' and 'longitude'.
        distance (:obj:`float`): Maximum distance (km).

    Returns:
        (:obj:`pandas.DataFrame`): Observations dataframe. Same as 'observations' input except that it only contains rows less than 'distance' from 'target'.

    |
    """

    selected=[]
    for idx in range(len(observations)):
        if haversine(target,observations.iloc[idx])<distance:
            selected.append(idx)
    return observations.iloc[selected]

def buddy_check(obs,field,obs_error=0.1,
                   random_state=None,model=None,
                   lat_range=(-90,90),lon_range=(-180,360)):
    """Checks the influence of assimilating each ob on its neighbours.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude', 'longitude', 'value', and 'dtm' - the last a datetime.datetime.
       field (:obj:`iris.Cube.cube`): Reanalysis ensemble field to assimilate to - dimensions lat, lon, ensemble.

    For each observation, assimilate into the field provided, then compare all the other observations to the field both before and after assimilation. For each ob, return the ratio of this mean difference with::without assimilation (<1 is good, observation improves fit to buddies, >1 is bad, degrades fit).

    Returns:
        (:obj:`pandas.Series`):  Mean difference ratio from assimilating each observation.

    |
    """

    results=[None]*len(obs)

    # Mean difference for each ob without assimilation
    e_o=[None]*len(obs)
    interpolator = iris.analysis.Linear().interpolator(field, 
                                   ['latitude', 'longitude'])
    for idx in range(len(obs)):
        ensemble=interpolator([obs.latitude[idx],obs.longitude[idx]])
        e_o[idx]=obs.value[idx]-numpy.mean(ensemble.data)

    # Effect of assimilating each ob
    for idx in range(len(obs)):
        new_field=DIYA.constrain_cube(field,field,obs.iloc[idx],
                                      obs_error=obs_error,
                                      random_state=random_state,
                                      model=model,
                                      lat_range=lat_range,
                                      lon_range=lon_range)

        interpolator = iris.analysis.Linear().interpolator(new_field, 
                                       ['latitude', 'longitude'])
        ms_o=0
        ms_n=0
        for id2 in range(len(obs)):
            if id2==idx: continue
            ms_o = ms_o + e_o[id2]**2
            ensemble=interpolator([obs.latitude[id2],obs.longitude[id2]])
            ms_n = ms_n + (obs.value[id2]-numpy.mean(ensemble.data))**2
        results[idx] = ms_n/ms_o

    return pandas.Series(results,index=obs.index)
