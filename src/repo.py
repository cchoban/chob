import helpers
from os import path as os
from core import JsonParser
def repos():
    path = helpers.getCobanPath+"\\repo.json"
    json = JsonParser.Parser(path)
    if os.exists(path):
        file = json.fileToJson()
        for i in file:
            if "{cobanpath}" in file[i]:
                replaced_dict = {
                    i: file[i].replace("{cobanpath}", helpers.getCobanPath)
                }

                file.update(replaced_dict)

        return file
    else:
        return {}
