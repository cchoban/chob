from helpers import getCobanPath, getToolsPath, infoMessage, askQuestion
from core import FileManager, JsonParser
import pip
from sys import exit


class doctor:

    def __init__(self):
        self.folders = {
            "packages": getCobanPath + "\\packages",
            "lib": getCobanPath + "\\lib",
            "chobanapps": getToolsPath,
            'powershell': getCobanPath + '\\powershell'
        }

        self.files = {
            "programList": getCobanPath + "\\programList.json",
            "packages": getCobanPath + "\\packages.json",
            "symlinks": getCobanPath + "\\symlinks.json",
            'config': getCobanPath + '\\config.json',
            'whof': getCobanPath + '\\powershell\\whof.ps1',
            'env': getCobanPath + '\\powershell\setenv.ps1',
            'repo': getCobanPath + '\\repo.json',
            'refreshenv': getCobanPath + '\\refreshenv.ps1'
        }

    def createFolders(self):
        file = FileManager.Manager()

        for i in self.folders:
            if not file.fileExists(self.folders[i]):
                infoMessage("Created: " + i)
                file.createFolder(self.folders[i])

    def validateJsonFiles(self):
        file = FileManager.Manager()
        for i in self.files:
            json = JsonParser.Parser(self.files[i])
            if file.fileExists(self.files[i]) and i.endswith('.json'):
                if not json.isValid():
                    if askQuestion(
                            'Do you want to rewrite {} file. (You might lose your settings based on which file you rewritting.)'
                            .format(i)):
                        infoMessage("Fixed: " + i)
                        json.rewriteJson()
            else:
                self.createFiles()

    def createFiles(self):
        file = FileManager.Manager()

        for i in self.files:
            if not file.fileExists(self.files[i]):
                infoMessage("Created: " + i)
                if i in self.file_contents():
                    file.createFile(self.files[i], self.file_contents()[i])
                else:
                    file.createFile(self.files[i])

    def downloadDependencies(self):
        dependencies = ["colorama", "requests", "tqdm"]
        for i in dependencies:
            pip.main(["install", i])

    def file_contents(self):
        __config = {
            "skipHashByDefault": {
                'help': 'Skipping checking of hash(s) if enabled.',
                'value': False
            },
            "skipQuestionConfirmations": {
                'help': 'Skip agreements [Y/N].',
                'value': False
            },
            "auth_key": {
                'help': 'Authentication key to connect with Choban services.'
            }
        }

        __refreshenv = """$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")"""
        __whof = """if (!(Test-Path Variable:PSScriptRoot)) {$PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent}$path = join-path "$env:chobanApps" "{packageExecutable}"; if($myinvocation.expectingInput) { $input | & $path  @args } else { & $path  @args }"""
        __set_env = """function AddToPath($env) {$path = [Environment]::GetEnvironmentVariable("PATH", "User"); $new_path = $path+";"+$env; $addPath = [Environment]::SetEnvironmentVariable("PATH", $new_path, [EnvironmentVariableTarget]::User)}
        function RemoveFromPath($env_value) {$path = [System.Environment]::GetEnvironmentVariable('PATH','User');$path = ($path.Split(';') | Where-Object { $_ -ne $env_value }) -join ';';[System.Environment]::SetEnvironmentVariable('PATH',$path,'User')}
        function RemoveEnv($env_name) { [Environment]::SetEnvironmentVariable($env_name,$null,"User") }
        """
        __repo = {
            "localProgramlist": "{cobanpath}\\programList.json",
            "localInstalledApps": "{cobanpath}\\packages.json",
            "symlink": "{cobanpath}\\symlinks.json",
            "programList": "https://choban.herokuapp.com/packages/repo",
            "_website": "http://localhost:8000",
            "website": "https://choban.herokuapp.com"
        }

        files = {
            "config": JsonParser.Parser().dump_json(__config, True),
            'whof': __whof,
            'repo': JsonParser.Parser().dump_json(__repo, True),
            'env': __set_env,
            'refreshenv': __refreshenv
        }

        return files


# TODO: add os path if choban is there or not
