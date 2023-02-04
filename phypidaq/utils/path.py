import os
import platform


def get_user_home() -> str:
    """
    Method to get the platform dependent user home directory.
    :return: String with the absolute path to the home directory
    """
    if platform.system() == "Windows":
        return os.getenv('USERPROFILE')
    else:
        return os.getenv('HOME')
