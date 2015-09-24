#! /usr/bin/env python

# Some more useful tips to adopt here http://goo.gl/LbBM3D

import fnmatch
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # NOQA
import sys


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def find_package_data():
    matches = []
    dirname = 'app/'
    for root, dirnames, filenames in os.walk(dirname):
        [matches.append(os.path.join(root.replace(dirname, ''), filename))
         for filename in fnmatch.filter(filenames, '*.*')
         if filename[-3:] != '.py']

    return matches


setup(name='app',
      version='0.1.0',
      description='App for Auto Undo Test Demo',
      author='Mark S. Maglana',
      author_email='mmaglana@gmail.com',
      packages=find_packages(),
      package_data={'app': find_package_data()},
      scripts=[
          'bin/run_app_tests'
      ],
      test_suite='tests',
      tests_require=['tox'],
      cmdclass={'test': Tox},
      install_requires=[
          'Flask~=0.10.1'
      ])
