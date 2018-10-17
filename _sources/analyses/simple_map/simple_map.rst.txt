:orphan:

Simple weather map
==================

.. figure:: ../../../analyses/representing_uncertainty/pressure_map/simple_map_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP contours from the first ensemble member of 20CRv3 for October 22nd, 1903 (at 6pm), and observations assimilated.

This is a simple weather map - shows only mean-sea-level pressure (MSLP). This is a single estimate of the MSLP field.

The yellow dots show the observations assimilated into this field.
|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/representing_uncertainty/pressure_map/get_data.py

Script to make the figure:

.. literalinclude:: ../../../analyses/representing_uncertainty/pressure_map/simple_map.py

