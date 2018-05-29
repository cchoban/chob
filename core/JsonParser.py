import json
from . import FileManager
import helpers
from Logger import Logger as log


class Parser:
    def __init__(self, path=""):
        self.path = path
        pass

    def fileToJson(self, path=""):
        if not path == "":
            with open(path, "r") as f:

                try:
                    convertToJSON = json.load(f)
                    return convertToJSON

                except Exception as e:
                    log.new(e).logError()
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: " + path, True)
                    return False

        else:
            with open(self.path, "r") as f:
                try:
                    convertToJSON = json.load(f)
                    return convertToJSON

                except Exception as e:
                    log.new(e).logError()
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: " + path, True)
                    return False

    def isValid(self):
        try:
            if self.fileToJson():
                return True
            else:
                return False
        except Exception as e:
            return False

    def rewriteJson(self):
        try:
            with open(self.path, "w") as f:
                js = json.dumps({})
                f.write(js)
                f.close()
        except OSError as e:
            exit(e)

    def getKey(self, key, path):
        dict = self.fileToJson(path)

        try:
            dict["packageArgs"][key]
        except KeyError as e:
            exit(key + " does not exists")

    def addNewPackage(self, packageName):
        jsonFile = helpers.getCobanPath + "\\packages.json"
        js = helpers.installedApps()

        if not packageName in js["installedApps"]:
            print(js)
            js["installedApps"].append(packageName)

            with open(jsonFile, "w") as f:
                f.write(json.dumps(js))
                f.close()

    def removePackage(self, packageName):
        jsonFile = helpers.getCobanPath + "\\packages.json"
        with open(jsonFile, "r") as f:
            js = json.load(f)
            f.close()
        try:
            newDict = js["installedApps"].remove(packageName)
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
