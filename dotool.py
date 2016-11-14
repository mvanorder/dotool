#!/usr/bin/env python3

import sys
from pprint import pprint

# Ensure that this code is running in Python 3 or greater
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version)
    exit(1)

# Try to import the digitalocean library
try:
    import digitalocean
except ImportError:
    print("python-digitalocean doesn't appear to be installed, please run install.py");
    exit(1)

# Import local libraries
from dotoollib import Config, ArgsParser, Actions

doconfig = Config

manager = digitalocean.Manager(token=Config['auth']['token'])
try:
    my_droplets = manager.get_all_droplets()
except:
    print('Unable to connect to DigitalOcean')
    exit(1)

actions = Actions(Config, manager)
parser = ArgsParser(Config, actions)

parser.args.func(parser.args)
