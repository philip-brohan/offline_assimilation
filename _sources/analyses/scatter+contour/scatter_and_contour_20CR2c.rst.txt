Visualising uncertainty: 20CR2c spaghetti contours & DWR data
=============================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.png" width=795></a></center></td></tr>
    <tr><td>MSLP spaghetti-contour plot for 20CR2c (left), and comparison with DWR obs at the station locations (right) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

|

Collect the reanalysis data (observations and prmsl ensemble from 20CR2c for 1901):

.. literalinclude:: ../../../analyses/scatter+contour/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/scatter+contour/scatter+contour.py

