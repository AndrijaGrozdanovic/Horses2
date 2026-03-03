from configparser import ConfigParser
import os


def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        config_path = os.path.join(current_dir, "mainConf.cfg")
        if os.path.exists(config_path):
            break
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        if parent_dir == current_dir:
            raise FileNotFoundError("Config file not found in any parent directory.")
        current_dir = parent_dir
    config = ConfigParser()
    config.read(config_path)
    return config


class Parameters(object):

    def __init__(self):
        config = load_config()
        self.mainPage = ""
        self.driver = ""

        self.server = ""
        self.database = ""
        self.dbdriver = ""

        if config.has_section('selenium'):
            self.mainPage = config.get('selenium', 'main_page')
            self.driver = config.get('selenium', 'driver')

        if config.has_section('mssql'):
            self.server = config.get('mssql', 'server')
            self.database = config.get('mssql', 'database')
            self.dbdriver = config.get('mssql', 'driver')
