import helpers
import os
from core import FileManager as fs
from core import JsonParser as parser


class Configurator():

    def __init__(self, config, set):
        self.__config_file = os.path.join(helpers.getCobanPath, 'config.json')
        self.config = config
        self.set = set
        if self.__check_for_config():
            self.__read_config_file()
        if not self.__key_exists():
            helpers.errorMessage('We do not have that configuration.')
            return
        self.setConfig()

    def setConfig(self):
        """
        Changes value of a key
        :return void
        """

        try:
            json = parser.Parser(self.__config_file)
            json.fileToJson()
            change = json.change_value(self.config, self.set)

            return helpers.successMessage('Changed value of \'{}\' to \'{}\''.format(self.config, self.set))
        except Exception as e:
            helpers.errorMessage(
                'An error occured while trying to set config.')
            if helpers.is_verbose():
                helpers.errorMessage(
                    'Configuration.config.setConfig - ' + str(e))

    def __read_config_file(self):
        """
        Reads and returns config file.
        :return dict
        """
        file = parser.Parser(self.__config_file)
        if file.isValid():
            return file.fileToJson()

    def __key_exists(self):
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
