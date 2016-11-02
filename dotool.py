#!/usr/bin/env python

import sys
from pprint import pprint

if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, you are running version " + sys.version)
    exit(1)

try:
    import digitalocean
except ImportError:
    print("python-digitalocean doesn't appear to be installed, please run install.py");
    exit(1)

from dotoollib import Config

manager = digitalocean.Manager(token=Config['auth']['token'])
try:
    my_droplets = manager.get_all_droplets()
except:
    print('Unable to connect to DigitalOcean')
    exit(1)

import argparse

parser = argparse.ArgumentParser(description='Digital Ocean tool')
subparser = parser.add_subparsers()

parser_list = subparser.add_parser('list')
parser_list.add_argument('list_type',
                         default='all',
                         const='all',
                         nargs='?',
                         choices=['all', 'servers', 'storage'],
                         help='list servers, storage, or both(default: %(default)s).')

parser_create = subparser.add_parser('create')
parser_create.add_argument('create_type',
                           default='server',
                           const='server',
                           nargs='?',
                           choices=['server', 'storage'],
                           help='create server or storage(default: %(default)s).')
parser_create.add_argument('-n', '--name',
                           action='store',
                           required=True,
                           help='Server name')
parser_create.add_argument('-r', '--region',
                           action='store',
                           required=False,
                           choices=Config['regions'],
                           help='Region')

parser_action = subparser.add_parser('action')
parser_action.add_argument('action_type',
                           default='server',
                           const='server',
                           nargs='?',
                           choices=['shutdown', 'start', 'reboot'],
                           help='Server actions (default: %(default)s).')

parser_status = subparser.add_parser('status')
parser_status.add_argument('request_type',
                           default='status',
                           const='status',
                           nargs='?',
                           choices=['status'],
                           help='Requst server status.')

parser_update = subparser.add_parser('update')
parser_update.add_argument('update',
                           default='all',
                           const='all',
                           nargs='?',
                           choices=['all', 'regions'])

args = parser.parse_args()
pprint(vars(args))

if 'create_type' in args:
    if 'region' not in args:
        print('Please provide a region')
        exit(1)
    droplet = digitalocean.Droplet(token=Config['auth']['token'],
                                   name=args.name,
                                   region=args.region,
                                   image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                   size_slug='512mb',  # 512MB
                                   backups=False)
    pprint(vars(droplet))
if 'update' in args:
    f = open('regions.json', 'w')
    f.truncate()
    for region in (manager.get_all_regions()):
        r = vars(region)
        r.pop('token', None)
        r.pop('end_point', None)
        r['_log'] = vars(r['_log'])
        #r['_log']['manager'] = vars(r['_log']['manager'])
        r['_log'].pop('manager', None)
        #r['_log']['parent'] = vars(r['_log']['parent'])
        r['_log'].pop('parent', None)
        #print(vars(r['_log']))
        pprint(r)
        f.write(str(r))
    f.close()
        
#pprint(vars(Config._sections))
#pprint(vars(Config['regions']))
#pprint(Config['regions']['nyc1'])
