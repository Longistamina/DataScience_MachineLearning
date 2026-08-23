'''
project = package = application = software

# ========================================================================================
# Step 1: activate the Python virtual environment (venv) that the project depends on
# ========================================================================================

conda activate venv_name
source /path/to/venv_name/bin/activate
source /path/to/venv_name/bin/activate.fish # for fishell's users

# Activating the venv so that PyInstaller can resolve dependencies while compiling

# ========================================================================================
# Step 2: cd to the directory of the project
# ========================================================================================

cd /path/to/project

# ========================================================================================
# Step 3: use Pyinstaller to compile your ``*.py`` file
# ========================================================================================
# Conventionally, the ``main.py`` stores the logic of the whole program

pyinstaller /path/to/main.py
pyinstaller /path/to/file_to_compile.py
pyinstaller /path/to/compile_me.py

# ========================================================================================
# Step 4: examine the ``build`` directory, ``dist`` directory and ``*.spec`` file
# ========================================================================================
After running ``pyinstaller /path/to/main.py``,
it will produce 3 things in your project directory:
+ ``build`` directory
+ ``dist`` directory
+ ``*.spec`` file

``build`` directory is the temporary workspace where PyInstaller stores intermediate files, logs, and caching data
while analyzing your code and resolving dependencies. You can safely delete this folder once the compilation is finished.

``dist`` directory is the distribution folder that contains your final, ready-to-run application.
Depending on your compilation flags, this will either hold a single standalone executable file
or a folder containing the executable alongside its required internal libraries.
This is the application you will actually share with your end users.

``*.spec`` file is the configuration file (written in Python syntax) that acts as a blueprint for your build.
It saves the command-line options you used and allows for advanced customizations,
like bundling external data files, including hidden imports, or adjusting windowed modes.
For future compilations, you can simply run ``pyinstaller main.spec`` instead of typing out all your command-line arguments again.

# ========================================================================================
# Example with ``compile_me.py``
# ========================================================================================

# Assume you already activated the venv

cd /path/to/05_Numba_PyInstaller_PythonCompilers/02_PyInstaller
pyinstaller ./compile_me.py

# or just ``pyinstaller compile_me.py``
'''
