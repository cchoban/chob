import helpers

def repos():
    return {
        "localProgramlist": helpers.getCobanPath+"\\programList.json",
        "localInstalledApps": helpers.getCobanPath+"\\packages.json",
        "dependencies": "C:/Users/Muhammed Kaplan/Desktop/coban-package-manager/dependencies.json",
        "programList": "http://www.mrmkaplan.com/programList.json"
    }