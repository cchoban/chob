from core import PackageManager, FileManager as file, JsonParser
from core.cli import cli
from core.packageManager import installPackage, removePackage
import helpers
from distutils.version import LooseVersion
from sys import exit


class main(PackageManager.Manager):

    def run(self):
        cli.main().downloadScript(self.packageName)
        self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)["packageArgs"]

        if self.isInstalled():
            if self.__checkForUpgrade():
                helpers.successMessage(
                    "Upgrade found for {0}. Upgrading {0} to version {1}".format(self.packageName, self.packageVersion))
                self.upgrade()

            else:
                helpers.infoMessage("There is no update for this package right now.")
        else:
            helpers.messages("error", "isNotInstalled", self.packageName)

    def check_upgrade_for_all_packages(self):
        installed_packages = JsonParser.Parser(
            helpers.getCobanPath + '\\packages.json').fileToJson().get('installedApps')
        search_for_packages = []
        online_version = {}
        update_packages = []

        for name in installed_packages:
            search_for_packages.append(name)
            installation_file_path = '{0}\\packages\\{1}\\{1}.cb'.format(helpers.getCobanPath, name)

            if not file.Manager().fileExists(installation_file_path):
                cli.main().downloadScript(name)

            installation_file = JsonParser.Parser(installation_file_path).fileToJson()['packageArgs']

            s = {
                name: {
                    'packageArgs': installation_file
                }
            }

            online_version.update(s)

        for installed in installed_packages:
            for online in online_version:
                if installed == online:
                    latest_version = LooseVersion(
                        online_version[online]['packageArgs'].get('version'))
                    current_version = LooseVersion(
                        installed_packages[installed].get('version'))
                    if latest_version > current_version:
                        update_packages.append(installed)
                    else:
                        pass

        return update_packages

    def __checkForUpgrade(self):
        self.currentVersion = LooseVersion(helpers.installedApps()["installedApps"][self.packageName]["version"])
        self.packageVersion = LooseVersion(self.scriptFile["version"])

        if self.currentVersion < self.packageVersion:
            return True
        else:
            return False

    def __removePackage(self):
        removePackage.main(self.packageName, self.skipHashes, self.forceInstallation, True).uninstaller()

    def __installPackage(self):
        installPackage.main(self.packageName, self.skipHashes, self.forceInstallation, True).installer()

    def upgrade(self):
        self.__removePackage()
        self.__installPackage()
