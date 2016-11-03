import argparse
from . import Config

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
                           choices=Config['Regions'],
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

Args = parser.parse_args()
