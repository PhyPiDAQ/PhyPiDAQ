"""
.. module:: _version_info
   :platform: python 3.6+
   :synopsis: Version 1.5.0rc0 of phypidaq, released Aug. 2024

.. moduleauthor:: Guenter Quast <guenter.quast@online.de>
"""

major = 1
minor = 5
revision = 0
suffix = 'rc0'  # for suffixes such as 'rc' or 'beta' or 'alpha'


def _get_version_tuple():
    """
    version as a tuple
    """
    return major, minor, revision


def _get_version_string():
    """
    version as a string
    """
    return "%d.%d.%d" % _get_version_tuple() + suffix
