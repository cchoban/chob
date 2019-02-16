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
subparser = parser.add_subparsers()

# Install command
install = subparser.add_parser('install')
install.add_argument('install', help="Install package(s)", nargs="*")
install.add_argument('--force', action="store_true")
install.add_argument("-y", action="store_true", help="Skips agreements")
install.add_argument(
    "--skip-hash", help="Skips of checking hash for files", action="store_true")
install.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")

#Uninstall command
remove = subparser.add_parser('remove')
remove.add_argument('remove', help="Uninstall package(s)", nargs="*")
remove.add_argument("-y", action="store_true", help="Skips agreements")
remove.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
#Upgrade command
upgrade = subparser.add_parser('upgrade')
upgrade.add_argument('upgrade', help="Upgrade package(s)", nargs="*")
upgrade.add_argument('--force', action="store_true")
upgrade.add_argument("-y", action="store_true", help="Skips agreements")
upgrade.add_argument(
    "--skip-hash", help="Skips of checking hash for files", action="store_true")
upgrade.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")

#Config command
config = subparser.add_parser('config')
config.add_argument("config", type=str, help="Configurator")
config.add_argument("--set", type=str, help="Configurator")
config.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")

#Create command
create = subparser.add_parser('create')
create.add_argument("create", type=str, help="Generates package for you")
create.add_argument("--flatfile", action="store_true")
create.add_argument(
    "--template",
    type=str,
    help="Generates package from an template from Choban website. (Package name)"
)
create.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")

#Test package command
test_package = subparser.add_parser('testpackage')
test_package.add_argument(
    "testpackage",
    type=str,
    help=
    "This command helps you to test your package before you push to our servers."
)
test_package.add_argument('--force', action="store_true")
test_package.add_argument("-y", action="store_true", help="Skips agreements")
test_package.add_argument(
    "--skip-hash", help="Skips of checking hash for files", action="store_true")
test_package.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
#Authenticate command
auth = subparser.add_parser('authenticate')
auth.add_argument(
    'authenticate',
    type=str,
    help="Your API Token key to push packages to our servers.")
auth.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
auth.add_argument('--force', action="store_true")

#Push command
push = subparser.add_parser('push')
push.add_argument(
    "push", action="store_true", help="Push your package via this command.")
push.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
#Packs the package for testing it
packit = subparser.add_parser('packit')
packit.add_argument(
    "packit", action="store_true", help="Push your package via this command.")
packit.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
#Clean command
clean = subparser.add_parser('clean')
clean.add_argument("clean", action="store_true", help="Clean cache of Choban.")

#Search command
search = subparser.add_parser('search')
search.add_argument("search", nargs="*", help="Search for package(s)")

#Update command
update = subparser.add_parser('update')
update.add_argument(
    "update",
    action="store_true",
    help="Update available package list on your system.")

#Doctor command
doctor = subparser.add_parser('doctor')
doctor.add_argument(
    "doctor", action="store_true", help="Fixes common problems.")

#Old but gold.
parser.add_argument("-S", help="Install package(s)", nargs="*")
parser.add_argument("-R", help="Uninstall package(s)", nargs="*")
parser.add_argument(
    "--packages", action="store_true", help="Lists all available packages.")
parser.add_argument("--download-chob-dependencies", action="store_true")
parser.add_argument(
    "--downloadScript", type=str, help="Downloads script for specific package.")
parser.add_argument("--local", action="store_true")
parser.add_argument(
    "--verbose", action="store_true", help="Turning on verbose mode")
parser.add_argument("--version", action="store_true")
parser.add_argument("--help-config", action='store_true', help="Configurator")
arg = parser.parse_args()

skip_hash = arg.skip_hash if hasattr(arg, 'skip_hash') else False
force = arg.force if hasattr(arg, 'force') else False
agreement = arg.y if hasattr(arg, 'y') else False

if hasattr(arg, 'install') or arg.S:
    package_name = arg.install if hasattr(arg, 'install') else arg.S
    PackageManager.Manager(package_name, skip_hash, force,
                           agreement).installPackage()

if hasattr(arg, 'remove') or arg.R:
    package_name = arg.remove if hasattr(arg, 'remove') else arg.R
    PackageManager.Manager(package_name, skip_hash, force, agreement,
                           True).removePackage()

if hasattr(arg, 'upgrade'):
    package_name = arg.upgrade
    PackageManager.Manager(package_name, skip_hash, force,
                           agreement).upgradePackage()

if hasattr(arg, 'config') and not hasattr(arg, 'set'):
    cli.main().config(arg.config)

if hasattr(arg, 'config') and hasattr(arg, 'set'):
    cli.main().config(arg.config, arg.set)

if hasattr(arg, 'create'):
    flatfile = arg.flatfile if hasattr(arg, 'flatfile') else False
    template = arg.template if hasattr(arg, 'template') else False
    cli.main().packageGenerator(arg.create, flatfile, template)

if hasattr(arg, 'push') and arg.push:
    cli.main().push()

if hasattr(arg, 'packit') and arg.packit:
    cli.main().packit()

if hasattr(arg, 'authenticate'):
    cli.main().auth(arg.authenticate, arg.force)

if hasattr(arg, 'clean') and arg.clean:
    cli.main().cleanLeftOvers()

if hasattr(arg, 'search'):
    cli.main().searchInPackages(arg.search)

if hasattr(arg, 'update') and arg.update:
    cli.main().update()

if hasattr(arg, 'doctor') and arg.doctor:
    cli.main().doctor()

if hasattr(arg, 'testpackage'):
    PackageManager.Manager(arg.testpackage, arg.skip_hash, arg.force,
                           arg.y).testPackage()

if arg.packages:
    cli.main().listPackages(arg.local)

if arg.downloadScript:
    cli.main().downloadScript(arg.downloadScript)

if arg.download_chob_dependencies:
    cli.main().downloadDeps()

if arg.help_config:
    cli.main().confighelp()

if arg.version:
    cli.main().version()
