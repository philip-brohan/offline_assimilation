:orphan:

Spaghetti contours
==================

.. figure:: ../../../analyses/representing_uncertainty/spaghetti_contour/spaghetti_example_1903102218.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP contours from 20CRv3 for October 22nd, 1903 (at 6pm), and observations assimilated.

This style of figure shows not only the best-estimate MSLP field (black contours), but also the uncertainty in that field. The blue lines are contours of MSLP for each of the 80 ensemble menbers in 20CRv3. Where the uncertainty is low these will cluster together (around the corresponding black contour) - where the blue contours diverge the uncertainty in the field is large.

The yellow dots show the observations assimilated into this field. It's the observations density that controls the quality of the field - more observations mean a lower uncertainty. (Though note that observations from earlier times (not shown) also matter). 

|

Code to make the figure
-----------------------

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude::  ../../../analyses/representing_uncertainty/spaghetti_contour/get_data.py

Script to make the figure:

.. literalinclude:: ../../../analyses/representing_uncertainty/spaghetti_contour/spv3.py

