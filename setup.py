#!/usr/bin/env python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (C) 2013-2015  Shawn Silva
# ------------------------------------
# This file is part of steamwebapi.
#
# steamwebapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"""Setuptools installer for steamwebapi"""

from setuptools import setup

import steamwebapi

def long_description():
      with open('README.rst') as f:
            readme = f.read()
      with open('CHANGELOG.rst') as f:
            changelog = f.read()
      return readme + changelog

setup(name='steamwebapi',
      version=steamwebapi.__version__,
      description='Steam API Wrapper',
      author='Shawn Silva',
      author_email='ssilva@jatgam.com',
      url='https://github.com/shawnsilva/steamwebapi',
      packages=['steamwebapi'],
      long_description=long_description(),
      keywords='steam valve api web user group profile',
      license='GNU GPL v3',
      platforms='Unix, Windows',
      test_suite='steamwebapi.test',
      classifiers=[
            'Development Status :: 4 - Beta',

            'Intended Audience :: Developers',

            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',

            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Internet',
      ],
     )
