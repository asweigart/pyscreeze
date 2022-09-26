import io
import os
import re
from setuptools import setup

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Load version from module (without loading the whole module)
with open("pyscreeze/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name="PyScreeze",
    version=version,
    url="https://github.com/asweigart/pyscreeze",
    author="Al Sweigart",
    author_email="al@inventwithpython.com",
    description="A simple, cross-platform screenshot module for Python 2 and 3.",
    long_description=long_description,
    license="MIT",
    packages=["pyscreeze"],
    package_data={"pyscreeze": ["pyscreeze/py.typed"]},
    test_suite="tests",
    # NOTE: Update the python_version info for Pillow as Pillow supports later versions of Python.
    install_requires=['Pillow >= 8.3.2; python_version == "3.8"',
                      'Pillow >= 8.3.2; python_version == "3.7"',
                      'Pillow >= 8.3.2; python_version == "3.6"',
                      'Pillow <= 7.2.0, >= 3.2.0; python_version == "3.5"',
                      'Pillow <= 5.4.1, >= 2.5.0; python_version == "3.4"',
                      'Pillow <= 4.3.0, >= 2.0.0; python_version == "3.3"',
                      'Pillow <= 3.4.2, >= 2.0.0; python_version == "3.2"',
                      'Pillow >= 2.0.0; python_version == "2.7"',
                      ],
    requires_python=">=2.7, !=3.0.*, !=3.1.*",  # Pillow library has never supported pre-2.7 or 3.0 or 3.1.
    keywords="screenshot screen screencap capture scrot screencapture image",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
