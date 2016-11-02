from configparser import ConfigParser
import os

Config = ConfigParser()
Config.read(['defaults.cfg', '/etc/dotool.cfg', os.path.expanduser('~/.dotool.cfg')])
