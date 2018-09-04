Validating 20CR3 against DWR data: February 1953 station error plot
===================================================================

.. seealso:: 
    * :doc:`Video version <reliability_and_error_video>`
    * :doc:`Full month error plot <error_v_error>`
    * :doc:`Scatter plot <scatter_and_contour>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/reliability_and_error>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/reliability_and_error>`
    * :doc:`Same diagnostic but for October 1903 <../../October_1903/20CR3/reliability_and_error>`

.. figure:: ../../../../../analyses/validation_case_studies/February_1953/20CRv3/reliability+error/reliability+error_1953021018.png
   :width: 650px
   :align: center
   :figwidth: 700px

   On the left: MSLP Contours for 20CRv3, observations assimilated (yellow circles), DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher.

   Top right: Scatter plot of ensemble-observation against observation at each DWR station.

   Bottom right: Scatter plot of ensemble standard deviation against ensemble-mean - observation.

|

Collect the reanalysis data:

.. note:: 20CRv3 has not yet been released, so the data retrieval script will currently work only for a privileged few.

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv3/get_data.py

Script to make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv3/reliability+error/reliability+error.py

