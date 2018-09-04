Validating 20CR2c against DWR data: February 1953 station scatterplot
=====================================================================

.. seealso:: 
    * :doc:`Video version <scatter_and_contour_video>`
    * :doc:`Full month scatter plot <scatter_month>`
    * :doc:`Error plot <reliability_and_error>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/scatter_and_contour>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/scatter_and_contour>`
    * :doc:`Same diagnostic but for October 1903 <../../October_1903/20CR2c/scatter_and_contour>`

.. figure:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/scatter+contour/Scatter+contour_1953021018.png
   :width: 650px
   :align: center
   :figwidth: 700px

   On the left: MSLP Contours for 20CR v2c, observations assimilated (yellow circles), DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher).

   On the right: MSLP observation (red line), and ensemble values (blue dots) at the location of each DWR station.

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/get_data.py

Script to make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/scatter+contour/scatter+contour.py

