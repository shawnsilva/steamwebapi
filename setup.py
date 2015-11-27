#!/usr/bin/env python

from setuptools import setup

import steamwebapi

setup(name='steamwebapi',
      version=steamwebapi.__version__,
      description='Steam API Wrapper',
      author='Shawn Silva',
      author_email='ssilva@jatgam.com',
      url='https://github.com/shawnsilva/steamwebapi',
      packages=['steamwebapi'],
      long_description='Steam API Wrapper',
      license='GNU GPL v3',
      platforms='Unix, Windows',
      test_suite='steamwebapi.test',
     )