import digitalocean
import json
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

    def create(self, args):
        if args.region == None:
            print('Please provide a region to create in.')
            exit(1)
        droplet = digitalocean.Droplet(token=self.Config['auth']['token'],
                                       name=args.name,
                                       region=args.region,
                                       image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                       size_slug='512mb',  # 512MB
                                       backups=False)
        from pprint import pprint
        pprint(vars(droplet))

    def update(self, args):
        store = {'regions': stripvars(self.domanager.get_all_regions()),
                 'dist_images': stripvars(self.domanager.get_images(type='distribution')),
                 'app_images': stripvars(self.domanager.get_images(type='application'))}
        f = open('datastore.json', 'w')
        f.truncate()
        f.write(json.dumps(store))
        f.close()
