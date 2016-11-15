import argparse

class ArgsParser(object):
    def __init__(self, config, Actions):
        self.config = config
        self.Actions = Actions
        self.parser = argparse.ArgumentParser(description='Digital Ocean tool')
        self.args = self.parse()

    def parse(self):
        subparser = self.parser.add_subparsers()

        parser_list = subparser.add_parser('list')
        parser_list.add_argument('list',
                                 default='all',
                                 const='all',
                                 nargs='?',
                                 choices=['all', 'servers', 'storage'],
                                 help='list servers, storage, or both(default: %(default)s).')
        parser_list.set_defaults(func=self.Actions.dolist)

        parser_listslug = subparser.add_parser('listslug')
        parser_listslug.add_argument('listslug',
                                     action='store',
                                     choices=['regions', 'images', 'sizes'],
                                     help='list servers, storage, or both(default: %(default)s).')
        parser_listslug.set_defaults(func=self.Actions.listslug)

        parser_create = subparser.add_parser('create')
        parser_create.add_argument('create',
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
                                   choices=self.config['Regions'],
                                   help='Droplet region')
        parser_create.add_argument('-s', '--size',
                                   action='store',
                                   required=False,
                                   choices=self.config['Sizes'],
                                   help='Droplet size')
        parser_create.add_argument('-b', '--backups',
                                   action='store_true',
                                   required=False,
                                   help='Enable Backups')
        parser_create.add_argument('-6', '--ipv6',
                                   action='store_true',
                                   required=False,
                                   help='Enable IPv6')
        parser_create.add_argument('-p', '--privnet',
                                   action='store_true',
                                   required=False,
                                   help='Enable private networking')
        
        Images = dict(self.config['DistImages'])
        Images.update(self.config['AppImages'])
        parser_create.add_argument('-i', '--image',
                                   action='store',
                                   required=False,
                                   choices=Images,
                                   help='Image')
        parser_create.set_defaults(func=self.Actions.create)

        parser_action = subparser.add_parser('action')
        parser_action.add_argument('action',
                                   default='server',
                                   const='server',
                                   nargs='?',
                                   choices=['shutdown', 'start', 'reboot'],
                                   help='Server actions (default: %(default)s).')

        parser_status = subparser.add_parser('status')
        parser_status.add_argument('request',
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
        parser_update.set_defaults(func=self.Actions.update)

        return self.parser.parse_args()
