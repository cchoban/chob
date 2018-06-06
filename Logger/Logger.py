import logging, helpers


class new:
    def __init__(self, message):
        self.message = message
        self.path = helpers.getCobanPath + "\\choban.log"
        logging.basicConfig(filename=self.path)

    def logError(self):
        logging.error(self.message)

    def logInfo(self):
        logging.info(self.message)
