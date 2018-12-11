from subprocess import call, DEVNULL, PIPE
from Logger import Logger as log
from helpers import is_verbose, errorMessage, getCobanPath
from os import environ, path


def __reload_environ():
    """
    Reloads environments variables.
    """
    path = getCobanPath + '\\refreshenv.ps1'
    set_path = call('powershell -Command ". {}'.format(path), stdout=DEVNULL, stderr=DEVNULL)


def set_env(env_key: str, env_value: str):
    """
    Sets enviroment variable for Windows enviroment.

    :param env_key: Enviroment key name: string
    :param env_value: Enviroment key value: string

    :return bool:
    """
    try:
        env_set = call(
            'cmd /c setx {} {}'.format(env_key, env_value),
            stdout=DEVNULL,
            stderr=DEVNULL)

        if env_set == 0:
            __reload_environ()
            return True
        else:
            return False
    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.set_env: ' + str(e))
        return False


def remove_env(env_key: str):
    """
    Removes enviroment variable for Windows enviroment.

    :param env_key: Enviroment key name: string
    :return bool:
    """
    try:
        path = getCobanPath + '\\powershell\\setenv.ps1'
        env_set = call(
            'powershell -Command ". {}; RemoveEnv -env_name \'{}\'"'.format(
                path, env_key))

        if env_set == 0:
            __reload_environ()
            return True
        else:
            return False

    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.remove_env: ' + str(e))
        return False


def remove_from_path(env_path: str):
    """
    Remove directory from PATH enviroment key.

    :param env_path: Path to be removed from PATH environment.
    :return bool:
    """

    try:
        path = getCobanPath + '\\powershell\\setenv.ps1'
        set_path = call(
            'powershell -Command ". {}; RemoveFromPath -env_value \'{}\'"'.
            format(path, env_path))

        if set_path == 0:
            __reload_environ()
            return True
        else:
            return False
    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.remove_from_path: ' + str(e))
        return False


def add_path_env(env_value: str):
    """
    Add directory to PATH enviroment key.

    :param env_value: Path to be added PATH environment.
    :return bool:
    """

    try:
        path = getCobanPath + '\\powershell\\setenv.ps1'
        set_path = call(
            'powershell -Command ". {}; AddToPath -env \'{}\'"'.format(
                path, env_value))

        if set_path == 0:
            __reload_environ()
            return True
        else:
            return False
    except Exception as e:
        log.new(e).logError()
        if is_verbose():
            errorMessage('winheplers.add_path_env: ' + str(e))
        return False


def env_key_exists(env_name: str):
    """
    Check if environment key exists.

    :param env_name: Environment key name to check if it exists or not.
    :return bool:
    """
    if environ.get(env_name):
        return True
    else:
        return False


def env_path_exists(env_value: str):
    """
    Checks if env_value is already exists in PATH environment.

    :param env_value: Path to be checked in PATH enviroment.
    :return bool:
    """
    path = environ.get('PATH').split(';')
    if env_value in path:
        return True
    else:
        return False
