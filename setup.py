'''
Contains informations necessaries to build, release and install a distribution.

Reference: https://github.com/fernandojunior/python-boilerplate
'''
import os
import shutil
from setuptools import setup
from pip.req import parse_requirements as parse

# Parse a requirements file to string list
requirements = lambda f: [str(i.req) for i in parse(f, session=False)]

SCRIPT_NAME = 'trains'

setup_attrs = dict(
    name='trains',
    version='0.0.1',
    author='Fernando Felix do Nascimento Junior',
    description='ThoughtWorks Trains Solution.',
    platforms='any',
    py_modules=[SCRIPT_NAME],
    scripts=[SCRIPT_NAME],
    install_requires=requirements('requirements.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
    ],  # see more at https://pypi.python.org/pypi?%3Aaction=list_classifiers
    zip_safe=False
)

try:
    shutil.copyfile(SCRIPT_NAME + '.py', SCRIPT_NAME)
    setup(**setup_attrs)
finally:
    os.remove(SCRIPT_NAME)
