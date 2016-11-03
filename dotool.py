#!/usr/bin/env python

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
from dotoollib import Config, Args

manager = digitalocean.Manager(token=Config['auth']['token'])
try:
    my_droplets = manager.get_all_droplets()
except:
    print('Unable to connect to DigitalOcean')
    exit(1)

pprint(vars(Args))

if 'create_type' in Args:
    if 'region' not in Args:
        print('Please provide a region')
        exit(1)
    droplet = digitalocean.Droplet(token=Config['auth']['token'],
                                   name=Args.name,
                                   region=Args.region,
                                   image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                   size_slug='512mb',  # 512MB
                                   backups=False)
    pprint(vars(droplet))
if 'update' in Args:
    f = open('regions.json', 'w')
    f.truncate()
    for region in (manager.get_all_regions()):
        r = vars(region)
        r.pop('token', None)
        r.pop('end_point', None)
        r.pop('_log', None)
        #print(vars(r['_log']))
        pprint(r)
        f.write(str(r))
    f.close()
        
#pprint(vars(Config._sections))
#pprint(vars(Config['regions']))
#pprint(Config['regions']['nyc1'])
