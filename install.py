#!/usr/bin/env python

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version)
    exit(1)

try:
    import digitalocean
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

    pip.main(['install', 'python-digitalocean'])

