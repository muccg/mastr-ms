#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(name='yaphc',
      version='0.1.2',
      description='Yet Another Python Http Client',
      author='Tamas Szabo',
      author_email='szabtam AT google\'s mail service',
      url='http://code.google.com/p/yaphc/',
      install_requires='httplib2',
      packages=setuptools.find_packages(exclude=['tests']),
     )
