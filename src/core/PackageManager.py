import helpers
from . import FileManager as file
from . import JsonParser as json
from . import hash
from .cli import cli
from sys import exit


class Manager:

    def __init__(self, packageName, skipHashes, force, agreements, uninstall=False):
        self.packageName = packageName
        self.oldPackageName = None
        self.skipHashes = skipHashes
        self.skipAgreements = agreements
        self.forceInstallation = force
        self.parser = json.Parser()
        self.exit_code = None
        self.install_path = ""
        self.dependencies = None
        self.uninstall = uninstall
        self.package_has_64bit = False
        self.arches = False

        if not isinstance(packageName, list):
            self.packagePathWithoutExt = helpers.packageInstallationPath + \
                                         packageName + "\\" + packageName
            self.packagePathWithExt = self.packagePathWithoutExt + ".cb"
            self.packageScriptName = self.packageName + ".cb"

            if file.Manager().fileExists(self.packagePathWithExt):
                if json.Parser(self.packagePathWithExt).isValid():
                    self.scriptFile = self.parser.fileToJson(
                        self.packagePathWithExt)["packageArgs"]

                    if self.parser.keyExists(self.scriptFile, 'downloadUrl64'):
                        self.package_has_64bit = True

    def installPackage(self):
        from .packageManager import installPackage as install
        packagename = self.packageName if not isinstance(self.packageName, list) else [
            package for package in self.packageName]

        if isinstance(self.packageName, list):
            for i in packagename:
                if not i in helpers.programList():
                    helpers.errorMessage(
                        "Package '{}' was not found on our servers. But you can push it your self with argument --create! ".format(
                            i))
                    return False
                self.packageName = i
                self.packageScriptName = i + ".cb"

                install.main(self.packageName, self.skipHashes, self.forceInstallation,
                             self.skipAgreements).installer()
        else:
            self.packageName = packagename
            self.packageScriptName = packagename + ".cb"
            install.main(self.packageName, self.skipHashes, self.forceInstallation,
                         self.skipAgreements).installer()

    def removePackage(self):
        self.uninstall = True
        from .packageManager import removePackage as remove
        packagename = self.packageName if not isinstance(self.packageName, list) else [
            package for package in self.packageName]
        if isinstance(self.packageName, list):
            for i in packagename:
                self.packageName = i
                self.packageScriptName = i + ".cb"

                remove.main(self.packageName, self.skipHashes, self.forceInstallation,
                            self.skipAgreements, self.uninstall).uninstaller()
        else:
            self.packageName = packagename
            self.packageScriptName = packagename + ".cb"
            remove.main(self.packageName, self.skipHashes, self.forceInstallation,
                        self.skipAgreements, self.uninstall).uninstaller()

    def upgradePackage(self):
        from .packageManager import upgradePackage as upgrade

        if not self.packageName:
            helpers.infoMessage('Checking for upgrades..')
            check = upgrade.main(self.packageName, self.skipHashes, self.forceInstallation,
                                 self.skipAgreements).check_upgrade_for_all_packages()

        if len(check) > 0:
            helpers.infoMessage('An update found for "{}"'.format(
                ', '.join(check)))
        else:
            helpers.successMessage('No update found for your applications.')

        if not check == True:
            self.packageName = check

        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"
            upgrade.main(i, self.skipHashes, self.forceInstallation,
                         self.skipAgreements).run()

    def testPackage(self):
        from .packageManager import testPackage
        testPackage.main(self.packageName, self.skipHashes,
                         self.forceInstallation, self.skipAgreements).test()

    def isInstalled(self, package_name=''):
        package_name = package_name or self.packageName
        if not self.forceInstallation and helpers.isInstalled(self.packageName):
            return True
        else:
            return False

    def downloadScript(self, uninstall=False):
        try:
            self.scriptFile
            self.scriptFile["softwareName"]
        except AttributeError or KeyError as e:
            cli.main().downloadScript(self.packageName)
            if not uninstall:
                self.scriptFile = self.parser.fileToJson(
                    self.packagePathWithExt)["packageArgs"]
            else:
                self.scriptFile = self.parser.fileToJson(
                    self.packagePathWithExt)

    def agreement(self, action="install"):
        if self.skipAgreements:
            return True
        return helpers.askQuestion("Do you want to " + action + " " + self.packageName)

    def checkHash(self, sandboxed=False, arches=False):
        try:
            if json.Parser().keyExists(self.scriptFile, "downloadUrl64"):
                hashedKey = self.scriptFile["checksum64"]
            else:
                hashedKey = self.scriptFile["checksum"]

            check = hash.check(hashedKey, self.packageName,
                               self.skipHashes, sandboxed, arches)

            if check:
                return True
        except KeyError as e:
            # TODO: add log
            pass

    def valid_exit_code(self):
        if not self.is_zip_package():
            if self.exit_code in self.scriptFile["validExitCodes"] or str(self.exit_code) in self.scriptFile[
                "validExitCodes"]:
                return True
            else:
                return False
        else:
            return True

    def is_zip_package(self):
        if self.parser.keyExists(self.scriptFile, 'unzip') and self.scriptFile['unzip'] == True:
            return True
        else:
            return False

    # TODO: add comments
    def set_envs(self):
        from windows import winhelpers

        if self.parser.keyExists(self.scriptFile, 'environments'):
            environments = self.scriptFile['environments']
            for env in environments:
                if not winhelpers.env_key_exists(env):
                    set_env = winhelpers.set_env(env, environments[env])

                    if not set_env:
                        helpers.infoMessage(
                            'Could not set enviroment variable.')
                else:
                    helpers.verboseMessage(
                        'Skipping creating an environment key for {}. Because it already exists.'.format(env))

    def add_to_path_env(self):
        from windows import winhelpers

        if self.parser.keyExists(self.scriptFile, 'path_env'):
            enviroments = self.scriptFile['path_env']
            for env in enviroments:
                if not winhelpers.env_path_exists(env):
                    set_env = winhelpers.add_path_env(env)

                    if not set_env:
                        helpers.infoMessage(
                            'Could not set enviroment variable.(path)')
                else:
                    helpers.verboseMessage('Skipping PATH:{}. Because it already exists.'.format(env))

    def checkForDependencies(self):
        js = self.scriptFile[
            'packageArgs'] if self.uninstall else self.scriptFile
        self.dependencies = []
        if self.parser.keyExists(js, "dependencies"):
            for i in js["dependencies"]:

                if isinstance(js["dependencies"], list) and len(js['dependencies']) > 1:
                    self.dependencies.append(i)
                else:
                    self.dependencies = i

                if i in helpers.programList() and i not in helpers.installedApps()["installedApps"]:
                    helpers.successMessage("Found dependencies: " + i)
                    self.oldPackageName = self.packageName
                    if isinstance(self.dependencies, list) and len(self.dependencies) > 1:
                        self.packageName = self.dependencies
                else:
                    if not self.uninstall:
                        helpers.infoMessage(
                            'Found {0} as dependencie(s) but it is already installed on your computer. Skipping it.'.format(
                                i))
                        self.dependencies = []
                        return True
                    else:
                        helpers.infoMessage(
                            'Found {0} as dependencie(s), will be removed as it\'s not uses from another package.'.format(
                                i))
