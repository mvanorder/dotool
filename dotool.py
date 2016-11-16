#!/usr/bin/env python3

import sys

# Ensure that this code is running in Python 3 or greater
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version.split()[0])
    exit(1)

for import_item in open('includes.csv', 'r'):
    # Try to import each required library that doesn't come with python normally
    try:
        exec('import ' + import_item.split(',')[1])
    except ImportError:
        print(import_item.split(',')[1].strip('\n') + ' doesn\'t appear to be installed, please run install.py');
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

if 'func' in parser.args:
    parser.args.func(parser.args)
else:
    parser.parser.parse_args(['-h'])
