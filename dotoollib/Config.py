from configparser import ConfigParser
import os
import json
from pprint import pprint

def loadstore():
    try:
        f = open('datastore.json', 'r')
    except:
        print('Unable to load regions.  Please run update.\n')
        return({'Regions': {},
                'DistImages': {},
                'AppImages': {},
                'Sizes': {}})

    return json.loads(f.read())
    f.close()

Config = ConfigParser()
Config.read(['defaults.cfg', '/etc/dotool.cfg', os.path.expanduser('~/.dotool.cfg')])
Config.read_dict(loadstore())
