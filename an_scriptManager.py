#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Procedure:
    scriptManager()

Creation Date:
    march 27, 2020

Authors:
    Belyaev Andrey
    andreikin@mail.ru
    
Description:
    Creates a menu "Scripts" and loads a hierarchy of scripts into it.

Installation:
    
    1. Edit the constant PATH in the code if you want to load scripts 
       from the necessary folder, while the second variable SCRIPTS_FOLDER should be empty: 
      
            PATH = r'D:\Project\scripts'
            SCRIPTS_FOLDER = r''
       
    2. If you want to load scripts from the folder ../my documents/maya/scripts/ 
       do not specify any paths: 
       
            PATH = r''
            SCRIPTS_FOLDER = r''

    
    3. If you want to load scripts from the folder located inside ../my documents/maya/scripts/riggingTools
       specify its name in the SCRIPTS_FOLDER variable, and do not specify any paths in PATH :
           
            PATH = r''
            SCRIPTS_FOLDER = r'riggingTools'
    
    4 Edit the constant PROCEDURES in the code if you want add its path to systems paths
    
    5. Save the an_scriptManager.py to your local user/scripts folder
	                   example: ../my documents/maya/scripts/
    
	6. Add a few lines to the file userSetup.py:
	    
            	    import maya.cmds as cmds
                    cmds.evalDeferred('from an_scriptManager import *')
	
	7. Start Maya	    
 
Comments or suggestions? E-mail me!!!
Good luck!!!

*************************************************************************************************************************
 version History
*************************************************************************************************************************
	v2.0
	- Edit an_sourceProcedures
	- Edit discription
	- Find procedures in hierarhy
	- Add script description.
	- Completed the second version
*************************************************************************************************************************
 Modify at your own risk
"""

import maya.mel as mm
import maya.cmds as cmds
import os, sys

PATH = r"D:/Distributiv/scripts" 
SCRIPTS_FOLDER = ''
PROCEDURES = 'procedures'
FORBID_LIST = [PROCEDURES, 'pvCreatePSDposes', 'pvImportAllModules', 'an_scriptManager', 'an_scriptManager2']

def scriptManager(path ='', scriptFolder=''):
    p_menu = 'an_menu'
    if cmds.menu (p_menu, exists=True):  cmds.deleteUI (p_menu)
    cmds.menu (p_menu, l='Scripts', p='MayaWindow', tearOff=True)
    if not path:
        if __name__ == '__main__':
            path = os.path.abspath('C:\Users\Mi\Documents\maya\scripts')
        else:
            path = os.path.split(str(os.path.abspath(__file__)))[0]+'\\'
    else: 
        path = os.path.abspath(path)
    
    if scriptFolder: 
        path =  os.path.join(path, scriptFolder)
    print 'Script manager loading scripts from: ', path
    an_sourceProcedures (os.path.abspath(path))
    an_checkContent (path, p_menu)

def sort_path(path):
    directories = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d!=".git"  ]) 
    files_py = sorted([f[:-3] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-3:]=='.py' ])
    files_mel = sorted([f[:-4] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-4:]=='.mel' ])
    return directories, files_py, files_mel

#path = r"D:/Distributiv/3d/scripts" 

def an_sourceProcedures (path):
    global procPath  
    procPath = '' 
    def get_folders_path(rootDir, fld): 
           global procPath
           for lists in os.listdir(rootDir):
               path = os.path.join(rootDir, lists) 
               if lists==fld:  
                   procPath = os.path.abspath(path)
               if os.path.isdir(path):
                   get_folders_path(path, fld)
    
    get_folders_path(path, 'procedures') 
    if procPath:
        directories, files_py, files_mel = sort_path(procPath)
        if not procPath  in list(sys.path):
            sys.path.insert(0, procPath )
            

def an_checkContent (path, p_menu):
    directories, files_py, files_mel = sort_path(path)
    for fld in [d for d in directories if not d in FORBID_LIST]:   
        cmds.menuItem ( fld+"name", l=fld, tearOff=True, sm=True, p=p_menu)
        if os.listdir(os.path.join(path, fld)) :   
            an_checkContent ( os.path.join(path, fld) , fld+"name" )
            
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

scriptManager(PATH, SCRIPTS_FOLDER)



 



  



