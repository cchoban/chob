from core import http, FileManager, JsonParser
import helpers
import os
import json
import requests
from core.packageCreator import pack, auth
from sys import exit


class main(pack.main):

    def __init__(self):
        self.json = None
        self.token = auth.main().readToken()
        self.authenticated = False
        self.packageName = None
        if self.isPackgable():
            if self.question():
                if self.isAuthenticated():
                    self.readScript()
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

    def get_image(self):
        image_from_scr = self.json['server'].get('icon')

        if image_from_scr:
            path = os.path.join(os.getcwd(), image_from_scr)
            if FileManager.Manager().fileExists(path):
                return image_from_scr
            else:
                helpers.errorMessage('Could not get image "{}" in "{}"'.format(image_from_scr, path))
                return self.detectImage()


    def detectImage(self):
        helpers.infoMessage('Trying to find image via detector..')

        for i in os.listdir(os.getcwd()):
            if i.endswith('.jpg') or i.endswith('.jpeg') or i.endswith('.png'):
                helpers.successMessage('Found {} as image.'.format(i))
                self.json.get('server')['icon'] = i
                return i

    def isAuthenticated(self):
        if auth.main().keyExists():
            return True
        else:
            return False

    def readScript(self):
        for i in os.listdir(os.getcwd()):
            FileManager.Manager().fileExists(os.getcwd() + "\\" + i)
            if i.endswith(".cb"):
                path = os.path.join(os.getcwd(), i)
                self.json = JsonParser.Parser(path).fileToJson()
                self.packageName = i.split(".")[0]
                return True

    def pushit(self):

        headers = {
            "Authorization": "Token " + self.token,
            "cache-control": "no-cache"
        }

        image = open(os.getcwd() + '\\' + self.get_image(), 'rb')
        files = {
            'packageIcon': image
        }

        dump = JsonParser.Parser().dump_json
        data = {
            "packageName": self.packageName,
            "packageArgs": dump(self.json.get('packageArgs')),
            "packageUninstallArgs": dump(self.json.get('packageUninstallArgs')),
            "server": dump(self.json.get('server'))
        }



        post_url = "{}/api/push/".format(helpers.getWebsite)
        resp = http.Http(True).post(
            post_url, headers=headers, files=files, data=data)

        if resp.status_code == 201:
            helpers.infoMessage(
                "You successfully submitted your package. It is now under approvement period.")

        elif resp.status_code == 406:
            helpers.errorMessage(
                "We could not push your package. See error detail: \n {0}".format(resp.json().get('error')))

        elif resp.status_code == 401:
            helpers.errorMessage('Please provide correct authentication key.')
        else:
            helpers.errorMessage(
                'Something happened... Please try again later..')
            if helpers.is_verbose():
                errors = {
                    'error_code': resp.status_code,
                    'response': resp.content,
                    'error': resp.json().get('error'),
                    'success': resp.json().get('success')
                }

                print(errors)
                return False
