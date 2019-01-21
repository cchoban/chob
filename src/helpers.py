from core import JsonParser
import repo
import math
import os
import platform
import sys
from Logger import Logger as log
from core.configurator import config


try:
    from colorama import init, AnsiToWin32, Fore, Style

    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
except ModuleNotFoundError as e:
    log.new(e).logError()

packageInstallationPath = os.getenv("programdata") + "\\choban\\packages\\"
getCobanPath = os.getenv("chobanPath")
getToolsPath = os.getenv("chobanApps")
getCobanBinFolder = getCobanPath + "\\lib\\"
getWebsite = repo.repos().get('website')
sslFile = os.path.join(getCobanPath, 'ssl.crt')


def errorMessage(message, logging=False):
    return print(Fore.RED + "ERROR: " + message + Style.RESET_ALL, file=stream)


def infoMessage(message):
    return print(Fore.CYAN + "INFO: " + message + Style.RESET_ALL, file=stream)

def verboseMessage(message):
    if is_verbose():
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
    """
    Returns downloadable application list.
    :return dict:
    """
    return JsonParser.Parser().fileToJson(repo.repos()["localProgramlist"])


def installedApps():
    """
    Returns installed softwares.
    :return dict:
    """
    return JsonParser.Parser().fileToJson(repo.repos()["localInstalledApps"])


def symlinkList():
    """
    Return saved symlinks.
    :return dict:
    """
    return JsonParser.Parser().fileToJson(repo.repos()["symlink"])


def isInstalled(packageName):
    """
    Checks if package is already installed.
    :return bool:
    """
    if packageName in installedApps()["installedApps"]:
        return True
    else:
        return False


def has_admin():
    """
    Checks if user runs Choban with administration rights.
    :return bool:
    """
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
    """
    Checks if users computer are 64bit
    :return bool:
    """
    if platform.machine().endswith('64'):
        return True
    else:
        return False


def askQuestion(question):
    """
    Asks question to user.
    :param question: Question to be asked user.
    :return bool:
    """
    if config.Configurator().get_key('skipQuestionConfirmations', True):
        infoMessage("Skipping agreements because 'skipQuestionConfirmations' is set to 'true'.")
        return True

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
    """
    Check if verbose mode is turned on.
    :return bool:
    """
    if "--verbose" in sys.argv:
        return True
    else:
        return False


def slugify(s):
    import re
    """
    Simplifies ugly strings into something URL-friendly.
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '')

    return s
