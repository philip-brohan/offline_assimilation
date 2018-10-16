Scatter-contour plot
====================

.. figure:: ../../../analyses/representing_uncertainty/scatter_contour/Scatter+contour_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`spaghetti-contour plot <../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP for October 22nd, 1903 (at 6pm). On the right, comparison of the ensemble values (blue dots), with independent observations from the `Daily Weather Reports <https://oldweather.github.io/DWR/>`_ (black lines).

This style of figure validates the reanalysis ensemble by comparing ensemble values at the times and places where we have independent observations, with the independent observations. The reanalysis is well-calibrated if the observation values mostly lie within the cloud of ensemble values, and precise if the ensemble spread around the observation value is small.

|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/representing_uncertainty/scatter_contour/get_data.py

Script to make the figure:

.. literalinclude:: ../../../analyses/representing_uncertainty/scatter_contour/scatter_contour.py

