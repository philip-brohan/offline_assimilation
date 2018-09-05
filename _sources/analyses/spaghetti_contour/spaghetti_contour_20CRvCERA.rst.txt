Spaghetti contours: 20CR v CERA
===============================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Compare_mslp_1903102218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Compare_mslp_1903102218.png" width=795></a></td></tr>
    <tr><td>MSLP Contours for 20CR2c (left), and CERA20C (right) for October 22nd, 1903 (at 6pm). Blue lines are contours from each of 10 ensemble members, black lines the contours of the ensemble mean (only shown where the ensemble spread is less than 3hPa). Yellow dots are observations asssimilated by 20CR, red dots are new observations now available from DWR (not assimilated in the reanalyses).</td></tr>
    </table>
    </center>

|

Collect the data (prmsl ensemble and observations from 20CR2c for 1903, prmsl ensemble for CERA20C for October 1903):

.. literalinclude:: ../../../analyses/spaghetti_contour/get_data_20CR.py

.. literalinclude:: ../../../analyses/spaghetti_contour/get_data_CERA.py

Script to make the figure:

.. literalinclude:: ../../../analyses/spaghetti_contour/compare_contours.py

