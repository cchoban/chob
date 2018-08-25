import helpers, os
from core import FileManager as fs
class Configurator():
    def __init__(self):
        self.__config_file = os.path.join(helpers.getCobanPath,'config.json')
        pass

    def __read_config_file(self):
        pass
