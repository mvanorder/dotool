#!/usr/bin/env python

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version)
    exit(1)

try:
    import digitalocean
except ImportError:
    print("python-digitalocean doesn't appear to be installed, please run install.py");
    exit(1)

from dotoollib import Config

print(Config['auth']['token'])
manager = digitalocean.Manager(token=Config['auth']['token'])
my_droplets = manager.get_all_droplets()
print(my_droplets)
