:orphan:

What if: Storm of Christmas 1811
================================

.. warning::

   This is a hypothetical reconstruction using fake observations - it's not an accurate map of the weather of the period.

.. figure:: ../../../../analyses/what_if/storm_xmas_1811/Leave_one_out_1811122312.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP at noon on December 23rd 1811. Centre and right, :doc:`Scatter-contour plot <../../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating 44 fake observations at that date. The centre panel shows the 20CRv3 ensemble after assimilating all 44 fake observations (red dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location.

We know of 44 european stations making pressure observations in December 1811, but not available to 20CRv3 - these observations have not yet been rescued. To give some idea of how much the uncertainties in the reanalysis would reduce if these observations were available, we can assimilate a fake observation at each station. To make the fake observations, we took the mslp from ensemble member 1 of 20CRv3 at the location of each station, at the time of the field, and added a bit of noise (normaly distributed random with 1hPa standard deviation). Because the fake observations were all taken from the same ensemble member, they are mutually consistent, and can be collectively assimilated. But the resulting post-assimilation ensemble will be clustered around the ensemble member used, rather than the (unknown) real weather.

This weather map should give a reasonable estimate of the quality of reconstruction we could get if observations were rescued for all these stations, but it's not an accurate map of the actual weather at the time.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for 1811):

.. literalinclude::  ../../../../analyses/what_if/storm_xmas_1811/get_data.py

Script to calculate a leave-one-out assimilation for one station:

.. literalinclude:: ../../../../analyses/what_if/storm_xmas_1811/leave-one-out.py

Calculate the leave-one-out assimilations for all the stations: (This script produces a list of calculations which can be done :doc:`in parallel <../../../tools/parallel>`):

.. literalinclude:: ../../../../analyses/what_if/storm_xmas_1811/run_assimilations.py

Plot the figure:

.. literalinclude:: ../../../../analyses/what_if/storm_xmas_1811/plot_leave-one-out.py

