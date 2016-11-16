import digitalocean
import json
import sys
import ast
from tabulate import tabulate

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
        headers = ['Name', 'Loc', 'Size', 'IPv4', 'IPv6', 'Status']
        table = []
        for droplet in droplets:
            name = droplet.name
            table.append([droplet.name,
                          droplet.region['slug'],
                          droplet.size_slug,
                          droplet.ip_address,
                          droplet.ip_v6_address,
                          droplet.status])
        print(tabulate(table, headers, tablefmt="fancy_grid"))

    def listslug(self, args):
        table = []
        if args.listslug == 'regions':
            headers = ['Name', 'Slug', 'Features']
            for region in self.Config['Regions']:
                image = ast.literal_eval(self.Config['Regions'][region])
                table.append([image['name'],
                              region,
                              ', '.join(image['features'])])
            table = sorted(table)

        elif args.listslug == 'images':
            headers = ['Name', 'Slug', 'Regions']
            for image in self.Config['DistImages']:
                image = ast.literal_eval(self.Config['DistImages'][image])
                table.append([image['distribution'] + ' ' + image['name'],
                              image['slug'], ', '.join(image['regions'])])
            for image in self.Config['AppImages']:
                image = ast.literal_eval(self.Config['AppImages'][image])
                table.append([image['distribution'] + ' ' + image['name'],
                              image['slug'], ', '.join(image['regions'])])
            table = sorted(table)

        elif args.listslug == 'sizes':
            headers = ['Slug',
                       'vCPUs',
                       'disk',
                       'trans',
                       'Monthly',
                       'Hourly',
                       'Regions']
            for image in self.Config['Sizes']:
                image = ast.literal_eval(self.Config['Sizes'][image])
                table.append([image['memory']/1024,
                              image['slug'],
                              str(image['vcpus']),
                              str(image['disk']),
                              str(int(image['transfer'])) + ' TB',
                              '$' + str('{:9,.2f}'.format(image['price_monthly'])),
                              '$' + str('{:5,.2f}'.format(image['price_hourly'])),
                              ', '.join(image['regions'])])
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
        #from pprint import pprint
        #pprint(vars(droplet))
        print('Creating ' + droplet.name, end='', flush=True)
        while True:
            actions = droplet.get_actions()
            if actions[0].status == 'completed':
                print()
                break
            else:
                print('.', end='', flush=True)

    def delete(self, args):
        droplets = self.domanager.get_all_droplets()
        droplet_dict = {}

        for droplet in droplets:
            droplet_dict[droplet.name] = droplet

        if args.droplet in droplet_dict:
            #headers = ['Name', 'Loc', 'Size', 'IPv4', 'IPv6', 'Status']
            table = [['Name', droplet_dict[args.droplet].name],
                     ['Location', droplet_dict[args.droplet].region['slug']],
                     ['Size', droplet_dict[args.droplet].size_slug],
                     ['IPv4', droplet_dict[args.droplet].ip_address],
                     ['IPv6', droplet_dict[args.droplet].ip_v6_address],
                     ['Status', droplet_dict[args.droplet].status]]
            print(tabulate(table, tablefmt="fancy_grid"))
            while True:
                verify = input('Are you sure you want to delete this droplet(YES/NO): ')
                if verify == 'YES':
                    droplet_dict[args.droplet].destroy()
                    break
                elif verify == 'NO':
                    break
                else:
                    print(verify + ' is not a valid answer.')
        else:
            print('Unable to find droplet named ' + args.droplet)

    def update(self, args):
        store = {'Regions': stripvars(self.domanager.get_all_regions()),
                 'DistImages': stripvars(self.domanager.get_images(type='distribution')),
                 'AppImages': stripvars(self.domanager.get_images(type='application')),
                 'Sizes': stripvars(self.domanager.get_all_sizes())}
        f = open('datastore.json', 'w')
        f.truncate()
        f.write(json.dumps(store))
        f.close()

    def status(self, args):
        droplets = self.domanager.get_all_droplets()
        droplet_dict = {}

        for droplet in droplets:
            droplet_dict[droplet.name] = droplet

        if args.droplet in droplet_dict:
            actions = droplet_dict[args.droplet].get_actions()

            if args.verbose:
                headers = ['Value']
                table = []
                this_droplet = vars(droplet_dict[args.droplet])
                this_droplet['image'] = this_droplet['image']['distribution'] + ' ' + this_droplet['image']['name']
                this_droplet['region'] = this_droplet['region']['name']
                this_droplet['size'] = this_droplet['size_slug']
                if this_droplet['kernel']:
                    this_droplet['kernel'] = this_droplet['kernel']['name']
                this_droplet['features'] = ', '.join(this_droplet['features'])
                for i in ['_log', 'token', 'size_slug', 'end_point', 'networks']:
                    this_droplet.pop(i, None)
                for key in this_droplet:
                    table.append([key, this_droplet[key]])
                table = sorted(table)
                print(tabulate(table, headers, tablefmt="fancy_grid"))

            print('Status: ' + actions[0].type + ' ' + actions[0].status + ' ', end='')
            if actions[0].status == 'completed':
                print(actions[0].completed_at)
            else:
                print()
        else:
            print('Unable to find droplet named ' + args.droplet)
