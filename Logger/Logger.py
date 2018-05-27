import logging


logging.basicConfig(filename="coban.log")

class new:
    def __init__(self, message):
        self.message = message


    def logError(self):
        logging.error(self.message)

    def logInfo(self):
        logging.info(self.message)