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
"""
Suppose you have an ensemble reanalysis, like `20CR <https://www.esrl.noaa.gov/psd/data/20thC_Rean/>`_. So you have 56 different estimates of the global mean-sea-level pressure field at a particular date (say, 1903-10-27:18). There is quite a lot of spread in this ensemble, the pressures are uncertain.

But we've also found a previously-unused observation, a measurement of MSLP at that time a a weather station (say in Fort William). We can use that new observation to improve the reanalysis estimate, with the `Ensemble Kalman Filter <https://www.esrl.noaa.gov/psd/data/20thC_Rean/>`_ or something similar.

This module does this. It takes reanalysis data and observations, and assimilates the observations into the reanalysis fields, making improved versions.

.. code-block:: python

    import DIYA
    new_field=DIYA.constrain_cube(old_field,old_field,obs)

|
"""

from assimilate import *
from qc import *
