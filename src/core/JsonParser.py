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
            "{cobanTools}": helpers.getToolsPath,
            "{packageName}": self.__package_name,
            "{packageToolsPath}": self.__package_tools_path,
        }

    def fileToJson(self, path=""):
        """
        Converts json file to dict.
        :param path: Json absolute path
        :return json:
        """
        _path = path or self.path
        if _path:
            try:
                with open(_path, "r") as f:


                        convertToJSON = json.load(f)
                        self.json = convertToJSON
                        # FIXME: can make a problem
                        if helpers.getCobanPath + "\\packages\\" in _path or ".package\\" in _path:
                            self.compile_objects()
                        return self.json

            except Exception as e:
                helpers.errorMessage(
                    "Could not parse JSON file while trying to convert it: " + _path, True)
                if helpers.is_verbose():
                    helpers.errorMessage(
                        "JsonParser.fileToJson - " + str(e))
                    raise JsonIsNotValid(e)
                log.new(e).logError()

                return False

    def isValid(self):
        """
        Checks json file if is valid or not.

        :usage JsonParser.Parser(path).isValid()
        :return boolean:
        """
        try:
            self.fileToJson()
            return True
        except Exception as e:
            return False

    def rewriteJson(self, dict_obj={}, beautify=False):
        """
        Rewrite json file with empty dict.

        :param dict_obj: Dump existing json object.
        :usage JsonParser.Parser(path).rewriteJson()

        """
        try:
            with open(self.path, "w") as f:
                js = self.dump_json(dict_obj, beautify)
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
            return dict[key]
        except KeyError as e:
            log.new("JsonParser.getKey - " + str(e)).logError()
            if helpers.is_verbose():
                raise KeyNotFound(e)
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

                return True
        else:
            return True

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
            if helpers.is_verbose():
                raise JsonIsNotValid(e)
            return False
        return True

    def change_value(self, key, value):
        """Changes a value of a key from json file instance.

        Arguments:
        :param key: Key you want to change value of.
        :param value: Value to change it.
        :usage JsonParser.Parser(path).change_value(from, to)
        :return boolean:
        """
        if self.keyExists(self.json, key):
            try:
                self.json[key] = value
                with open(self.path, "w") as f:
                    f.write(json.dumps(self.json, indent=4, sort_keys=True))
                    f.close()
                    return True
            except Exception as e:
                if helpers.is_verbose():
                    helpers.errorMessage(str(e))
                return False
        else:
            return False

    def compile_objects(self):
        """Merge objects in json file."""
        objects = [obj for obj in self.objects]
        package_args = self.json["packageArgs"]
        empty_list = []

        for i in package_args:
            if package_args[i] in objects:
                package_args[i] = package_args[i].replace(package_args[i], self.objects[package_args[i]])

            if isinstance(package_args[i], dict):
                for p in package_args[i]:
                    if package_args[i][p] in objects:
                        package_args[i][p] = package_args[i][p].replace(package_args[i][p], self.objects[package_args[i][p]])
                    else:
                        gathered_object_key = self.__search_via_regex(package_args[i][p])
                        if gathered_object_key:
                            package_args[i][p] = package_args[i][p].replace(gathered_object_key, self.objects[gathered_object_key])

            elif isinstance(package_args[i], list):
                for p in package_args[i]:
                    if p in objects:
                        package_args[i] = p.replace(p, self.objects[p])
                    else:
                        gathered_object_key = self.__search_via_regex(p)
                        if gathered_object_key:
                            package_args[i] = empty_list
                            if hasattr(self.objects[gathered_object_key], '__call__'):
                                empty_list.append(p.replace(gathered_object_key, self.objects[gathered_object_key]()))
                            else:
                                empty_list.append(p.replace(gathered_object_key, self.objects[gathered_object_key]))

            else:
                gathered_object_key = self.__search_via_regex(package_args[i])
                if gathered_object_key:
                    package_args[i] = package_args[i].replace(gathered_object_key, self.objects[gathered_object_key])


    def __search_via_regex(self, string):
        from re import search

        search = search('\{([^}]+)\}', str(string))
        if search:
            gathered_object_key = search.group(0)
            if gathered_object_key in self.objects:
                return gathered_object_key
            else:
                return False
        else:
            return False


    def dump_json(self, dict: dict, beautify=False):
        """Converts dict to json object.

        Arguments:
        :param dict: Dictionary you want convert to json object.
        :param beautify: Beautifies json object with indent.
        :return json:
        """
        if beautify:
            return json.dumps(dict, indent=4, sort_keys=True)
        else:
            return json.dumps(dict)

    def __package_name(self):
        """ Returns package name to use it inside installation scripts """

        if len(self.json) > 1:
            return self.json.get('packageArgs')['packageName']

    def __package_tools_path(self):
        """ Returns 'chobanapps' path for package """

        package_args = self.json['packageArgs']
        if self.keyExists(package_args, 'unzip'):
            if len(self.json) > 1:
                return FileManager.os.path.join(helpers.getToolsPath, package_args.get('packageName'))

