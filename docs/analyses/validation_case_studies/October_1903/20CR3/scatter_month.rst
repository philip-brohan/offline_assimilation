Validating 20CR3 against DWR data: October 1903 monthly scatterplot
===================================================================

.. seealso:: 
    * :doc:`Error-error plot <error_v_error>`
    * :doc:`Breakdown by time <scatter_and_contour>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/scatter_month>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/scatter_month>`
    * :doc:`Same diagnostic but in February 1953 <../../February_1953/20CR3/scatter_month>`.

.. figure:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/month_summary/Scatter_month.png
   :width: 650px
   :align: center
   :figwidth: 700px

   Observed versus ensemble MSLP for each observation in the month

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/get_data.py

Extract the ensemble pressures at the space and time location of each observation

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/month_summary/get_comparison.py

Make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/month_summary/scatter_month.py


