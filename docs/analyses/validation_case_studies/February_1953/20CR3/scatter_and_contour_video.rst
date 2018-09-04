Validating 20CR3 against DWR data: February 1953 station scatterplot video
==========================================================================

.. seealso:: 
    * :doc:`Static version <scatter_and_contour>`
    * :doc:`Error plot <reliability_and_error_video>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/scatter_and_contour_video>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/scatter_and_contour_video>`
    * :doc:`Same diagnostic but for October 1903 <../../October_1903/20CR3/scatter_and_contour_video>`

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/267264064?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td>On the left: MSLP Contours for 20CRv3, observations assimilated (yellow circles), DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher).<p>
   On the right: MSLP observation (red line), and ensemble values (blue dots) at the location of each DWR station.</center></td></tr>
    </table>
    </center>

|

Collect the reanalysis data:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv3/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../../../../analyses/validation_case_studies/February_1953/20CRv3/scatter+contour/video/scatter+contour.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Scatter_and_contour/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Scatter_and_contour.mp4

