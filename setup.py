"""Setup for breakword."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='breakword',
    version='0.1.2',

    description='Mixing breakpoints with print debugging.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/breuleux/breakword',

    author='Olivier Breuleux',
    author_email='breuleux@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='debug breakpoint print',

    packages=find_packages(exclude=['contrib', 'doc', 'tests']),

    install_requires=[],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
    },

    python_requires='>=3.7',
)
