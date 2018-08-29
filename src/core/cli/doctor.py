import helpers
from core import FileManager, JsonParser
import pip
from sys import exit


class doctor:

    def __init__(self):
        self.folders = {
            "packages": helpers.getCobanPath + "\\packages",
            "lib": helpers.getCobanPath + "\\lib",
            "tools": helpers.getToolsPath
        }

        self.files = {
            "programList": helpers.getCobanPath + "\\programList.json",
            "packages": helpers.getCobanPath + "\\packages.json",
            "symlinks": helpers.getCobanPath + "\\symlinks.json",
            'config': helpers.getCobanPath + '\\config.json'
        }

    def createFolders(self):
        file = FileManager.Manager()

        for i in self.folders:
            if not file.fileExists(self.folders[i]):
                helpers.infoMessage("Created: " + i)
                file.createFolder(self.folders[i])

    def validateJsonFiles(self):
        file = FileManager.Manager()
        for i in self.files:
            json = JsonParser.Parser(self.files[i])
            if file.fileExists(self.files[i]):
                if not json.isValid():
                    if helpers.askQuestion('Do you want to rewrite {} file. (You might lose your settings based on which file you rewritting.)'.format(i)):
                        helpers.infoMessage("Fixed: " + i)
                        json.rewriteJson()
            else:
                self.createFiles()

    def createFiles(self):
        file = FileManager.Manager()

        for i in self.files:
            if not file.fileExists(self.files[i]):
                helpers.infoMessage("Created: " + i)
                if i in self.file_contents():
                    file.createFile(self.files[i], self.file_contents()[i])
                else:
                    file.createFile(self.files[i])

    def downloadDependencies(self):
        dependencies = ["colorama", "requests", "tqdm"]
        for i in dependencies:
            pip.main(["install", i])

    def file_contents(self):
        __config = {
            "skipHashByDefault": False,
            "skipQuestionConfirmations": False,
            "auth_key": ""
        }

        files = {
            "config": JsonParser.Parser().dump_json(__config, True)
        }

        return files
# TODO: add os path if choban is there or not
