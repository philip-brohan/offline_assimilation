What this is, and why
=====================

This document is kept under version control in a `git repository <https://en.wikipedia.org/wiki/Git>`_. The repository is hosted on `GitHub <https://github.com/>`_ (and the documentation made with `GitHub Pages <https://pages.github.com/>`_). The repository is `<https://github.com/philip-brohan/offline_assimilation>`_. This repository contains everything you need to reproduce or extend this work, but note that the 20CRv3 data is still preliminary, and access to it is currently restricted.

If you are familiar with GitHub, you already know `what to do <https://github.com/philip-brohan/offline_assimilation>`_: If you'd prefer not to bother with that, you can download the whole dataset as `a zip file <https://github.com/philip-brohan/offline_assimilation/archive/master.zip>`_.

To re-run the scripts included, first install three packages this depends on:

- `IRData <http://brohan.org/IRData/>`_ which provides access to the reanalysis data used,
- `Meteographica <https://brohan.org/Meteorographica/>`_ for plotting weather maps,
- `The DWR dataset <https://oldweather.github.io/DWR/>`_ containing the newly-digitised British Isles observations.

Then install the libraries included in this package:

.. code-block:: sh

   python setup.py install --user

Each diagnostic contains code to download the reanalysis data required. For 20CR2c and CERA-20C data this process is straighforward, but for the preliminary 20CRv3 data it is more complicated. Please read carefully the :doc:`instructions on access to 20CRv3 data <extract_data/extract_data>` and the `instructions on using the IRData module with 20CRv3 <http://brohan.org/IRData/subdata/data_20CR.html#pre-release-version-3>`_.

If you reuse this, please let me know, by `raising an issue <https://github.com/philip-brohan/offline_assimilation/issues/new>`_. You are not obliged to do this, but it would help.

~                                                                                             
