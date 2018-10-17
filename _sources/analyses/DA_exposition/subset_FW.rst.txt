:orphan:

Validation of assimilating an observation at Fort William
=========================================================

.. figure:: ../../../analyses/DA_exposition/multiple_observations/Subset_FW_only_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP. Centre and right, :doc:`Scatter-contour plot <../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating the Fort William observation, with all the other (independent) observations in the  `Daily Weather Reports <https://oldweather.github.io/DWR/>`_. The centre panel shows the 20CRv3 ensemble after assimilating the Fort William observation (red dot) and the locations of all other new stations with observations at the same time (black dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating the Fort William observation.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for 1903):

.. literalinclude::  ../../../analyses/DA_exposition/multiple_observations/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition//multiple_observations/subset_FW_only.py

