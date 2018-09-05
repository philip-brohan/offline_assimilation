Making the logo - correlation map for a new observation
=======================================================

The sole purpose of this figure is to make a colourful and relevant image for use as the project logo.

.. figure:: ../../logo/logo.png
   :width: 75%
   :align: center
   :figwidth: 75%

   MSLP ensemble mean contours, and ensemble spread correlation with a hypothetical Fort William observation - from 20CRv2c.

The black lines are contours of the ensemble mean MSLP - at 1903:02:27:06, the time of the `Ulysses storm <https://weatherrescue.wordpress.com/2017/10/12/february-1903-the-ulysses-storm/>`_. The yellow dot marks the location of a hypothetical new observation, the coloured shading marKs regions where the ensemble spread is correlated (red) or anti-correlated (blue) with the spread at the observation location (in other words - the regions where assimilating such an observation would have a substantial effect). 

|

Collect the reanalysis data (prmsl ensemble from 20CR2c for 1903):

.. code-block:: python

   import datetime
   import IRData.twcr as twcr
   twcr.fetch('prmsl',datetime.datetime(1903,2,27),version='2c')
   
Script to make the figure:

.. literalinclude:: ../../logo/make_logo.py

Shrink the logo to a more convenient size

.. code-block:: bash

   convert -geometry 350x424 logo.png logo_small.png

