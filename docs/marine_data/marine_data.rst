Improving 20CR with ship observations
=====================================

We can assimilate ship observations in exactly the same way as station observations. We expect ship records to be in `IMMA <http://brohan.org/pyIMMA/>`_ format.

I don't have a cluster of ship observations which are not already in 20CRv3 to provide validation for each other as we did with the :doc:`DWR observations <../DWR_data/DWR_data>`. So instead the example is a single ship leaving Germany in January 1906 - `SMS Planet <https://oldweather.github.io/Expeditions/ToDo/voyages/Planet_1906-7/Planet.html>`_. We can assimilate the observations from the ship, and validate them against :doc:`DWR observations <../DWR_data/DWR_data>` for the same date.

.. figure:: ../../analyses/Ship_examples/SMS_planet_1906/Planet_1906012409.png
   :width: 95%
   :align: center
   :figwidth: 95%

On the left, a :doc:`Spaghetti-contour plot <../analyses/spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP at 9 a.m. on January 24th 1906. Centre and right, :doc:`Scatter-contour plot <../analyses/scatter+contour/scatter_and_contour>` comparing the same field, after assimilating the `SMS Planet <https://oldweather.github.io/Expeditions/ToDo/voyages/Planet_1906-7/Planet.html>`_ observations within 4 hours of that date. The centre panel shows the 20CRv3 ensemble after assimilating the ship observations (red dots), and also `DWR stations <https://oldweather.github.io/DWR/>`_ for the same date (here used for validation and not assimilated). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures at the validation stations, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating the ship observations. (:doc:`Figure source <../analyses/ship_examples/SMS_Planet_January_1906/index>`).



