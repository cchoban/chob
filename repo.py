import helpers

def repos():
    return {
        "localProgramlist": helpers.getCobanPath+"\\programList.json",
        "localInstalledApps": helpers.getCobanPath+"\\packages.json",
        "programList": "https://gitlab.com/muhammedkpln/coban-packages/raw/master/programList.json"
    }