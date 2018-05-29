from core import JsonParser
import repo, math, os, platform
from Logger import Logger as log


packageInstallationPath = os.getenv("programdata")+"\\coban\\packages\\"
getCobanPath = os.getenv("cobanPath")
getToolsPath = os.getenv("cobanTools")
getCobanBinFolder = getCobanPath+"\\lib\\"

print(getCobanBinFolder)
class colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


def errorMessage(message, logging = False):
    if not logging == False:
        log.new(message).logError()

    return print(colors.fg.red+colors.bold+"ERROR: "+message+colors.reset)

def infoMessage(message, logging = False):
    if not logging == False:
        log.new(message).logInfo()
    return print(colors.fg.lightblue+colors.bold+"INFO: "+message+colors.reset)

def successMessage(message):
    return print(colors.fg.green+colors.bold+message+colors.reset)

def redColor(message):
    return print(colors.fg.red+colors.bold+message+colors.reset)

def programList():
    js = JsonParser.Parser(repo.repos()["localProgramlist"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        exit(colors.bg.red + "JSON is not valid! Please run 'coban doctor'" + colors.reset)

def installedApps():
    js = JsonParser.Parser(repo.repos()["localInstalledApps"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        exit(colors.bg.red + "JSON is not valid! Please run 'coban doctor'" + colors.reset)


def dependenciesList():
    js = JsonParser.Parser(repo.repos()["dependencies"])

    if js.isValid() == True:
        return js.fileToJson()
    else:
        exit(colors.bg.red+"JSON is not valid! Please run 'coban doctor'"+colors.reset)

def isInstalled(packageName):
    if packageName in installedApps():
        return False
    else:
        return True


def has_admin():
    if os.name == 'nt':
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
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