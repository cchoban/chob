import errno, os, winreg, re


class Registry:

    def installedSoftware():
        properties = {}
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
                             winreg.KEY_READ)
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            skey_name = winreg.EnumKey(key, i)
            skey = winreg.OpenKey(key, skey_name)
            try:
                packageName = winreg.QueryValueEx(skey, 'DisplayName')[0]
                packageUninstallString = winreg.QueryValueEx(skey, 'UninstallString')[0]
                data = {
                    packageName: packageUninstallString
                }
                properties.update(data)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # DisplayName doesn't exist in this skey
                    pass
            finally:
                skey.Close()

        # print(properties)
        return properties

    def searchForSoftware(self, packageName):
        data = {}
        for prod in self.installedSoftware():

            m = re.search(packageName.lower(), prod.lower())

            if m:
                newData = {
                    "PackageName": prod,
                    "UninstallString": self.installedSoftware()[prod]
                }

                data.update(newData)

        return data