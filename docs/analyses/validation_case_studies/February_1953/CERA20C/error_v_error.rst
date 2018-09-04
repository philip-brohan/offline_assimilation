Validating CERA20C against DWR data: February 1953 error-error plot
===================================================================

.. seealso:: 
    * :doc:`Month scatter plot <scatter_month>`
    * :doc:`Breakdown by time <reliability_and_error>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/error_v_error>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/error_v_error>`
    * :doc:`Same diagnostic but in October 1903 <../../October_1903/CERA20C/error_v_error>`.

.. figure:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/month_summary/E_v_E.png
   :width: 650px
   :align: center
   :figwidth: 700px

   Observation minus ensemble mean RMS, as a function of ensemble standard deviation, over the times and places where there are observations. The three grey lines show the expected relationship, if the reanalysis spread is correctly calibrated, assuming observation errors of 0, 1, and 2 hPa.

|

If the reanalysis spread is correct and the observations are perfect, then the expected value of observation-ensemble mean is equal to the reanalysis standard deviation. If the observations are not perfect, the expected value of observation-ensemble mean is given by adding the observation error standard deviation to the reanalysis standard deviation in quadrature.

So to make this plot, find all the points where there are observations and the reanalysis standard deviation is about 1hPa, and calculate the RMS observation-ensemble mean for those points. That's one dot, repeat for other values of reanalysis standard deviation. The dots should follow the grey lines. If the dots are below the grey lines the reanalysis is underconfident (too much spread), if they are above the grey lines it is overconfident (too little spread).

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/get_data.py

Extract the ensemble pressures at the space and time location of each observation

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/month_summary/get_comparison.py

Make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/month_summary/rms_v_rms.py


