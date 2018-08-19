from core import JsonParser
import repo
import math
import os
import platform
import sys
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
            "alreadyInstalled": "You already installed this package. You can upgrade it by 'chob --upgrade " + packageName + ""                                                                                                        "' or by adding '--force' argument to force installation"
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
    return JsonParser.Parser().fileToJson(repo.repos()["localProgramlist"])


def installedApps():
    return JsonParser.Parser().fileToJson(repo.repos()["localInstalledApps"])


def symlinkList():
    return JsonParser.Parser().fileToJson(repo.repos()["symlink"])


def isInstalled(packageName):
    if packageName in installedApps()["installedApps"]:
        return True
    else:
        return False


def has_admin():
    if os.name == 'nt':
        try:
            temp = os.listdir(os.sep.join(
                [os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
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


def askQuestion(question):
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    text = infoMessage(question+"? [Y/N]")

    if not "-y" in sys.argv:
        choice = input("").lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            sys.exit("Please respond with 'yes' or 'no'")
    else:
        return True


def is_verbose():
    if "--verbose" in sys.argv:
        return True
    else:
        return False
