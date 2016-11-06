import digitalocean

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
        # Get the list of regions
        regions = manager.get_all_regions()
        regions_list = []

        # Strip unneeded keys from each entry and append the modified entry to the list
        for region in regions:
            r = vars(region)
            r.pop('token', None)
            r.pop('end_point', None)
            r.pop('_log', None)
            regions_list.append(r)

        # Save the modified list in a json file
        f = open('regions.json', 'w')
        f.truncate()
        f.write(json.dumps(regions_list))
        pprint(json.dumps(regions_list))
        f.close()
