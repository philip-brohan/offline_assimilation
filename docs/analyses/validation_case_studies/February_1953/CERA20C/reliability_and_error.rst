Validating CERA20C against DWR data: February 1953 station error plot
=====================================================================

.. seealso:: 
    * :doc:`Video version <reliability_and_error_video>`
    * :doc:`Full month error plot <error_v_error>`
    * :doc:`Scatter plot <scatter_and_contour>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/reliability_and_error>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/reliability_and_error>`
    * :doc:`Same diagnostic but in October 1903 <../../October_1903/CERA20C/reliability_and_error>`.

.. figure:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/reliability+error/reliability+error_1953021018.png
   :width: 650px
   :align: center
   :figwidth: 700px

   On the left: MSLP Contours for CERA20C, DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher.

   Top right: Scatter plot of ensemble-observation against observation at each DWR station.

   Bottom right: Scatter plot of ensemble standard deviation against ensemble-mean - observation.

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/get_data.py

Script to make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/CERA20C/reliability+error/reliability+error.py

