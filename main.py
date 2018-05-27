import argparse
import helpers
from core import PackageManager

if not helpers.has_admin():
    helpers.errorMessage("You need admin permissions to be able use this program.")
    exit()


parser = argparse.ArgumentParser(description="Coban Package manager")
parser.add_argument("-S", type=str, help="install a package")
parser.add_argument("-R", type=str, help="Remove a package")
parser.add_argument("-Scc", help="Clean's unused files", action="store_true")
parser.add_argument("-skipHash", help="Skips of checking hash for files", action="store_true")
parser.add_argument("--force", help="Forces a installation of package", action="store_true")
arg = parser.parse_args()

programList = helpers.programList()
installedList = helpers.installedApps()
dependenciesList = helpers.dependenciesList()



if not arg.S == None:
    packageManager = PackageManager.Manager(arg.S, arg.skipHash, arg.force)
    packageManager.installPackage()

if not arg.R == None:
    packageManager = PackageManager.Manager(arg.R, arg.skipHash)
    PackageManager.Manager.removePackage()


# if not arg.R == None:
#     removePackage(arg.R)
#
# if not arg.Scc == None:
#     clean()

# def installPackage(packageName):
#     deps = packageName + "-dependencies"
#     if isInstalled(packageName):
#         if packageName in programList:
#             programUrl = programList[packageName]
#             download(programUrl, packageInstallationDir + packageName)
#             helpers.infoMessage("Downloaded " + packageName)
#             installDependencies(packageNa me)
#     else:
#         helpers.errorMessage("This package is already installed on your computer.")
#         exit()
# #
#

#
#
# def installDependencies(packageName):
#     deps = packageName + "-dependencies"
#     dependencies = {}
#     try:
#         if programList[deps]:
#             for depName in programList[deps]:
#                 if depName in programList:
#                     programList[deps].pop(depName)
#                     download(programList[depName], packageInstallationDir + depName)
#                     helpers.infoMessage("Downloaded: " + depName)
#
#                     if depName + "-dependencies" in programList:
#                         for depens in programList[depName + "-dependencies"]:
#                             download(programList[depName + "-dependencies"][depens], packageInstallationDir + depens)
#                             helpers.infoMessage("Downloaded: " + depens)
#
#                     super(installDependencies(packageName))
#
#                 download(programList[deps][depName], packageInstallationDir + depName)
#                 helpers.infoMessage("Downloaded " + depName)
#
#                 sa = {
#                     depName: packageInstallationDir + depName
#                 }
#                 dependencies.update(sa)
#
#         print(dependencies)
#         # updateList(installedList, packageName, dependencies)
#
#     except Exception as e:
#         print(e)
#         # Logger.exception(e)
#
#
# def removePackage(packageName):
#     # TODO: fix removing of dependencies
#     if not isInstalled(packageName):
#         programDesinition = installedList[packageName]
#         print(programDesinition)
#         if os.path.exists(programDesinition):
#             os.remove(programDesinition)
#             removeDependencies(packageName)
#             updateList(installedList, packageName)
#             helpers.successMessage("Successfully removed " + packageName, True)
#         else:
#             exit("We could not detect installation folder of " + packageName)
#
#     else:
#         exit("This program is not installed")
#
#
# def removeDependencies(packageName):
#     packageDependencies = packageName + "-dependencies"
#     dependenciesNeedsToBeRemoved = programList[packageName + "-dependencies"]
#     print("Sarching for dependencies...")
#     for i in programList:
#         if not i == packageName or i == packageDependencies:
#             if not i.find("-dependencies") == -1 and not i == packageDependencies:
#                 deps = programList[i]
#
#     dependenciesToBeDeleted = {}
#     for row in dependenciesNeedsToBeRemoved:
#         dependenciesToBeDeleted.update({
#             row: row
#         })
#
#     for row in deps:
#         if row in dependenciesNeedsToBeRemoved:
#             dependenciesToBeDeleted.pop(row)
#
#     for file in dependenciesToBeDeleted:
#         try:
#             helpers.infoMessage("Removed: " + file)
#             os.remove(packageInstallationDir + file)
#         except Exception as e:
#             return True
#
#     return True
#
#
# def removeFromJson(list, packageName):
#     removeKey = list.pop(packageName)
#     deps = packageName + "-dependencies"
#
#     return list
#
#
# def addToInstalledPackages(list, packageName):
#     list[packageName] = packageInstallationDir + packageName
#
#     return list
#
#
# def addDependencies(packageName, deps={}):
#     for i in deps:
#         if i in dependenciesList:
#             return True
#         else:
#             newList = {
#                 i: packageInstallationDir + i
#             }
#
#             dependenciesList.update(newList)
#
#         try:
#             helpers.rewriteFile(dependenciesListPath, json.dumps(dependenciesList))
#         except Exception as e:
#             exit("olmadi: " + e)
#
#
# def updateList(list, packageName, deps={}):
#     try:
#         modifiedList = removeFromJson(list, packageName)
#     except Exception as e:
#         modifiedList = addToInstalledPackages(list, packageName)
#         addDependencies(packageName, deps)
#
#     try:
#         helpers.rewriteFile(installedAppsListPath, json.dumps(modifiedList))
#     except Exception as e:
#         exit(e)
#
#
# def clean():
#     installedPackages = os.listdir(packageInstallationDir)
#     for packages in installedPackages:
#         if packages in dependenciesList:
#             print(packages)
#
#

