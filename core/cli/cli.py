import repo, helpers
from core import http, FileManager, JsonParser
from Logger import Logger as log
from . import doctor
class main:
    def __init__(self):
        pass


    def update(self):
        helpers.infoMessage("Updating repo "+repo.repos()["programList"])
        try:
            http.Http.download(http.Http, repo.repos()["programList"], helpers.getCobanPath+"\\programList", "json")
        except Exception as e:
            log.new(e).logError()

    def doctor(self):
        self.update()
        doc = doctor.doctor()
        doc.createFolders()
        doc.validateJsonFiles()

        helpers.successMessage("Fixed problems..")

    def cleanLeftOvers(self):
        fileManager = FileManager.Manager().cleanup()

    def packages(self):
        self.update()
        js = JsonParser.Parser(repo.repos()["localProgramlist"]).fileToJson()
        for i in js:
            print(i)