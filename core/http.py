from tempfile import gettempdir
from Logger import Logger as log
import requests
import math
from tqdm import tqdm
import helpers
from core.cli import cli
class Http:

    def __init__(self, url="", path=""):
        self.url = url
        self.path = path

    def download(self, url, path=gettempdir(), ext="exe"):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        try:
            resp = requests.get(url, headers=headers, stream=True)
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
                    print(sv["message"])
            exit()

    def get(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        try:
            resp = requests.get(url, headers=headers)
            return resp
        except Exception as e:
            log.new(e).logError()
            helpers.errorMessage("Cannot request the server, for more information please use '--verbose'")
            if helpers.is_verbose():
                helpers.errorMessage(str(e))