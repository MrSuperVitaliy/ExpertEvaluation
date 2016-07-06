import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_msvcr": True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup( name = "ExpertAssessment",
       version = "0.1",
       description = "Ваше описание",
       options = {"build_exe": build_exe_options},
       executables = [Executable("E:\my_documents\Dropbox\Projects\Python\ExpertAssessment\source34\launcher.py", base=base)])