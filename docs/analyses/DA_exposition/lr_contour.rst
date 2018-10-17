:orphan:

Linear relations
================

.. figure:: ../../../analyses/DA_exposition/place_to_place/lr+contour_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP at Fort William, Stornoway, and London (October 22nd, 1903 at 6pm).

   The left panel is a :doc:`Spaghetti-contour plot <../spaghetti_contour/spaghetti_contour>`, with the red dot marking Fort William, the blue Stornoway, and the black London. The right panels are scatter plots of the mslp values at this point in time, across the 80 members of the 20CRv3 ensemble, comparing the value at Fort William with that at Stornoway (top), and the value at Fort William with that at London (bottom).

|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/DA_exposition/place_to_place/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition/place_to_place/lr_contour.py

