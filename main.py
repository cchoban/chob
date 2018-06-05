import argparse, helpers
from core.cli import cli
from core import PackageManager

if not helpers.has_admin():
    helpers.errorMessage("You need admin permissions to be able use this program.")
    exit()

parser = argparse.ArgumentParser(description="Choban Package manager")
parser.add_argument("-S", nargs="*", help="Install package(s)")
parser.add_argument("-R", nargs="*", help="Remove package(s)")
parser.add_argument("--upgrade", nargs="*", help="Upgrade package(s)")

parser.add_argument("-Ss", type=str, help="Search packages")
parser.add_argument("--downloadScript", type=str, help="Downloads script for specific package.")
parser.add_argument("--update", action="store_true", help="Update package repo list to get updated.")
parser.add_argument("--doctor", action="store_true", help="Fixes common problems.")
parser.add_argument("--clean", action="store_true", help="Cleans caching of packages.")
parser.add_argument("-y", action="store_true", help="Skips agreements")
parser.add_argument("--packages", action="store_true", help="Lists all available packages.")

# TODO: add multiple package search
# TODO: add multiple installation of packages
# TODO: --force doing some weird things??
# TODO: add to installed list when it is installed with unzip method
parser.add_argument("-Scc", help="Clean's unused files", action="store_true")
parser.add_argument("-skipHash", help="Skips of checking hash for files", action="store_true")
parser.add_argument("--force", help="Forces a installation of package", action="store_true")
arg = parser.parse_args()

if arg.S:
    PackageManager.Manager(arg.S, arg.skipHash, arg.force, arg.y).installPackage()

if arg.R:
    PackageManager.Manager(arg.R, arg.skipHash, arg.force, arg.y).removePackage()

if arg.upgrade:
    PackageManager.Manager(arg.upgrade, arg.skipHash, arg.force, arg.y).upgradePackage()

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
