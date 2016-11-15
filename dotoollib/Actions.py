import digitalocean
import json
import sys
from pprint import pprint

def stripvars(source):
    return_dict = {}
    for item in source:
        i = vars(item)
        for key in ['token', 'end_point', '_log']:
            i.pop(key, None)
        return_dict[i['slug']] = i
    return(return_dict)

class Actions:
    def __init__(self, config, manager):
        self.domanager = manager
        self.Config = config

    def dolist(self, args):
        droplets = self.domanager.get_all_droplets()
        from pprint import pprint
        for droplet in droplets:
            name = droplet.name
            print(name)

    def listslug(self, args):
        import ast
        from tabulate import tabulate
        table = []
        if args.listslug == 'regions':
            headers = ['Name', 'Slug', 'Features']
            #regions = self.Config['Regions']
            #for region in sorted(regions,
            #                     key=lambda regions: (regions['slug'])):
            for region in self.Config['Regions']:
                image = ast.literal_eval(self.Config['Regions'][region])
                table.append([image['name'], region, ', '.join(image['features'])])
            table = sorted(table)
        elif args.listslug == 'images':
            headers = ['Name', 'Slug', 'Regions']
            for image in self.Config['DistImages']:
                image = ast.literal_eval(self.Config['DistImages'][image])
                table.append([image['distribution'] + ' ' + image['name'], image['slug'], ', '.join(image['regions'])])
            for image in self.Config['AppImages']:
                image = ast.literal_eval(self.Config['AppImages'][image])
                table.append([image['distribution'] + ' ' + image['name'], image['slug'], ', '.join(image['regions'])])
            table = sorted(table)
        elif args.listslug == 'sizes':
            headers = ['Slug',
                       'vCPUs',
                       'disk',
                       'trans',
                       'Monthly',
                       'Hourly',
                       'Regions',
            ]
            for image in self.Config['Sizes']:
                image = ast.literal_eval(self.Config['Sizes'][image])
                table.append([
                              image['memory']/1024,
                    image['slug'],
                              str(image['vcpus']),
                              str(image['disk']),
                              str(int(image['transfer'])) + ' TB',
                              '$' + str('{:9,.2f}'.format(image['price_monthly'])),
                              '$' + str('{:5,.2f}'.format(image['price_hourly'])),
                              ', '.join(image['regions']),
                ])
            table = sorted(table)
            for i in table:
                i.pop(0)
        print(tabulate(table, headers, tablefmt="fancy_grid"))

    def create(self, args):
        if args.region == None:
            print('Please select a region to create in.\n\n' +
                  'To view a list run ' + sys.argv[0] + ' listslug regions')
            exit(1)
        if args.image == None:
            print('Please select an image to create from.\n\n' +
                  'To view a list run ' + sys.argv[0] + ' listslug images')
            exit(1)
        if args.size == None:
            print('Please select a droplet size to create.\n\n' +
                  'To view a list run ' + sys.argv[0] + ' listslug sizes')
            exit(1)
        droplet = digitalocean.Droplet(token=self.Config['auth']['token'],
                                       name=args.name,
                                       region=args.region,
                                       image=args.image,
                                       size_slug=args.size,
                                       backups=args.backups,
                                       #ssh_keys_id,
                                       ipv6 = args.ipv6,
                                       private_networking = args.privnet,
                                       #volumes
        )
        droplet.create()
        from pprint import pprint
        pprint(vars(droplet))

    def update(self, args):
        store = {'Regions': stripvars(self.domanager.get_all_regions()),
                 'DistImages': stripvars(self.domanager.get_images(type='distribution')),
                 'AppImages': stripvars(self.domanager.get_images(type='application')),
                 'Sizes': stripvars(self.domanager.get_all_sizes())}
        f = open('datastore.json', 'w')
        f.truncate()
        f.write(json.dumps(store))
        f.close()
