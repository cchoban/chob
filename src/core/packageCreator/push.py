from core import http, FileManager, JsonParser
import helpers
import os
import json
import requests
from core.packageCreator import pack, auth
from sys import exit


class main(pack.main):

    def __init__(self):
        self.zip = None
        self.token = auth.main().token
        self.authenticated = False
        self.packageName = None
        if self.isPackgable():
            if self.question():
                if self.zipExists():
                    if self.isAuthenticated():
                        self.pushit()

    def question(self):
        ask = helpers.askQuestion(
            "Have you tested this package before pushing to server")
        if ask:
            if not FileManager.Manager().fileExists(os.getcwd() + "\\.tested"):
                helpers.errorMessage(
                    "You have not tested it yet. Please do it first.")
                exit()
            else:
                return True

    def zipExists(self):
        for i in os.listdir(os.getcwd()):
            FileManager.Manager().fileExists(os.getcwd() + "\\" + i)
            if i.endswith(".zip"):
                self.zip = i
                self.packageName = i.split(".")[0]
                return True

    def isAuthenticated(self):
        if auth.main().keyExists():
            return True
        else:
            return False

    def pushit(self):
        headers = {
            "Authorization": "Token " + self.token,
            "cache-control": "no-cache"
        }

        zipFile = open(os.getcwd() + "\\" + self.zip, "rb")

        files = {
            "package": (self.zip, zipFile)
        }

        data = {
            "packageName": self.packageName
        }

        request = requests.post(
            "{}/api/push/".format(helpers.getWebsite), data=data, files=files, headers=headers)

        if JsonParser.Parser().is_json(request.content):
            js = json.loads(request.content)

        if request.status_code == 201:
            helpers.infoMessage(
                "You successfully submitted your package. It is now under approvement period.")
        elif request.status_code == 406:
            helpers.errorMessage(
                "We could not push your package. See error detail: \n {0}".format(js["error"]))
