#!/usr/bin/env python3

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version.split()[0])
    exit(1)

for import_item in open('includes.csv', 'r'):
    try:
        exec('import ' + import_item.split(',')[1])
    except ImportError:
        try:
            import pip
        except ImportError:
            print("Pip doesn't appear to be installed, please install pip");
            exit(1)

        import os
        if os.geteuid() > 0:
            print("You need root permissions to do this.")
            exit(1)

        pip.main(['install', import_item.split(',')[0]])

