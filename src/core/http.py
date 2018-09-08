from tempfile import gettempdir
from Logger import Logger as log
import requests
import math
from tqdm import tqdm
import helpers
from core.cli import cli
from sys import exit


class Http:
    __headers = {'User-Agent': 'Googlebot/2.1',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                 'Accept-Language': 'en-US,en;q=0.5',
                 'Connection': 'keep-alive',
                 'cache-control': 'no-cache'
                 }
    def __init__(self, custom_headers=False):
        self.custom_headers=custom_headers

    def download(self, url, path=gettempdir(), ext="exe"):
        """
        Downloading file from url.
        :param url: URL to download file from.
        :param path: Path to save downloaded file.
        :param ext: File to save with custom extension.
        """
        headers = self.__headers
        try:
            resp = requests.get(url, headers=headers, stream=True)

            if resp.status_code == 404:
                helpers.errorMessage('Server returned a broken link. Skipping this package as it\'s broken.')
                if helpers.is_verbose():
                    helpers.errorMessage('Http.download: Server returned 404 status code ({}).'.format(url))
                exit()
            with open("{0}.{1}".format(path, ext), 'wb') as f:
                total_size = int(resp.headers.get('content-length', 0));
                block_size = 1024
                wrote = 0
                if resp:
                    for data in tqdm(resp.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB'):
                        wrote = wrote  + len(data)
                        f.write(data)
        except requests.exceptions.ConnectionError as e:
            log.new(e).logError()
            helpers.errorMessage("Could not download the requested file. Please try again later.")
            sv = cli.main().server_status()
            if sv == False:
                helpers.errorMessage("The server is not accessible at this time.")
            else:
                if helpers.is_verbose():
                    helpers.errorMessage("Http.download: "+str(e))
                    print(sv["message"])
            exit()

    def get(self, url, **args):
        """
        Sending GET Requests.
        :param url: URL to send GET request.
        """

        if args.get('headers') and not self.custom_headers:
            args['headers'] = {**args.get('headers'), **self.__headers}

        try:
            resp = requests.get(url, **args)
            return resp
        except Exception as e:
            log.new(e).logError()
            helpers.errorMessage("Cannot request the server, for more information please use '--verbose'")
            if helpers.is_verbose():
                helpers.errorMessage(str(e))

    def post(self, url, **args):
        """
        Sending POST Requests.
        :param url: URL to send POST request.
        """

        if args.get('headers') and not self.custom_headers:
            args['headers'] = {**args.get('headers'), **self.__headers}

        try:
            self.resp = resp = requests.post(url, **args)
            return resp
        except Exception as e:
            log.new(e).logError()
            helpers.errorMessage(
                "Cannot request the server, for more information please use '--verbose'")
            if helpers.is_verbose():
                helpers.errorMessage(str(e))

    def json():
        """
        Converting json response to dict.
        :return dict
        """
        import json
        if self.resp:
            if JsonParser.Parser().is_json(self.resp.content):
                js = json.loads(request.content)
                return js
