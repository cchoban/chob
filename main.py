import argparse, helpers
from core.cli import cli
from core.packageManager import installPackage, removePackage

if not helpers.has_admin():
    helpers.errorMessage("You need admin permissions to be able use this program.")
    exit()


parser = argparse.ArgumentParser(description="Coban Package manager")
parser.add_argument("-S", type=str, help="Install a package")
parser.add_argument("--update", action="store_true", help="Update package repo list to get updated.")
parser.add_argument("--doctor", action="store_true", help="Fixes common problems.")
parser.add_argument("--clean", action="store_true", help="Cleans caching of packages.")

# parser.add_argument("-Ss", nargs='+', help="install a package")
#TODO: add multiple installation of packages
#TODO: --force doing some weird things??
parser.add_argument("-R", type=str, help="Remove a package")
parser.add_argument("-Scc", help="Clean's unused files", action="store_true")
parser.add_argument("-skipHash", help="Skips of checking hash for files", action="store_true")
parser.add_argument("--force", help="Forces a installation of package", action="store_true")
arg = parser.parse_args()



if arg.S:
    installPackage.main(arg.S, arg.skipHash, arg.force).installer()

if arg.R:
    removePackage.main(arg.R, arg.skipHash, arg.force).uninstaller()

if arg.doctor:
    cli.main().doctor()

if arg.update:
    cli.main().update()

if arg.clean:
   cli.main().cleanLeftOvers()
   
# elif arg.cmd == "install":
#     packageInstallation(arg.cmd)
# elif arg.cmd == "remove":
#     removingPackage(arg.cmd)

