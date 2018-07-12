from tempfile import gettempdir
from Logger import Logger as log
import requests
import math
from tqdm import tqdm
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
            with open("{0}.{1}".format(path, ext), 'wb') as f:
                resp = requests.get(url, headers=headers, stream=True)
                total_size = int(resp.headers.get('content-length', 0));
                block_size = 1024
                wrote = 0
                if resp:
                    for data in tqdm(resp.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB'):
                        wrote = wrote  + len(data)
                        f.write(data)
        except Exception as e:
            log.new(e).logError()
            pass
