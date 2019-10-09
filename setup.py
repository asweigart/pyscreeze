import re
from setuptools import setup

# Load version from module (without loading the whole module)
with open('pyscreeze/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

# Read in the README.md for the long description.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyScreeze',
    version=version,
    url='https://github.com/asweigart/pyscreeze',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description='A simple, cross-platform screenshot module for Python 2 and 3.',
    long_description=long_description,
    license='BSD',
    packages=['pyscreeze'],
    test_suite='tests',
    install_requires=['Pillow'],
    requires_python='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*', # Copied from the Pillow library, since PyScreeze is built on top of it.
    keywords="screenshot screen screencap capture scrot screencapture image",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
         # Copied from the Pillow library, since PyScreeze is built on top of it:
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)