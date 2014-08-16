#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'TracMention',
    version = '0.0.1',
    author = 'Jellyfrog',
    url = 'https://github.com/Jellyfrog/TracMention',
    description = 'Plugin to send a notification to the mentioned person',
    license = 'BSD',
    packages=['tracmention'],
    entry_points={'trac.plugins': ['TracMention = tracmention']},
)