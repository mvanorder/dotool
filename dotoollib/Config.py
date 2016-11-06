from configparser import ConfigParser
import os
import json
from pprint import pprint

Config = ConfigParser()
Config.read(['defaults.cfg', '/etc/dotool.cfg', os.path.expanduser('~/.dotool.cfg')])
addition_configs = {}
Regions = {}
with open('regions.json') as data_file:
    data = json.load(data_file)

for region in data:
    Regions[region['slug']] = region['name']

addition_configs['Regions'] = Regions
Config.read_dict(addition_configs)
