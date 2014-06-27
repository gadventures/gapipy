#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gapipy

from setuptools import setup, find_packages


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'requests',
]

test_requirements = [
    'mock',
    'nose',
    'nose-parameterized',
]

setup(
    name='gapipy',
    version=gapipy.__version__,
    description='Python client for the G Adventures REST API',
    long_description=readme + '\n\n' + history,
    author='G Adventures',
    author_email='software@gadventures.com',
    url='https://github.com/gadventures/gapipy',
    packages=find_packages(),
    package_dir={'gapipy': 'gapipy'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='gapipy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements,
)
