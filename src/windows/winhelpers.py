from subprocess import call, DEVNULL
from Logger import Logger as log
from helpers import is_verbose, errorMessage, getCobanPath
from os import environ, path


def set_env(env_key: str, env_value: str):
    """
    Sets enviroment variable for Windows enviroment.

    :param env_key: Enviroment key name: string
    :param env_value: Enviroment key value: string

    :return bool:
    """
    try:
        env_set = call('cmd /c setx {} {}'.format(env_key,
                                                  env_value), stdout=DEVNULL, stderr=DEVNULL)

        if env_set == 0:
            return True
        else:
            return False
    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.set_env: ' + str(e))
        return False


def add_path_env(env_value: str):
    """
    Add directory to PATH enviroment key.

    :param env_value: Path to be added PATH enviroment.
    :return bool:
    """

    try:
        path = getCobanPath+'\\powershell\\setenv.ps1'
        print('powershell -Command ". {} -env {}"'.format(path, env_value))
        set_path = call('powershell -Command ". {}; AddToPath -env \'{}\'"'.format(path, env_value))
        if set_path == 0:
            return True
        else:
            return False
    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.add_path_env: ' + str(e))
        return False
