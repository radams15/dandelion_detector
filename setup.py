import sys
from cx_Freeze import setup, Executable

additional_mods = ['numpy.core._methods', "numpy.lib.format", "cv2"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "includes": additional_mods}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "dandelion_detector",
        version = "0.1",
        description = "App to count dandelions in picture",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
