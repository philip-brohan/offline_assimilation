Validating 20CR2c against DWR data: February 1953 monthly scatterplot
=====================================================================

.. seealso:: 
    * :doc:`Error-error plot <error_v_error>`
    * :doc:`Breakdown by time <scatter_and_contour>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/scatter_month>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/scatter_month>`
    * :doc:`Same diagnostic but in October 1903 <../../October_1903/20CR2c/scatter_month>`.

.. figure:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/month_summary/Scatter_month.png
   :width: 650px
   :align: center
   :figwidth: 700px

   Observed versus ensemble MSLP for each observation in the month

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/get_data.py

Extract the ensemble pressures at the space and time location of each observation

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/month_summary/get_comparison.py

Make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv2c/month_summary/scatter_month.py


