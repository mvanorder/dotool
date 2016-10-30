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
my_droplets = manager.get_all_droplets()

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

parser_create = subparser.add_parser('action')
parser_create.add_argument('action_type',
                           default='server',
                           const='server',
                           nargs='?',
                           choices=['shutdown', 'start', 'reboot'],
                           help='Server actions (default: %(default)s).')

parser_create = subparser.add_parser('status')
parser_create.add_argument('request_type',
                           default='status',
                           const='status',
                           nargs='?',
                           choices=['status'],
                           help='Requst server status.')

args = parser.parse_args()
pprint(vars(args))
