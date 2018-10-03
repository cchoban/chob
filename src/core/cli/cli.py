import repo
import helpers
from core import http, FileManager
from core.packageCreator import creator, pack, push, auth
from core.configurator import config
from Logger import Logger as log
from . import doctor
import re
from sys import exit

class main:

    def config(self, configFrom, configTo=None):
        if not configTo:
            return helpers.successMessage(str(config.Configurator().get_key(configFrom)))

        return config.Configurator().setConfig(configFrom, configTo)

    def confighelp(self):
        return config.Configurator().config_help()

    def packageGenerator(self, packageName, generateFlatFileOnly=False):
        if generateFlatFileOnly:
            cls = creator.generatePackage(packageName, generateFlatFileOnly)
            json = cls.generateJson()
            cls.writeToFile(json)
        else:
            cls = creator.generatePackage(packageName, False)
            cls.getAnswers()
            cls.generateJson()
            cls.writeToFile()

    def packit(self):
        return pack.main()

    def push(self):
        if auth.main().keyExists():
            return push.main()
        else:
            helpers.errorMessage(
                "You don't have authentication key. Please get one from {0}. You can activate it with --authenticate".format(helpers.getWebsite))

    def auth(self, token, force=False):
        return auth.main(token, force).init()

    def update(self):
        helpers.infoMessage("Updating repo if needed " +
                            repo.repos()["programList"])
        try:
            http.Http().download(repo.repos()[
                               "programList"], helpers.getCobanPath + "\\programList", "json")
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("cli.cli.update: "+str(e.strerror))

    def doctor(self):
        doc = doctor.doctor()
        doc.createFolders()
        doc.createFiles()
        doc.validateJsonFiles()
        self.update()
        helpers.successMessage("Fixed problems..")

    def cleanLeftOvers(self):
        fileManager = FileManager.Manager().cleanup()

    def packages(self):
        self.update()
        js = helpers.programList()
        return js

    def listPackages(self, local):
        if local == True:
            packages = helpers.installedApps()["installedApps"]
        else:
            packages = self.packages()
        for i in packages:
            print(i)

    def searchInPackages(self, packageName):
        foundPackages = []
        packages = self.packages()
        for package in packageName:
            for i in packages:
                regex = re.search(package.lower(), i.lower())

                if regex:
                    foundPackages.append(i)

        if len(foundPackages) > 0:
            helpers.successMessage("Found this package(s): ")
            for i in foundPackages:
                print(i)

    def downloadDeps(self):
        doctor.doctor().downloadDependencies()

    def downloadScript(self, packageName):
        packageUrl = helpers.programList()[packageName]+'&download=true'
        if not FileManager.Manager().fileExists(helpers.packageInstallationPath + packageName):
            FileManager.Manager().createFolder(helpers.packageInstallationPath + packageName)
        helpers.infoMessage(
            "Downloading Installation Script of: " + packageName + ".cb")

        http.Http().download(packageUrl,
                           helpers.packageInstallationPath + packageName + "\\" + packageName, "cb")
    def version(self):
        helpers.successMessage("Choban Package Manager")
        helpers.infoMessage("Version 0.5.8.2")

    def server_status(self):
        resp = http.Http().get(repo.repos()["programList"])
        if resp and resp.status_code == 200:
            return {"message": resp.content, "status_code": resp.status_code}
        else:
            return False
