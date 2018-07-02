import helpers

def repos():
    return {
        "localProgramlist": helpers.getCobanPath+"\\programList.json",
        "localInstalledApps": helpers.getCobanPath+"\\packages.json",
        "symlink": helpers.getCobanPath+"\\symlinks.json",
        "programList": "http://localhost:8000/packages/repo",
        "website": "http://localhost:8000"
    }