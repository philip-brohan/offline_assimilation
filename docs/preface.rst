How to replicate or extend this
===============================

This document is kept under version control in a `git repository <https://en.wikipedia.org/wiki/Git>`_. The repository is hosted on `GitHub <https://github.com/>`_ (and the documentation made with `GitHub Pages <https://pages.github.com/>`_). The repository is `<https://github.com/philip-brohan/offline_assimilation>`_. This repository contains everything you need to reproduce or extend this work, but note that the 20CRv3 data is still preliminary, and access to it is currently restricted.

If you are familiar with GitHub, you already know `what to do <https://github.com/philip-brohan/offline_assimilation>`_: If you'd prefer not to bother with that, you can download the whole dataset as `a zip file <https://github.com/philip-brohan/offline_assimilation/archive/master.zip>`_.

All the code included is writen in Python (version 3.6). I strongly recommend running it in a `conda environment <https://conda.io/docs/>`_ - which greatly simplifies getting the necessary dependencies. The code is known to work on Linux and OSX, I've not tried it on anything else.

To re-run the scripts included, first install four packages this depends on:

- `IRData <http://brohan.org/IRData/>`_ which provides access to the reanalysis data used,
- `Meteographica <https://brohan.org/Meteorographica/>`_ for plotting weather maps,
- `The Python IMMA library <http://brohan.org/pyIMMA/>`_ for access to marine observations.
- `The DWR dataset <https://oldweather.github.io/DWR/>`_ containing the newly-digitised British Isles observations.

Then install the libraries included in this package:

.. code-block:: sh

   python setup.py install --user

Each diagnostic contains code to download the reanalysis data required. While 20CRv3 data is still preliminary, this process is complicated. Please read carefully the `instructions on access to 20CRv3 data <https://oldweather.github.io/20CRv3-diagnostics/extract_data/extract_data.html>`_ and the `instructions on using the IRData module with 20CRv3 <http://brohan.org/IRData/subdata/data_20CR.html#pre-release-version-3>`_.

If you reuse this, please let me know, by `raising an issue <https://github.com/philip-brohan/offline_assimilation/issues/new>`_. You are not obliged to do this, but it would help.
            
