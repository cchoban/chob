import argparse, helpers
from core.cli import cli
from core.packageManager import installPackage, removePackage, upgradePackage
from core import PackageManager

if not helpers.has_admin():
    helpers.errorMessage("You need admin permissions to be able use this program.")
    exit()

parser = argparse.ArgumentParser(description="Coban Package manager")
parser.add_argument("-S", type=str, help="Install a package")
parser.add_argument("--upgrade", type=str, help="Upgrades package")
parser.add_argument("-Ss", type=str, help="Search packages")
parser.add_argument("--downloadScript", type=str, help="Downloads script for specific package.")
parser.add_argument("--update", action="store_true", help="Update package repo list to get updated.")
parser.add_argument("--doctor", action="store_true", help="Fixes common problems.")
parser.add_argument("--clean", action="store_true", help="Cleans caching of packages.")
parser.add_argument("-y", action="store_true", help="Skips agreements")
parser.add_argument("--packages", action="store_true", help="Lists all available packages.")

# parser.add_argument("-Ss", nargs='+', help="install a package")
# TODO: add multiple installation of packages
# TODO: --force doing some weird things??
parser.add_argument("-R", type=str, help="Remove a package")
parser.add_argument("-Scc", help="Clean's unused files", action="store_true")
parser.add_argument("-skipHash", help="Skips of checking hash for files", action="store_true")
parser.add_argument("--force", help="Forces a installation of package", action="store_true")
arg = parser.parse_args()

if arg.S:
    installPackage.main(arg.S, arg.skipHash, arg.force, arg.y).installer()

if arg.upgrade:
    upgradePackage.main(arg.upgrade, arg.skipHash, arg.force, arg.y).run()

if arg.R:
    removePackage.main(arg.R, arg.skipHash, arg.force, arg.y).uninstaller()

if arg.doctor:
    cli.main().doctor()

if arg.update:
    cli.main().update()

if arg.clean:
    cli.main().cleanLeftOvers()

if arg.packages:
    cli.main().listPackages()

if arg.Ss:
    cli.main().searchInPackages(arg.Ss)

if arg.downloadScript:
    cli.main().downloadScript(arg.downloadScript)
