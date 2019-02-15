import errno, winreg, re, helpers
from Logger import Logger as log
from sys import exit


class Registry:

    def __init__(self):
        self.key64 = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        self.key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    def installedSoftware(self):
        """
        Returns all installed softwares including installation for both arch types.

        :return dict: A list of softwares with their uninstall string.
        """

        data = {}
        data.update(self.CurrUninstaller(self.key))
        data.update(self.CurrUninstaller(self.key64))

        return data

    def CurrUninstaller(self, key):
        """
        Looking for software installed on the system.

        :param key: Registry key to looking for softwares.
        :return dict: A list of softwares with their uninstall string.
        """

        properties = {}
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            skey_name = winreg.EnumKey(key, i)
            skey = winreg.OpenKey(key, skey_name)
            try:
                packageName = winreg.QueryValueEx(skey, 'DisplayName')[0]
                packageUninstallString = winreg.QueryValueEx(
                    skey, 'UninstallString')[0]
                data = {packageName: packageUninstallString}
                properties.update(data)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # DisplayName doesn't exist in this skey
                    pass
            finally:
                skey.Close()

        return properties

    def searchForSoftware(self, packageName):
        """
        Searching for a software from dictionary (self.installedSoftware())

        :param packageName: Software/Package name to looking for.
        :return dict: Returns dict if something is found.
        """

        data = {}
        for prod in self.installedSoftware():
            try:
                prod_slugged = helpers.slugify(prod)
                packageName = helpers.slugify(packageName)

                m = re.search(packageName.lower(), str(prod_slugged.lower()))

                if m:
                    newData = {
                        "PackageName": prod,
                        "UninstallString": self.installedSoftware()[prod]
                    }
                    data.update(newData)
                    return data
            except Exception as e:
                log.new(e).logError()
                pass
