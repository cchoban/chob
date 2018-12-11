import errno, winreg, re, helpers
from Logger import Logger as log
from sys import exit


class Registry:
    def __init__(self):
        self.key64 = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        self.key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    def installedSoftware(self):
        data = {}
        data.update(self.CurrInstaller(self.key) if self.CurrInstaller(self.key) else {})
        data.update(self.CurrUninstaller(self.key) if self.CurrUninstaller(self.key) else {})
        data.update(self.CurrUninstaller(self.key64) if self.CurrUninstaller(self.key64) else {})

        return data

    def CurrUninstaller(self, key):
        properties = {}
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, i)
                skey = winreg.OpenKey(key, skey_name)

                packageName = winreg.QueryValueEx(skey, 'DisplayName')[0]
                packageUninstallString = winreg.QueryValueEx(skey, 'UninstallString')[0]
                data = {
                    packageName: packageUninstallString
                }
                properties.update(data)

                skey.Close()
                return properties

        except Exception as e:
            log.new(e).logError()


    def CurrInstaller(self, key):
        properties = {}
        key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)

            for i in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, i)
                skey = winreg.OpenKey(key, skey_name)
                install_properties = winreg.OpenKey(skey, 'InstallProperties')

                packageName = winreg.QueryValueEx(install_properties, 'DisplayName')[0]
                packageUninstallString = winreg.QueryValueEx(install_properties, 'UninstallString')[0]
                data = {
                    packageName: packageUninstallString
                }
                properties.update(data)

                skey.Close()
                return properties

        except Exception as e:
            log.new(e).logError()


    def searchForSoftware(self, packageName):
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
