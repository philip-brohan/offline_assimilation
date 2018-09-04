Compare DWR and CERA20C reanalysis ensemble at station locations
================================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_CERA_1901012218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_CERA_1901012218.png" width=500></a></center></td></tr>
    <tr><td>MSLP as observed at each DWR station (red line), and as reconstructed by the CERA20C ensemble at the station location (blue dots) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

|

Collect the data (prmsl ensemble from CERA20C for January 1901):

.. literalinclude:: ../../../analyses/validation_scatterplot/get_data_CERA.py

Script to make the figure:

.. literalinclude:: ../../../analyses/validation_scatterplot/validation_scatterplot.cera20c.py
