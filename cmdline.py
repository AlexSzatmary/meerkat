#!/usr/bin/env python
import sys
sys.path.insert(0, '..')
import imp
import os
import shutil
import re
import meercat


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    module_path = argv[0]
    path = argv[1]

    os.mkdir(path)

    os.system('cp ' + module_path + ' ' + path)
    with open(module_path) as hin:
        L_copy = []
        for line in hin.readlines():
            m = re.match('#meercat-copy (.*)', line[:-1])
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

    meercat.pre_load(module)
    for tup in module.L_tup:
        module.setup(*tup)

    module.run()


if __name__ == "__main__":
    sys.exit(main())
