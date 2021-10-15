
import maya.mel as mm
import maya.cmds as cmds
import os, sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSettings

PROCEDURES = 'procedures'
FORBID_LIST = [PROCEDURES, 'pvCreatePSDposes', 'pvImportAllModules', 'an_scriptManager', 'an_scriptManager2', ".idea", ".git"]


def scriptManager(path=""):
    p_menu = 'an_menu'
    if cmds.menu (p_menu, exists=True):  cmds.deleteUI (p_menu)
    cmds.menu (p_menu, l='Scripts', p='MayaWindow', tearOff=True)
    if not path:
        path = QSettings("scriptManager", "Settings").value("path")
    if path:
        sourceProcedures (os.path.abspath(path))
        checkContent(path, p_menu)
        print 'Script manager loading scripts from: ', path
    cmds.menuItem(divider=True, p=p_menu)
    cmds.menuItem("set path", l="Set path to scripts folder", p=p_menu, c='set_path()')

def set_path():  # action = "reset" - reset path manually

    path = QtWidgets.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
    QSettings("scriptManager", "Settings").setValue("path", path)
    scriptManager(path)
    #QSettings("scriptManager", "Settings").remove("path")

def sort_path(path):
    directories = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d!=".git"  ])
    files_py = sorted([f[:-3] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-3:]=='.py' ])
    files_mel = sorted([f[:-4] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-4:]=='.mel' ])
    return directories, files_py, files_mel

def get_folders_path(rootDir, fld):
       global procPath
       for lists in os.listdir(rootDir):
           path = os.path.join(rootDir, lists)
           if lists==fld:
               procPath = os.path.abspath(path)
           if os.path.isdir(path):
               get_folders_path(path, fld)

def sourceProcedures (path):
    global procPath
    procPath = ''
    get_folders_path(path, 'procedures')
    if procPath:
        directories, files_py, files_mel = sort_path(procPath)
        if not procPath  in list(sys.path):
            sys.path.insert(0, procPath )

def checkContent (path, p_menu):
    directories, files_py, files_mel = sort_path(path)
    for fld in [d for d in directories if not d in FORBID_LIST]:
        cmds.menuItem ( fld+"name", l=fld, tearOff=True, sm=True, p=p_menu)
        if os.listdir(os.path.join(path, fld)) :
            checkContent ( os.path.join(path, fld) , fld+"name" )

    if directories: cmds.menuItem (divider=True,  p=p_menu)

    for p_file in [d for d in files_py if not d in FORBID_LIST]:
        norm = os.path.join(path, p_file+ '.py')
        mc = 'run_python(r"'+norm+'")'
        cmds.menuItem ( p_file, l=p_file, p=p_menu, c= mc  )

    for m_file in  [d for d in files_mel if not d in FORBID_LIST]:
        cmds.menuItem ( m_file, l=m_file, p=p_menu , c= r'run_mel(" {}\{}.mel")'.format(path, m_file).replace( '\\', '/' ))

def run_mel(data):
    mm.eval( r'source "'+ data[1:]+'"'   )
    fl = data.split("/")[-1].split(".")[0]
    mm.eval( fl )

def run_python(data):
    data = os.path.abspath(data )
    path = os.path.dirname(data)
    fl, ex = os.path.basename(data).split(".")
    system_paths = list(sys.path)
    if not path in system_paths:
        sys.path.insert(0, path)
    cmds.evalDeferred('from '+ fl +' import *; '+fl+'()')

def get_defoult_scripts_dir():
    scriptPath = os.environ['MAYA_SCRIPT_PATH']
    for path in scriptPath.split(";"):
        if "Documents/maya/scripts" in path:
            return path
    return None

scriptManager()
