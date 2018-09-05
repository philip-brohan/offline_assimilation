Visualising uncertainty: CERA20C spaghetti contours & DWR data
==============================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.cera20c.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.cera20c.png" width=795></a></center></td></tr>
    <tr><td>MSLP spaghetti-contour plot for 20CR2c (left), and comparison with DWR obs at the station locations (right) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

|

Collect the reanalysis data (prmsl ensemble from CERA20C for January 1901):

.. literalinclude:: ../../../analyses/scatter+contour/get_data_CERA.py

Script to make the figure:

.. literalinclude:: ../../../analyses/scatter+contour/scatter+contour.cera20c.py

