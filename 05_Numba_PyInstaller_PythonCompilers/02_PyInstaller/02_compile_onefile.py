'''
In case we don't need the ``build`` and ``dist`` directories,
we just need the executable (and perhaps the ``*.spec`` file too),
what should we do?
=> Use these commands

# ================================================================================
# Keep both executable and ``*.spec`` file, no ``build`` and ``dist``
# ================================================================================

pyinstaller --onefile --distpath . --workpath /tmp /path/to/main.py

# The ``build`` folder will go to /tmp/project/, deleted after shutting down computer
# ``--distpath .`` flag will produce the executable here without ``dist``, like ``/project/executable``, not /project/dist/executable
# The ``*.spec`` file still stays in the same directory as the executable file

# ===============================================================================
# Keep only the executable file
# ================================================================================

pyinstaller --onefile --distpath . --workpath /tmp --specpath /tmp /path/to/main.py

# The ``--specpath /tmp`` flag forces the ``*.spec`` file to be in the /tmp directory instead of your project directory.
# Combined with ``--workpath /tmp`` and ``--distpath .``, your project folder will remain completely clean.
# You will be left with strictly the final executable file right where you ran the command.

# ========================================================================================
# Example with ``compile_me.py``
# ========================================================================================

# Assume you already activated the venv

cd /path/to/05_Numba_PyInstaller_PythonCompilers/02_PyInstaller
pyinstaller ./compile_me.py

pyinstaller --onefile --distpath . --workpath /tmp --specpath /tmp ./compile_me.py
'''
