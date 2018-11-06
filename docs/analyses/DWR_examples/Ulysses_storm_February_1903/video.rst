:orphan:

DWR assimilation: Ulysses Storm of February 1903 video
======================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/297919245?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>Two reconstructions of the Ulysses storm of February 1903: mean-sea-level pressure (mslp) contours from the Twentieth Century Reanalysis version 3 (left), and after assimilating additional observations from the UK Daily Weather Reports (centre).</td></tr>
    </table>
    </center>

On the left, a :doc:`Spaghetti-contour plot <../../spaghetti_contour/spaghetti_contour>` of 20CRv3 MSLP. Centre and right, :doc:`Scatter-contour plot <../../scatter+contour/scatter_and_contour>` comparing the same field, after assimilating all 44 `DWR <https://oldweather.github.io/DWR/>`_ observations for that date. The centre panel shows the 20CRv3 ensemble after assimilating all 44 station observations (red dots). The right panel compares the two ensembles with the new observations: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location.

|

Code to make the figure
-----------------------

Collect the reanalysis data (prmsl ensemble and observations from 20CRv3 for February 1903):

.. literalinclude::  ../../../../analyses/DWR_examples/Ulysses_storm_Feb_1903/get_data.py

Script to calculate a leave-one-out assimilation for one station:

.. literalinclude:: ../../../../analyses/DWR_examples/Ulysses_storm_Feb_1903/video/leave-one-out.py

Calculate the leave-one-out assimilations for all the stations. (This script produces a list of calculations which can be done :doc:`in parallel <../../../tools/parallel>`):

.. literalinclude:: ../../../../analyses/DWR_examples/Ulysses_storm_Feb_1903/video/run_assimilations.py

Plot a single frame:

.. literalinclude:: ../../../../analyses/DWR_examples/Ulysses_storm_Feb_1903/video/plot_leave-one-out.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 7-minute period. (This script produces a list of calculations which can be done :doc:`in parallel <../../../tools/parallel>`)

.. literalinclude:: ../../../../analyses/DWR_examples/Ulysses_storm_Feb_1903/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i DWR_jacknife_png/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy DWR_assimilate.mp4
