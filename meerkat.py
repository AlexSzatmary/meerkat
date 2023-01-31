import os
import pickle
import imp
import sys


def combine(*args):
    if args == ():
        return []
    elif len(args) == 1:
        return [[a] for a in args[0]]
    else:
        return [a + [b] for a in combine(*(args[:-1])) for b in args[-1]]


def get_L_tup(module):
    return list(map(tuple, combine(*module.L_variables)))


def get_L_job_name(module):
    return [module.job_name(*tup) for tup in module.L_tup]


def pre_load(module):
    '''Initial steps in loading module that don't require completed runs'''
    module.L_tup = get_L_tup(module)
    module.L_job_name = get_L_job_name(module)
    module.batch_dir = os.path.dirname(module.__file__)
    module.set_name = os.path.basename(module.batch_dir)


def load(module_path, suffix=None):
    sys.path.insert(0, os.path.dirname(module_path))
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    (hin, p, t) = imp.find_module(module_name, [os.path.dirname(module_path)])
    module = imp.load_module(module_name, hin, p, t)
    if suffix is None:
        suffix = module.default_suffix
    pre_load(module)
    module.d_runs = {}
    for (jn, tup) in zip(module.L_job_name, module.L_tup):
        with open(os.path.join(module.batch_dir, jn + suffix), 'rb') as hin:
            module.d_runs[tup] = pickle.load(hin)
    module.L_runs = [module.d_runs[tup] for tup in module.L_tup]
    sys.path = sys.path[1:]
    return module
