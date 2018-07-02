import json
from . import FileManager
import helpers
from Logger import Logger as log
from sys import argv

class Parser:
    def __init__(self, path=""):
        self.path = path
        pass

    def fileToJson(self, path=""):
        """
        Converts json file to dict.
        :param path:
        :return json:
        """
        if not path == "":
            with open(path, "r") as f:

                try:
                    convertToJSON = json.load(f)
                    return convertToJSON

                except Exception as e:
                    log.new(e).logError()
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: " + path, True)
                    if "--verbose" in argv:
                        print(e)
                    return False

        else:
            with open(self.path, "r") as f:
                try:
                    convertToJSON = json.load(f)
                    return convertToJSON

                except Exception as e:
                    log.new(e).logError()
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: " + self.path, True)
                    if "--verbose" in argv:
                        print(e)
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
            exit(e)

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
            exit(key + " does not exists")

    def addNewPackage(self, packageName, version):
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
                    "version": version
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
        jsonFile = helpers.symlinkList()
        js = helpers.getCobanPath + "\\symlinks.json"

        if packageName in jsonFile:
            jsonFile.pop(packageName)

        with open(js, "w") as f:
            f.write(json.dumps(jsonFile))
            f.close()

    def removePackage(self, packageName):
        jsonFile = helpers.getCobanPath + "\\packages.json"
        with open(jsonFile, "r") as f:
            js = json.load(f)
            f.close()
        try:
            newDict = js["installedApps"].pop(packageName)
        except ValueError as e:
            log.new(e).logError()
            pass

        with open(jsonFile, "w") as f:
            f.write(json.dumps(js))
            f.close()

    def keyExists(self, array, key):
        if key in array:
            return True
        else:
            return False


    def is_json(self, string):
        try:
            json.loads(string)
        except ValueError as e:
            return False
        return True