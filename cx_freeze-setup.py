from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
#os.environ['TCL_LIBRARY'] = "C:\\Users\\Agranya Pratap Singh\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY'] = "C:\\Users\\Agranya Pratap Singh\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"
print(PYTHON_INSTALL_DIR)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}
setup(options = options,
      name = "AutoMail" ,
      version = "1.0" ,
      description = "" ,
      executables = [Executable("final.py")])
