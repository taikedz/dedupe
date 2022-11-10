""" Required file for using this repository as a PIP dependency.
This is not a development enviornment setup script, it should NOT be run manually.
Add to your requirements.txt a line like:
    git+https://github.com/taikedz/dedupe@main
"""

# For help adjusting this file, see
# https://setuptools.pypa.io/en/latest/userguide/quickstart.html

from glob import glob
import os
import setuptools
import sys
import re

# ===================
# Configuration of setup

# Track the version in a file in your lib
# Ensure it has a "get_version()" method returning the version string
import dedupe as MYLIB

REPO_URL="https://github.com/taikedz/dedupe"

# Short description
DESCRIPTION = "Deduplicator for file trees"

# Short-name for library (used in paths, etc)
LIB_NAME = "dedupe"

# Ownership details ...
OWNER = "TaiKedz"
AUTHOR_NAME = "Tai Kedzierski"
AUTHOR_EMAIL = "dch.tai/G-MAIL"

# Any executable script files
SCRIPT_FILES = ['bin/dedupe', 'bin/dd-merge', 'bin/dd-flatten']

# Files to include during installation
CONFIG_GLOBS = ["config/*.yaml"]

# Packages (top-level dirs with a __init__.py file inside them)
#   to exclude during installation
EXCLUDE_GLOBS = ["tests"]


# note - in python2 , platform is "linux2" :-(
# Add a "requirements.{os_string}.txt" to add support for it
# e.g. "requirements.linux.txt"
SUPPORTED_OS_LIST = ("win32", "linux")

MIN_PYTHON_VERSION = "3.6"

# Load this file's content as the long-description
DESCRIPTION_FILE = "ABOUT.md"
LONG_DESCRIPTION_TYPE = "text/markdown"

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    ]

# / END OF CONFIG AREA
# ----------------------------------------------------

# ===========
# Helpers

with open(DESCRIPTION_FILE) as fh:
    LONG_DESCRIPTION = fh.read()

def uncomment_file(path:str):
    """ Read a file, ignore all blank or comment lines, return each line as an individual list item
    """
    with open(path) as fh:
        return [L.strip() for L in fh.readlines() if not re.match("^\\s*(#.*)?$", L.strip())]


def get_all_files(globs):
    all_files = []
    for pat in globs:
        all_files.extend(glob(pat))
    return all_files

# ============
# Load requirements

# Sometimes, the lib requires a specific platform to _work_
if sys.platform not in SUPPORTED_OS_LIST:
    print("WARNING - platform {} cannot install some dependencies.".format(sys.platform))
    print( "          You can still develop with {},".format(LIB_NAME))
    print( "          but your project will not run locally on this machine.")


# Anywhere this package installed, use content from requirements.txt always ...
reqtxt_list = []
if os.path.exists("requirements.txt"):
    reqtxt_list.extend(uncomment_file("requirements.txt"))


# Add special support for some OSes - e.g. deployment environments, dev environments ...
for os_string in SUPPORTED_OS_LIST:
    if sys.platform == os_string:
        req_file = "requirements.{}.txt".format(os_string)

        if os.path.isfile(req_file):
            print("--- Selecting {} dependencies ---".format(os_string))
            extras = uncomment_file(req_file)
            reqtxt_list.extend(extras)

# ==============
# Active setup routine

setuptools.setup(
    name=LIB_NAME,
    version=MYLIB.version.get_version(),

    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,

    url=REPO_URL,

    scripts=get_all_files(SCRIPT_FILES),

    project_urls={ 
        "Bug Tracker": f"{REPO_URL}/issues",
    },
    classifiers=CLASSIFIERS,
    package_dir={LIB_NAME: LIB_NAME},
    python_requires=">=".format(MIN_PYTHON_VERSION),
    install_requires=reqtxt_list,

    packages=setuptools.find_packages(exclude=get_all_files(EXCLUDE_GLOBS)),

    # Installs to f"{sys.prefix}/{dirname}" where 'dirname' is the first memebr of each tuple
    data_files=[('{}/config'.format(LIB_NAME), get_all_files(CONFIG_GLOBS))]
)