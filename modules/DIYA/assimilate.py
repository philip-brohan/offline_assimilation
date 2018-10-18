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

#Functions to do EnKF-type data assimilation

import iris
import numpy
import sklearn.linear_model
import sklearn.utils
import IRData.utils

# X-matrix for the model is a numpy array of dimension
#  (n.ensemble.members,n.stations)
# With the pressures at each station location
# Use this same matrix to fir each gridpoint
def _build_X_matrix_from_cube(cube,latitudes,longitudes):
    locations = [('longitude', numpy.array(longitudes)),
                 ('latitude',  numpy.array(latitudes))]
    interpolated=cube.interpolate(locations,iris.analysis.Linear())
    if len(latitudes)>1:
        interpolated=IRData.utils.cube_order_dimensions(
                                             interpolated,('member',
                                            'latitude','longitude'))
    # This interpolates at each lat,lon pair - we only want the ith lat and ith lon
    result=numpy.diagonal(interpolated.data,axis1=1,axis2=2).copy()
    return result

# If the obs are at different times, we can't just use one cube.
# Need to load a cube at each obs time, and get the sub-matrix with obs at
# that time from that, and then merge them
# cube_function 
def _build_X_matrix_from_obs(obs,cube_function):
    # Find groups of obs made at the same time
    bunch=([[y for y in range(len(obs.dtm.values)) if obs.dtm.values[y]==x] 
                                                     for x in obs.dtm.values])
    bunch=[ele for ind, ele in enumerate(bunch) if ele not in bunch[:ind]]
    result=None # Don't know n.ensemble.members yet
    # For each bunch of contemporary obs, make a sub-matrix
    for subset in bunch:
        field=cube_function(obs.dtm.values[subset[0]])
        subX=_build_X_matrix_from_cube(field,obs.latitude.values[subset],
                                             obs.longitude.values[subset])
        if result is None:
            result=numpy.ndarray((subX.shape[0],len(obs)))
        result[:,subset]=subX
    return result

# Given a target cube, a function to load constraints, and a set of 
#  observations, make a constrained cube.
def constrain_cube(target,cube_function,obs,obs_error=0.1,
                   random_state=None,model=None,
                   lat_range=(-90,90),lon_range=(-180,360)):
    """Constrain the target at each gridpoint.

    Generates the constraints at each observation location, and then runs :func:`constrain_point` for each grid point in the target cube (inside the lat:lon ranges).

    Args:
        target (:obj:`iris.cube.Cube`): Ensemble to be constrained, must have dimensions 'member','latitude', and 'longitude'".
        cube_function (function taking a :obj:`numpy.datetime64` as argument, and returning an :obj:`iris.cube.Cube`): Resulting cube must have dimensions ('member','latitude','longitude')".
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude', 'longitude', and 'value', and value should have same units as constraints.
        obs_error (:obj:`float`): Uncertainty in each observation value (1 s.d.) . Units as obs.value.
        random_state (:obj:`int` | :obj:`numpy.random.RandomState`, optional): Set to produce exactly reproducible results.
        model (:obj:`sklearn.linear_model`, optional): Model to use to relate target to constraints. Defaults to :obj:`sklearn.linear_model.ElasticNet` with default parameters.
        lat_range (:obj:`list`, optional): Only do constraint in this range of latitudes.
        lon_range (:obj:`list`, optional): Only do constraint in this range of longitudes.

    Returns:
        :obj:`iris.cube.cube`: target, after applying constraints.

    |
    """
    X=_build_X_matrix_from_obs(obs,cube_function)
    Y=IRData.utils.cube_order_dimensions(
                 target,('member','latitude','longitude'))
    # Make a different set of perturbed obs for each ensemble member
    perturbed_obs=numpy.zeros([X.shape[0],len(obs.latitude)])
    random_state = sklearn.utils.check_random_state(random_state)
    for member in range(0,X.shape[0]):
        perturbed_obs[member,:]=obs.value+random_state.normal(
                                   loc=0,scale=obs_error,
                                   size=perturbed_obs.shape[1])
    if model is None: # Default model is Elastic Net Regression
        model=sklearn.linear_model.ElasticNet(alpha=1.0, l1_ratio=0.5,
                          fit_intercept=True,
                          normalize=False, 
                          precompute=False,
                          max_iter=1000, 
                          copy_X=False, 
                          tol=0.0001, 
                          warm_start=False, 
                          positive=False, 
                          random_state=random_state, 
                          selection='cyclic')
    grid_lats=Y.coord('latitude').points
    grid_lons=Y.coord('longitude').points
    for lat_i in range(0,Y.data.shape[1]):
        if grid_lats[lat_i]<lat_range[0] or grid_lats[lat_i]>lat_range[1]: continue
        for lon_i in range(0,Y.data.shape[2]):
            if lon_range[0]<lon_range[1]:
                if grid_lons[lon_i]<lon_range[0] or grid_lons[lon_i]>lon_range[1]: continue
            else:  # longitude wrap-around
                if grid_lons[lon_i]<lon_range[0] and grid_lons[lon_i]>lon_range[1]: continue
            y=Y[:,lat_i,lon_i].data
            Y.data[:,lat_i,lon_i]=constrain_point(y,X,model,perturbed_obs)
    return Y

# Constrain the ensemble at a selected point
def constrain_point(target,constraint,model,obs):
    """Constrain the target at a point

    Fit a model to the target given the constraint (t=m(c)+r). Then make a predicted ensemble using the observations in the fitted model, and the residuals to the fit (p=m(o)+r). If nE=number of ensemble members, and nP=number of observation points:

    Args:
        target (:obj:`numpy.array`): 1d array size nE - the target ensemble at the target point.
        constraint (:obj:`numpy.array`): 2d array size [nE,nP] - the constraint ensemble at each of the observation points.
        model (:obj:`sklearn.linear_model`): Model to fit.
        obs (:obj:`numpy.array`): 1d array size nP - the observations.

    Returns:
        :obj:`numpy.array`: 1d array size nE - the constrained target ensemble.

    |
    """

    fit=model.fit(constraint,target)
    residuals=target-fit.predict(constraint)
    predictions=fit.predict(obs)+residuals
    return predictions


