from tempfile import gettempdir
import helpers, sys
from Logger import Logger as log
from urllib.request import urlretrieve


class Http:

    def __init__(self, url, path):
        self.url = url
        self.path = path

    def reporthook(blocknum, blocksize, totalsize):

        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))

    def download(self, url, path=gettempdir(), ext="exe"):
        try:
            urlretrieve(url, path + "." + ext,self.reporthook)
        except Exception as e:
            log.new(e).logError()
            pass
