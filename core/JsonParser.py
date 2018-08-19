import json
from . import FileManager
import helpers
from Logger import Logger as log
from sys import argv, exit

class JsonIsNotValid(Exception):
    pass

class KeyNotFound(Exception):
    pass


class Parser:

    def __init__(self, path=""):
        self.path = path
        self.json = {}
        self.objects = {
            "{cobanPath}": helpers.getCobanPath,
            "{cobanTools}": helpers.getToolsPath
        }

    def fileToJson(self, path=""):
        """
        Converts json file to dict.
        :param path: Json absolute path
        :return json:
        """

        _path = path or self.path
        if _path:
            with open(_path, "r") as f:

                try:
                    convertToJSON = json.load(f)
                    self.json = convertToJSON
                    # FIXME: can make a problem
                    if helpers.getCobanPath + "\\packages\\" in _path or ".package\\" in _path:
                        self.compile_objects()
                    return self.json

                except Exception as e:
                    log.new(e).logError()
                    helpers.errorMessage(
                        "Could not parse JSON file while trying to convert it: " + _path, True)
                    if helpers.is_verbose():
                        helpers.errorMessage(
                            "JsonParser.fileToJson - " + str(e))
                    raise JsonIsNotValid(e)
                    return False

    def isValid(self):
        """
        Checks json file if is valid or not.

        :usage JsonParser.Parser(path).isValid()
        :return boolean:
        """
        try:
            if self.fileToJson():
                return True
            else:
                return False
        except Exception as e:
            raise JsonIsNotValid(e)
            return False

    def rewriteJson(self):
        """
        Rewrite json file with empty dict.
        :usage JsonParser.Parser(path).rewriteJson()

        """
        try:
            with open(self.path, "w") as f:
                js = json.dumps({})
                f.write(js)
                f.close()
        except OSError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("JsonParser.rewriteJson - " + str(e))

    def getKey(self, key, path):
        """
        Returns wanted key
        :param key:
        :param path:
        :return str
        """
        dict = self.fileToJson(path)

        try:
            dict["packageArgs"][key]
        except KeyError as e:
            raise KeyNotFound(e)
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("JsonParser.getKey - " + str(e))

    def addNewPackage(self, packageName, context: dict):
        """
        Adds new package to packages.json
        :param packageName:
        :param version:
        """
        jsonFile = helpers.getCobanPath + "\\packages.json"
        js = helpers.installedApps()

        if not packageName in js["installedApps"] and not "--test-package" in argv:
            newPackage = {
                packageName: {
                    "version": context.get("version"),
                    "dependencies": context.get("dependencies")
                }
            }

            dict = {**js["installedApps"], **newPackage}

            js["installedApps"].update(dict)

            with open(jsonFile, "w") as f:
                f.write(json.dumps(js))
                f.close()

    def add_new_symlink(self, packageName, dest):
        """Adds symlink desinitation to symlinks.json for removing it later

        :param packageName: Package name for symlink key
        :param dest: Desiniation path for symlink
        """
        jsonFile = helpers.symlinkList()
        js = helpers.getCobanPath + "\\symlinks.json"
        if not packageName in jsonFile:
            jsonFile[packageName] = dest

            with open(js, "w") as f:
                f.write(json.dumps(jsonFile))
                f.close()

    def remove_package_symlink(self, packageName):
        """Removes already created package symlink

        Arguments:
        :param packageName: Package name for remove symlink
        """
        jsonFile = helpers.symlinkList()
        js = helpers.getCobanPath + "\\symlinks.json"

        if packageName in jsonFile:
            jsonFile.pop(packageName)

        with open(js, "w") as f:
            f.write(json.dumps(jsonFile))
            f.close()

    def removePackage(self, packageName):
        """Removes a packagefrom packages.json

        Arguments:
        :param packageName: Package name for removing it from packages.json
        """
        jsonFile = helpers.getCobanPath + "\\packages.json"
        with open(jsonFile, "r") as f:
            js = json.load(f)
            f.close()
        try:
            newDict = js["installedApps"].pop(packageName)
        except ValueError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("JsonParser.removePackage() = " + e)
        with open(jsonFile, "w") as f:
            f.write(json.dumps(js))
            f.close()

    def keyExists(self, array, key):
        """Check is specified key exists in array

        Arguments:
        :param array: Array to check key if it exists or not.
        :param key: Key to check if it exists in array
        :return boolean:
        """
        if key in array:
            return True
        else:
            return False

    def is_json(self, string):
        """Determining if string is json

        Arguments:
        :param string: String to be controller if its json or not.
        :return boolean:
        """
        try:
            json.loads(string)
        except ValueError as e:
            raise JsonIsNotValid(e)
            return False
        return True

    def compile_objects(self):
        """Merge objects in json file."""
        objects = [obj for obj in self.objects]
        package_args = self.json["packageArgs"]
        for i in package_args:
            if package_args[i] in objects:
                package_args[i] = package_args[i].replace(
                    package_args[i], self.objects[package_args[i]])
