Assimilating all the DWR observations
=====================================

.. figure:: ../../../analyses/DA_exposition/multiple_observations/Jacknife_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP. Centre and right, :doc:`Scatter-contour plot <../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating all 22 `DWR <https://oldweather.github.io/DWR/>`_ observations for that date. The centre panel shows the 20CRv3 ensemble after assimilating all 22 station observations (red dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for 1903):

.. literalinclude::  ../../../analyses/DA_exposition/multiple_observations/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition//multiple_observations/jacknife.py

