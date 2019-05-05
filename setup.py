import sys
#from cx_Freeze import setup, Executable
from esky import bdist_esky
from distutils.core import setup

from esky.bdist_esky import Executable

additional_mods = ['numpy.core._methods', "numpy.lib.format"]

build_exe_options = {"includes": additional_mods,
                     "freezer_module": "cxfreeze"}

setup(  name = "dandelion_detector",
        version = "0.1",
        description = "App to count dandelions in picture",
        options = {"bdist_esky": build_exe_options},
        scripts = [Executable("main.py")])
