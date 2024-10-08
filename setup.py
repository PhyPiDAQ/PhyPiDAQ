"""
Setup script for the phypidaq module.

This setup includes the test runner for the module and the setup class for
package information
"""

import sys
from setuptools import setup


pkg_name = "phypidaq"
# import _version_info from package
sys.path[0] = pkg_name
import _version_info

_version = _version_info._get_version_string()


setup(
    name=pkg_name,
    version=_version,
    author='Guenter Quast',
    author_email='Guenter.Quast@online.de',
    packages=[
        pkg_name,
        pkg_name + '.sensors',
        pkg_name + '.utils',
        pkg_name + '.doc',
        pkg_name + '.images',
    ],
    include_package_data=True,
    package_data={pkg_name: ['PhyPiDemoData.csv', 'images/*', 'doc/*']},
    scripts=['phypi.py', 'run_phypi.py'],
    classifiers=[
        'Development Status :: 5 - stable',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    url='https://github.com/PhyPiDAQ',
    license='MIT BSD 2-Clause',
    description='Data AcQuisition and analysis for Physics education with Raspberry Pi',
    long_description=open('README.md').read(),
    setup_requires=["NumPy >= 1.13.3", "SciPy >= 0.18.1", "matplotlib >= 2.0.0"],
)
