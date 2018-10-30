:orphan:

spice_parallel: submitting a task queue to SPICE
================================================

If ``run.txt`` is a file with a list of tasks (one per line), then run them all on SPICE with:

.. code-block:: sh

   spice_parallel --time=10 < run.txt

Options:

* ``--time`` - CPU time required for a single task - required.
* ``--output`` - task output files will be put in ``$SCRATCH/slurm_output``. If this option is set, the value given will be used as a subdirectory name. So ``--output=test`` will leave the output files in ``$SCRATCH/slurm_output/test``.
* ``--qos`` - Quality-of-service queue to submit to. Can be ``high``, ``normal``, or ``low``. Leave at the default of ``normal`` unless you are sure you know better.
* ``--ntasks`` Number of CPUs needed by each task. Defaults to 1.
* ``--mem`` RAM requirement for each task (Mb). Defaults to 10,000.


Source
------

.. literalinclude:: ../../tools/spice_parallel.py
