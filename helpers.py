from core import JsonParser
import repo, math, os, platform, sys
from Logger import Logger as log

try:
    from colorama import init, AnsiToWin32, Fore, Style

    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
except ModuleNotFoundError as e:
    log.new(e).logError()

packageInstallationPath = os.getenv("programdata") + "\\choban\\packages\\"
getCobanPath = os.getenv("chobanPath")
getToolsPath = os.getenv("chobanTools")
getCobanBinFolder = getCobanPath + "\\lib\\"


def errorMessage(message, logging=False):
    return print(Fore.RED + "ERROR: " + message + Style.RESET_ALL, file=stream)


def infoMessage(message):
    return print(Fore.CYAN + "INFO: " + message + Style.RESET_ALL, file=stream)


def successMessage(message):
    return print(Fore.GREEN + message + Style.RESET_ALL, file=stream)


def redColor(message):
    return print(Fore.RED + "INFO: " + message + Style.RESET_ALL, file=stream)


def messages(type, template, packageName):
    messages = {
        "info": {
            "alreadyInstalled": "You already installed this package. You can upgrade it by 'chob upgrade " + packageName + ""                                                                                                        "' or by adding '--force' argument to force installation"
        },

        "error": {
            "isNotInstalled": packageName + " is not installed on your computer."
        }
    }

    if type in messages and template in messages[type]:
        if type == "error":
            return errorMessage(messages["error"][template])
        elif type == "info":
            return infoMessage(messages["info"][template])
    else:
        log.new("Messages: Key does not exists").logError()


def programList():
    js = JsonParser.Parser(repo.repos()["localProgramlist"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'choban doctor'")
        exit()


def installedApps():
    js = JsonParser.Parser(repo.repos()["localInstalledApps"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'choban doctor'")
        exit()


def dependenciesList():
    js = JsonParser.Parser(repo.repos()["dependencies"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        errorMessage("JSON is not valid! Please run 'choban doctor'")
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
