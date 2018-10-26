:orphan:

DWR assimilation: Storm of March 1905
=====================================

.. seealso:: :doc:`Video version <video>`

.. figure:: ../../../../analyses/DWR_examples/storm_March_1905/Leave_one_out_1905031509.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP at 9 a.m. on March 15th 1905. Centre and right, :doc:`Scatter-contour plot <../../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating all 43 `DWR <https://oldweather.github.io/DWR/>`_ observations  within 8 hours of that date. The centre panel shows the 20CRv3 ensemble after assimilating all 43 station observations (red dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for 1905):

.. literalinclude::  ../../../../analyses/DWR_examples/storm_March_1905/get_data.py

Script to calculate a leave-one-out assimilation for one station:

.. literalinclude:: ../../../../analyses/DWR_examples/storm_March_1905/leave-one-out.py

Calculate the leave-one-out assimilations for all the stations:

.. literalinclude:: ../../../../analyses/DWR_examples/storm_March_1905/run_assimilations.py

Plot the figure:

.. literalinclude:: ../../../../analyses/DWR_examples/storm_March_1905/plot_leave-one-out.py

