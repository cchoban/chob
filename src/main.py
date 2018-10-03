import argparse
import helpers
from core.cli import cli
from core import PackageManager
from sys import argv, exit

if len(argv) == 1:
    exit("""
        Choban package manager
        Type chob -h to get some help.
    """)


if not helpers.has_admin():
    exit("You need admin permissions to be able use this program.")

parser = argparse.ArgumentParser(description="Choban Package manager")
parser.add_argument("-S", nargs="*", help="Install package(s)")
parser.add_argument("--install", nargs="*", help="Install package(s)")

parser.add_argument("-R", nargs="*", help="Remove package(s)")
parser.add_argument("--remove", nargs="*", help="Remove package(s)")


parser.add_argument("--upgrade", nargs="*", help="Upgrade package(s)")
parser.add_argument("--test-package", type=str,
                    help="This command helps you to test your package before you push to our servers.")
parser.add_argument("-Ss", nargs="*", help="Search packages")
parser.add_argument("--downloadScript", type=str,
                    help="Downloads script for specific package.")
parser.add_argument("--update", action="store_true",
                    help="Update package repo list to get updated.")
parser.add_argument("--doctor", action="store_true",
                    help="Fixes common problems.")
parser.add_argument("--clean", action="store_true",
                    help="Cleans caching of packages.")
parser.add_argument("-y", action="store_true", help="Skips agreements")
parser.add_argument("--packages", action="store_true",
                    help="Lists all available packages.")
parser.add_argument("--download-chob-dependencies", action="store_true")
parser.add_argument("-Scc", help="Clean's unused files", action="store_true")
parser.add_argument(
    "-skipHash", help="Skips of checking hash for files", action="store_true")
parser.add_argument(
    "--force", help="Forces a installation of package", action="store_true")
parser.add_argument("--local", action="store_true")
parser.add_argument("--create", type=str, help="Generates package for you")
parser.add_argument("--flatfile", action="store_true")
parser.add_argument("--packit", action="store_true")
parser.add_argument("--push", action="store_true")
parser.add_argument("--authenticate", type=str, help="Your token key")
parser.add_argument("--config", type=str, help="Configurator")
parser.add_argument("--help_config", action='store_true', help="Configurator")
parser.add_argument("--set", type=str, help="Configurator")
parser.add_argument("--verbose", action="store_true",
                    help="Turning on verbose mode")
parser.add_argument("--version", action="store_true")
arg = parser.parse_args()


if arg.S or arg.install:
    package_name = arg.S if arg.S else arg.install
    PackageManager.Manager(package_name, arg.skipHash,
                           arg.force, arg.y).installPackage()

if arg.test_package:
    PackageManager.Manager(arg.test_package, arg.skipHash,
                           arg.force, arg.y).testPackage()

if arg.R or arg.remove:
    package_name = arg.R if arg.R else arg.remove
    PackageManager.Manager(package_name, arg.skipHash,
                           arg.force, arg.y, True).removePackage()

if arg.upgrade:
    PackageManager.Manager(arg.upgrade, arg.skipHash,
                           arg.force, arg.y).upgradePackage()

if arg.doctor:
    cli.main().doctor()

if arg.update:
    cli.main().update()

if arg.clean:
    cli.main().cleanLeftOvers()

if arg.packages:
    cli.main().listPackages(arg.local)

if arg.Ss:
    cli.main().searchInPackages(arg.Ss)

if arg.downloadScript:
    cli.main().downloadScript(arg.downloadScript)

if arg.download_chob_dependencies:
    cli.main().downloadDeps()

if arg.create:
    cli.main().packageGenerator(arg.create, arg.flatfile)

if arg.packit:
    cli.main().packit()

if arg.push:
    cli.main().push()

if arg.authenticate:
    cli.main().auth(arg.authenticate, arg.force)

if arg.config and not arg.set:
    cli.main().config(arg.config)

if arg.help_config:
    cli.main().confighelp()

if arg.config and arg.set:
    cli.main().config(arg.config, arg.set)

if arg.version:
    cli.main().version()
