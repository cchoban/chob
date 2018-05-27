import json
from . import FileManager
import helpers

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
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: "+ path, True)
                    exit()
        else:
            with open(self.path, "r") as f:
                try:
                    convertToJSON = json.load(f)
                    return convertToJSON

                except Exception as e:
                    helpers.errorMessage("Could not parse JSON file while trying to convert it: "+path, True)
                    exit()

    def isValid(self):
        try:
            self.fileToJson()
            return True
        except ValueError as e:
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
            exit(key+" does not exists")

    def addNewPackage(packageName):
        jsonFile = helpers.getCobanPath+"\\packages.json"
        with open(jsonFile, "r") as f:
            js = json.load(f)
            f.close()
        newDict = js["installedApps"].append(packageName)

        with open(jsonFile, "w") as f:
            f.write(json.dumps(js))
            f.close()

    def removePackage(packageName):
        jsonFile = helpers.getCobanPath + "\\packages.json"
        with open(jsonFile, "r") as f:
            js = json.load(f)
            f.close()
        newDict = js["installedApps"].pop(packageName)

        with open(jsonFile, "w") as f:
            f.write(json.dumps(js))
            f.close()

    def keyExists(array, key):
        try:
            array[key]
            return True
        except KeyError as e:
            return False