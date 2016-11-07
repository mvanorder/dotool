import argparse

class ArgsParser(object):
    def __init__(self, config, Actions):
        self.config = config
        self.Actions = Actions
        self.args = self.parse()

    def parse(self):
        parser = argparse.ArgumentParser(description='Digital Ocean tool')
        subparser = parser.add_subparsers()

        parser_list = subparser.add_parser('list')
        parser_list.add_argument('list',
                                 default='all',
                                 const='all',
                                 nargs='?',
                                 choices=['all', 'servers', 'storage'],
                                 help='list servers, storage, or both(default: %(default)s).')
        parser_list.set_defaults(func=self.Actions.dolist)

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
                                   help='Region')
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

        return parser.parse_args()
