Meerkat is a tool for setting up batches of jobs, and then loading them in the
Python interpreter for post-processing. You provide a Python module that
generates objects corresponding to each job, pickling them, and a program that
opens each pickle, runs the object contained within, and saves the object after
the run.

Your module implements the following:

* L_variables, a list of lists of values for each parameter that you're varying
* setup(parameter_1, parameter_2, ...), which, for a given set of values of
  each parameter, generates a pickled object, ready to be run.
* job_name(parameter_1, parameter_2, ...), which generates a job name; for each
  job_name, a file, job_name.pkl should be generated.
* Lines beginning with "#meerkat-copy", followed by a list of files and
  directories to copy to the path in which the runs are performed, for example,
* run()

#meerkat-copy code_module script_to_run_code.py



Optionally, your module can provide,

* prototype(), which returns one example run out of module.d_runs
    return d_runs[(1., 400.)]
* default_suffix = '.run.pkl'

    runner.setup(L_job_name)
# setup is also required
#End required by Meerkat


1. Setting up jobs:

meerkat [module] [path]

scans the text of [module] looking for lines beginning with 

./meerkat/cmdline.py
