import helpers
from core import FileManager, JsonParser
class doctor:
    def __init__(self):
        self.folders = {
            "packages": helpers.getCobanPath + "\\packages",
            "lib": helpers.getCobanPath + "\\lib",
            "tools": helpers.getToolsPath
        }

        self.files = {
            "programList": helpers.getCobanPath + "\\programList.json",
            "packages": helpers.getCobanPath + "\\packages.json"
        }
    def createFolders(self):
        file = FileManager.Manager

        for i in self.folders:
            if not file.fileExists(self.folders[i]):
                helpers.infoMessage("Created: " + i)
                file.createFolder(self.folders[i])

    def validateJsonFiles(self):
        file = FileManager.Manager
        for i in self.files:
            json = JsonParser.Parser(self.files[i])
            if file.fileExists(self.files[i]):
                if json.isValid():
                    pass
                else:
                    helpers.infoMessage("Fixed repo: "+i)
                    json.rewriteJson()
            else:
                self.createFiles()

    def createFiles(self):
        file = FileManager.Manager

        for i in self.files:
            if not file.fileExists(self.files[i]):
                helpers.infoMessage("Created: " + i)
                file.createFolder(self.files[i])