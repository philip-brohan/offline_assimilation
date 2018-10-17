:orphan:

Effect at Stornoway of assimilating observation at Fort William
===============================================================

.. figure:: ../../../analyses/DA_exposition/place_to_place/before+after_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP at Stornoway, before and after assimilating the Fort William observation.

    Scatter plots of 20CRv3 ensemble pressures at Stornoway against ensemble pressures at Fort William, at 6pm on 22nd October 1903. The Stornoway pressures are adjusted by fitting a linear regression (left plot) and then removing the fit from each value (right plot).

|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/DA_exposition/place_to_place/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition/place_to_place/before+after.py

