from core import JsonParser
import repo, math, os, platform, sys
from colorama import init, AnsiToWin32, Fore, Style

packageInstallationPath = os.getenv("programdata") + "\\coban\\packages\\"
getCobanPath = os.getenv("cobanPath")
getToolsPath = os.getenv("cobanTools")
getCobanBinFolder = getCobanPath + "\\lib\\"

print(getCobanBinFolder)

init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream


def errorMessage(message, logging=False):
    return print(Fore.RED + "ERROR: " + message + Style.RESET_ALL, file=stream)


def infoMessage(message):
    return print(Fore.CYAN + "INFO: " + message + Style.RESET_ALL, file=stream)


def successMessage(message):
    return print(Fore.GREEN + message + Style.RESET_ALL, file=stream)


def redColor(message):
    return print(Fore.RED + "INFO: " + message + Style.RESET_ALL, file=stream)

def alreadyInstalled(packageName):
    return infoMessage(
        "You already installed this package. You can upgrade it by 'coban upgrade " + packageName + ""
                                                                                                    "' or by adding '--force' argument to force installation")


def programList():
    js = JsonParser.Parser(repo.repos()["localProgramlist"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'coban doctor'")
        exit()


def installedApps():
    js = JsonParser.Parser(repo.repos()["localInstalledApps"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'coban doctor'")
        exit()


def dependenciesList():
    js = JsonParser.Parser(repo.repos()["dependencies"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'coban doctor'")
        exit()


def isInstalled(packageName):
    if packageName in installedApps():
        return False
    else:
        return True


def has_admin():
    if os.name == 'nt':
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
            return True
        except:
            return False
        else:
            return False


def is_os_64bit():
    if platform.machine().endswith('64'):
        return True
    else:
        return False


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
