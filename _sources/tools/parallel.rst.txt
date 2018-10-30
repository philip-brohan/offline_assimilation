:orphan:

Running many calculations at once
=================================

As there are lots of observations to use, it's often necessary to do a lot of calculation. To do this fast, we need to parallelise it - to do more than one thing at a time.

My preferred way to do this is to divide the calculational task into many small independent tasks, and then process this list of tasks as fast as possible by running many of them at once. The best way to do this is system dependent.

Laptop approach - GNU parallel
------------------------------

A simple tool to process task queues is `GNU parallel <https://www.gnu.org/software/parallel/>`_. This will use all the cores of a single computer, so if your machine has 4 cores it will run the tasks 4 at a time. If the tasks each use a lot of memory it may be desirable to tell it to run fewer at once.

Met Office approach - SPICE cluster
-----------------------------------

At the Met Office, the Scientific Processing and Intensive Compute Environment (SPICE) can be used to run many tasks in parallel. SPICE is a cluster managed by the `slurm workload manager <https://slurm.schedmd.com/>`_, so to use it each task in the job list needs to be converted into a slurm job and submitted to the cluster. The script to do this is :doc:`spice_parallel <spice_parallel>`.

