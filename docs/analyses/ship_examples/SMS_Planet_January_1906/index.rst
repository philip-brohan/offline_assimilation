:orphan:

Ship observation assimilation: SMS Planet in January 1906
=========================================================

.. figure:: ../../../../analyses/Ship_examples/SMS_planet_1906/Planet_1906012409.png
   :width: 95%
   :align: center
   :figwidth: 95%

   On the left, a :doc:`Spaghetti-contour plot <../../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP at 9 a.m. on January 24th 1906. Centre and right, :doc:`Scatter-contour plot <../../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating the `SMS Planet <https://oldweather.github.io/Expeditions/ToDo/voyages/Planet_1906-7/Planet.html>`_ observations  within 4 hours of that date. The centre panel shows the 20CRv3 ensemble after assimilating the ship observations (red dots), and also `DWR stations <https://oldweather.github.io/DWR/>`_ for the same date (here used for validation and not assimilated). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures at the validation stations, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating the ship observations.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for 1906):

.. literalinclude::  ../../../../analyses/Ship_examples/SMS_planet_1906/get_data.py

Plot the figure:

.. literalinclude:: ../../../../analyses/Ship_examples/SMS_planet_1906/Planet_v_DWR.py

