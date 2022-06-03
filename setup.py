# -*- coding: utf-8 -*-

"""
Example of how to use setuptools
"""

__version__ = "1.0.0"

from setuptools import setup, find_packages


# Read description from README file.
def long_description():
    from os import path
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


def get_depends():
    with open('requirements.txt') as f:
        return f.read().splitlines()


# 使用 unittest 测试框架
import unittest
def get_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    name="devops_monitor",
    long_description=long_description(),

    # Command line: "python setup.py --version" to get the version number.
    version=__version__,
    
    ### exclude directories or modules:
    # `exclude` means to find project files in all other directories except tests and test directories.
    packages=find_packages(
        exclude=['tests', 'test']
    ),
    # You can also directly specify that only certain directories are packaged
    #   packages=['submodule1', 'submodule2']
    # But module1/submoduleA and module/submoduleB will not be included. If you want to include its subdirectories, you need to change it to:
    #   packages=find_packages(), or explicitly list the path of each submodule。
    #
    ### Packaing format：
    # 1）wheel format（Recommanded, supported by: `pip install twine`）：
    # package command：`python setup.py egg_info -bDEV bdist_wheel rotate -m.egg -k3`
    # Package file name：{dist}-{version}(-{build})?-{python_version}-{abi}-{platform}.whl
    #
    # Or `egg` format (easy_install standard)
    # Package command：`python setup.py egg_info -bDEV bdist_egg rotate -m.egg -k3`
    #
    # `egg_info` argument list detail packaging information.
    # wheel only works with `.py` file , If you want add other file to the package, the folling argument：
    #
    # `package_data` is used to include non-code files under `submodule/subdirectory`.
    # It is mainly used for packaging the internal data of the module. The files are finally installed in the `site` directory.
    #
    # `data_files` can contain arbitrary paths, including additional data files in the root directory. It is mainly used for files 
    # that need to be modified according to the installation environment, such as configuration.
    data_files=[
        # Parameter format: (directory name in package file, [path in source code]).
        ('conf', ['conf/config.properties']),
    ],
    # These files in `wheel` format will be packaged into `[package]/<package_name-version>.data/data/` path, for example, 
    # `conf/conf.properties` will be packaged into `[package]/<package_name-version>.data/data/conf/config.properties`. The `conf` 
    # in the path is specified by the first element in the tuple.
    #
    # The files in the `egg` format are packaged directly into `/conf/config.properties` in the package root directory, and the `conf` 
    # in the directory is specified by the first element in the tuple.
    #
    # `pip install` installs data (not module) files into the `$PYTHONPATH/conf/config.properties` directory. The `conf` in the path 
    # is specified by the first element of the tuple.
    #
    # pip can install wheel format but not egg files. Egg is installed by `python -m easy_install dist/xxx.egg`.
    #
    # 2）tar.gz Format
    # Packaging command: `python setup.py egg_info -bDEV sdist rotate -m.egg -k3`
    #
    # `MANIFEST.in` is used to list the files that need to be packaged. You can specify any file, such as the file README.md in the project root directory.
    #
    # MANIFEST.in does not work with formats such as wheel. It only takes effect for the `sdist` packing parameter. Data (non-module) files are installed 
    # into the `.venv/conf/conf.properties` directory.
    #

    install_requires=get_depends(),

    # python setup.py test
    test_suite='setup.get_test_suite',
)
