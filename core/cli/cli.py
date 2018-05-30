import repo, helpers
from core import http, FileManager
from . import doctor
class main:
    def __init__(self):
        pass


    def update(self):
        helpers.infoMessage("Updating repo "+repo.repos()["programList"])
        http.Http.download(http.Http, repo.repos()["programList"], helpers.getCobanPath+"\\programList", "json")

    def doctor(self):
        self.update()
        doc = doctor.doctor()
        doc.createFolders()
        doc.validateJsonFiles()

        helpers.successMessage("Fixed problems..")

    def cleanLeftOvers(self):
        fileManager = FileManager.Manager().cleanup()

