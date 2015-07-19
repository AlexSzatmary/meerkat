#!/usr/bin/env python
import argparse
import sys
sys.path.insert(0, '..')
import imp
import os
import shutil
import re
from . import meerkat


def make_argparser():
    a = argparse.ArgumentParser()
    a.add_argument('--rm', action='store_true')
    a.add_argument('fromx', metavar='from')
    a.add_argument('to')
    return a


def main(argv=None):
    argparser = make_argparser()
    if argv is None:
        argv = sys.argv[1:]
    args = argparser.parse_args(argv)
    module_path = args.fromx
    path = args.to

    if args.rm:
        shutil.rmtree(path)
    os.mkdir(path)

    os.system('cp ' + module_path + ' ' + path)
    with open(module_path) as hin:
        L_copy = []
        for line in hin.readlines():
            m = re.match('#meerkat-copy (.*)', line[:-1])
            if m is not None:
                L_copy.append(m.group(1))
    os.system('cp -R ' + ' '.join(L_copy) + ' ' + path)

    os.system('git show > ' + os.path.join(path, 'git-show.txt'))

    sys.path.insert(0, path)
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    (hin, p, t) = imp.find_module(module_name, [path])
    module = imp.load_module(module_name, hin, p, t)

#    home = os.getcwd()
    os.chdir(path)
#    os.chdir(home)

    meerkat.pre_load(module)
    for tup in module.L_tup:
        module.setup(*tup)

    module.run()


if __name__ == "__main__":
    sys.exit(main())
