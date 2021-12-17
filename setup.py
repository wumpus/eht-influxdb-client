#!/usr/bin/env python

from os import path

from setuptools import setup

packages = [
    'eht-influxdb-client',
]

ztest_requirements = ['pytest', 'coverage', 'pytest-cov', 'pytest-sugar', 'coveralls']

requires = [
    'influxdb_client',  # official v2 client
]

setup_requires = ['setuptools_scm']

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description = f.read()

setup(
    name='eht-influxdb-client',
    use_scm_version=True,
    description='A client for manipualting InfluxDB monitoring of the Event Horizon Telescope'
    long_description=description,
    long_description_content_type='text/markdown',
    author='Greg Lindahl and others',
    author_email='glindahl@cfa.harvard.edu',
    url='https://github.com/wumpus/eht-influxdb-client/',
    packages=packages,
    python_requires=">=3.6.*",
    #extras_require=extras_require,
    setup_requires=setup_requires,
    install_requires=requires,
    entry_points='''
        [console_scripts]
        eht-influxdb-client = eht-influxedb-client.cli:main
    ''',
    #scripts=scripts,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Environment :: MacOS X',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        #'Programming Language :: Python :: 3.5',  # setuptools_scm problem
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
