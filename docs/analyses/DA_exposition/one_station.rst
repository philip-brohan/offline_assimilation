:orphan:

One station
===========

.. figure:: ../../../analyses/DA_exposition/one_station/With_FW_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP contours from 20CRv3 for October 22nd, 1903 (at 6pm), observations assimilated, yellow dots, and the location of a newly-digitised observation at Fort William (red dot).

|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CRv3 for October 1903):

.. literalinclude::  ../../../analyses//DA_exposition/one_station/get_data_20CR.py

The Fort William location and data are in the `Daily Weather Reports dataset <https://oldweather.github.io/DWR>`_.

Script to make the figure:

.. literalinclude:: ../../../analyses/DA_exposition/one_station/prmsl_20CR.py

