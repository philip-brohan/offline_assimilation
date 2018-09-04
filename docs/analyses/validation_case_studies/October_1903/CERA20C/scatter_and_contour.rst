Validating CERA20C against DWR data: October 1903 station scatterplot
=====================================================================

.. seealso:: 
    * :doc:`Video version <scatter_and_contour_video>`
    * :doc:`Full month scatter plot <scatter_month>`
    * :doc:`Error plot <reliability_and_error>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/scatter_and_contour>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/scatter_and_contour>`
    * :doc:`Same diagnostic but in February 1953 <../../February_1953/CERA20C/scatter_and_contour>`.

.. figure:: ../../../../../analyses/validation_case_studies/October_1903/CERA20C/scatter+contour/Scatter+contour_1903102518.png
   :width: 650px
   :align: center
   :figwidth: 700px

   On the left: MSLP Contours for CERA20C, DWR observations not assimilated (circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher).

   On the right: MSLP observation (red line), and ensemble values (blue dots) at the location of each DWR station.

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/CERA20C/get_data.py

Script to make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/CERA20C/scatter+contour/scatter+contour.py

