from core import PackageManager
from core.cli import cli
from core.packageManager import installPackage, removePackage
import helpers


class main(PackageManager.Manager):

    def run(self):
        cli.main().downloadScript(self.packageName)

        if self.isInstalled():
            if self.__checkForUpgrade():
                helpers.successMessage(
                    "Upgrade found for {0}. Upgrading {0} to version {1}".format(self.packageName, self.packageVersion))
                self.upgrade()

            else:
                helpers.infoMessage("There is no update for this package right now.")
        else:
            helpers.messages("error", "isNotInstalled", self.packageName)

    def __checkForUpgrade(self):
        self.currentVersion = helpers.installedApps()["installedApps"][self.packageName]["version"]
        self.packageVersion = self.scriptFile["version"]

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
