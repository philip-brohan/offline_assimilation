Assimilating the Fort William pressures into 20CR2c video
=========================================================

.. raw:: html

    <center>
    <table><tr><td></center>
    <iframe src="https://player.vimeo.com/video/259167326?title=0&byline=0&portrait=0" width="795" height="447" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td>MSLP spaghetti-contour plot for 20CR2c (left), and after assimilating a single observation from Fort William (right) for the Ulysses storm: February 27th, 1903.</td></tr>
    </table>
    </center>

|

Collect the reanalysis data (prmsl ensemble and observations from 20CR2c for 1903):

.. literalinclude:: ../../../analyses/assimilating_Fort_William/video_20CR/get_data_20CR.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../../analyses/assimilating_Fort_William/video_20CR/add_FW_20CR.py

To make the video, it is necessary to run the script above about 400 times - giving an image for every 3-minute period in a day. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../../analyses/assimilating_Fort_William/video_20CR/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Add_FW_20CR/\*1903\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Add_FW_20CR.mp4
