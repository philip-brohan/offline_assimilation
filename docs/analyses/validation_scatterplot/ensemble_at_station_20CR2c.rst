Compare DWR and 20CR2c reanalysis ensemble at station locations
===============================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_20CR_1901012218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_20CR_1901012218.png" width=500></a></center></td></tr>
    <tr><td>MSLP as observed at each DWR station (red line), as reconstructed by the 20CR2c ensemble at the station location (blue dots) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

|
    
Collect the data (prmsl ensemble from 20CR2c for 1901):

.. literalinclude:: ../../../analyses/validation_scatterplot/get_data_20CR.py

Script to make the figure:

.. literalinclude:: ../../../analyses/validation_scatterplot/validation_scatterplot.py
