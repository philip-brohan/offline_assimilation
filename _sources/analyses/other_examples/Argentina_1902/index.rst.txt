DWR assimilation: Argentine cold surge of August 1902
=====================================================

This case-study shows the effect of using `observations from the Argentine Daily Weather Reports <http://brohan.org/station-data/sources/Argentine_DWR/index.html>`_, newy digitised through the `Copernicus C3S Data Rescue Service <https://climate.copernicus.eu/data-rescue-service>`_, to improve the reconstruction of the 1902 cold-surge which badly damaged the South American Coffee plantations.

.. seealso:: :doc:`Video version <video>`

.. figure:: ../../../../analyses/other_examples/Argentina_1902/mslp_ensemble/Leave_one_out_190208171800.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP at 6 p.m. on August 17th 1902. Centre and right, :doc:`Scatter-contour plot <../../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating all the `Argentine DWR station pressure observations <http://brohan.org/station-data/sources/Argentine_DWR/index.html>`_  within 1 hour of that date. The centre panel shows the 20CRv3 ensemble after assimilating all the station observations (red dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for February 1903):

.. literalinclude::  ../../../../analyses/other_examples/Argentina_1902/mslp_ensemble/get_data.py

Script to calculate a leave-one-out assimilation for one station:

.. literalinclude:: ../../../../analyses/other_examples/Argentina_1902/mslp_ensemble/leave-one-out.py

Calculate the leave-one-out assimilations for all the stations. (This script produces a list of calculations which can be done :doc:`in parallel <../../../tools/parallel>`):

.. literalinclude:: ../../../../analyses/other_examples/Argentina_1902/mslp_ensemble/run_assimilations.py

Plot the figure:

.. literalinclude:: ../../../../analyses/other_examples/Argentina_1902/mslp_ensemble/plot_leave-one-out.py

