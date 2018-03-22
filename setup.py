#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup

with open('README.rst') as readme:
    documentation = readme.read()

setup(
    name = 'huefs',
    version = '0.0.1a1',

    description = 'Philips Hue as a FUSE filesystem',
    long_description = documentation,
    author = 'Daniel K Lyons',
    author_email = 'fusion@storytotell.org',
    license = 'MIT',
    py_modules=['huefs'],
    url = 'http://github.com/fusiongyro/huefs',
    keywords = 'fuse hue',
    install_requires = ['fusepy>=2.0.4,<3', 'phue>=1.0.0,<2'],

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Filesystems',
        'Topic :: Home Automation'
    ],

    entry_points = {
        'console_scripts': [
            'huefs = huefs.huefs:main'
        ]
    }
)