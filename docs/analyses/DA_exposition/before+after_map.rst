:orphan:

Effect of assimilating observation at Fort William
==================================================

.. figure:: ../../../analyses/DA_exposition/place_to_place/before+after_map_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   :doc:`Spaghetti-contour plots <../spaghetti_contour/spaghetti_contour>` showing 20CRv3 MSLP fields before (left) and after (right) assimilating one Fort William observation (October 22nd, 1903 at 6pm).


|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/DA_exposition/place_to_place/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition/place_to_place/before+after_map.py

