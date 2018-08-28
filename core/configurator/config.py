import helpers
import os
from core import FileManager as fs
from core import JsonParser as parser


class Configurator():

    def __init__(self, config=""):
        self.config = config
        self.set = ""
        self.__config_file = os.path.join(helpers.getCobanPath, 'config.json')
        if self.__check_for_config():
            self.__read_config_file()
        if len(self.config) > 0 and not self.key_exists():
            helpers.errorMessage('We do not have that configuration.')
            return

    def setConfig(self, config, keySet):
        """
        Changes value of a key
        :return void
        """
        try:
            self.config = config
            self.set = keySet
            json = parser.Parser(self.__config_file)
            json.fileToJson()
            change = json.change_value(config, keySet)

            return helpers.successMessage('Changed value of \'{}\' to \'{}\''.format(self.config, self.set))
        except Exception as e:
            helpers.errorMessage(
                'An error occured while trying to set config.')
            if helpers.is_verbose():
                helpers.errorMessage(
                    'Configuration.config.setConfig - ' + str(e))

    def get_key(self, key):
        """
        Reads and returns key from config file.
        :param key: Key you want to grab from config file.
        :return str
        """

        self.config = config = self.__read_config_file()

        if key in config:
            return config.get(key)
        else:
            if helpers.is_verbose():
                raise parser.KeyNotFound('{} key not found.'.format(key))
            return False

    def __read_config_file(self):
        """
        Reads and returns config file.
        :return dict
        """
        file = parser.Parser(self.__config_file)
        if file.isValid():
            return file.fileToJson()

    def key_exists(self):
        """
        Checks if key exists.
        :return bool
        """
        if parser.Parser().keyExists(self.__read_config_file(), self.config):
            return True
        else:
            return False

    def __check_for_config(self):
        """
        Checks for config file if it exists.
        :return bool
        """
        file = fs.Manager().fileExists(self.__config_file)

        if file:
            return True
        else:
            helpers.errorMessage(
                'Your files are missing! Please correct this using \'chob --doctor\'')
            return False
