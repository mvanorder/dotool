import configparser
import os

Config = configparser.ConfigParser()
Config.read(['defaults.cfg', '/etc/dotool.cfg', os.path.expanduser('~/.dotool.cfg')])
