#!/usr/bin/python3

# --- BEGIN COPYRIGHT BLOCK ---
# Copyright (C) 2020
#
# Authors:
#   Simon Pichugin <simon.pichugin@gmail.com>
#   Dinesh Prasanth M K <dmoluguw@redhat.com>
#
# All rights reserved.
#
# License: GPL (version 3 or any later version).
# See LICENSE for details.
# --- END COPYRIGHT BLOCK ---

#
# A setup.py file
#

from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

version = "0.1"

with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='pagure2github',
    license='GPLv3+',
    version=version,
    description='A simple tool for Pagure issues to Github issues migration',
    long_description=long_description,
    url='https://github.com/SilleBille/pagure2github/',
    author='Dinesh Prasanth M K',
    author_email='dmoluguw@redhat.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Tool',
        'Topic :: Software Development :: Migration'],

    keywords='Pagure issues to Github issues migration',
    packages=['pagure2github'],
    package_dir={'': 'lib', },

    scripts=['cli/pagure2github'],

    install_requires=[
        'pygithub',
        'libpagure',
        'python-bugzilla',
        'argcomplete',
        'argparse-manpage',
        'setuptools',
        ],
)
