
import sys, os
vDirPath = '//dataServer/Project/backup_s3d/lib/setup/maya/maya_scripts_rfm3/rigging_tools/procedures/'
if not  vDirPath in  list(sys.path): sys.path.insert(0, vDirPath)


import maya.cmds as cmds
from anProcedures import *

import maya.cmds as cmds
import os

def dynamics_tools ():
    leyouts = an_turnBasedUi('dtls', title ='dynamics_tools',  stepsLabel =['playback_options', 'dynamic version', 'export alembic'])
    playback_options(leyouts[0])

    dynamic_version (leyouts[1])
    
    export_alembicUI(leyouts[2])


#dynamics_tools ()  


def playback_options(par):
    def_st_val = cmds.playbackOptions(q=True,  min=True)-30
    def_mid_val = cmds.playbackOptions(q=True,  min=True)
    def_max_val = cmds.playbackOptions(q=True,  max=True)
    cmds.rowColumnLayout('Layout', nc =4,  p=par)
    cmds.text('', al='left',  width= 140)
    cmds.textField('stField', tx= def_st_val )
    cmds.textField('midField', tx=def_mid_val )
    cmds.textField('endField', tx=def_max_val)
    cmds.rowColumnLayout('Layout2', nc=3, p=par)
    cmds.button(l='Set previos', c= 'comand("ttt")', w=140)
    cmds.button(l='Set all', c='comand("all")', w=140)
    cmds.button(l='Set render', c='comand("render")', w=140)

def dynamic_version(par):
    cmds.columnLayout(  p=par,)
    w=420
    cmds.button(l='Referens to DynVersion', c='refToDynVersion()', w=w )
    cmds.button(l='Select all nucleus', c='selNucleus()', w=w)
    cmds.button(l='Set start frame', c='setStartFrame()', w=w)


def export_alembicUI(par):
    cmds.columnLayout('pathCL',    p=par)
    cmds.textField('pathField',  w=420, tx=getAlembikPath())
    cmds.rowColumnLayout('pathRCL', nc =3,  p=par)
    cmds.button(l='Referens out path', c="cmds.textField('pathField',  e=True, tx=getAlembikPath())", w=140  )
    cmds.button(l='Open out folder', c='openFolder()', w=140  )
    cmds.button(l='Export alembic', c='exportAlembik()', w=140)
    


def refToDynVersion():
    refNodes = cmds.referenceQuery( cmds.ls(sl=True)[0], rfn=True )  
    refPath = cmds.referenceQuery(refNodes, f=True)
    
    if '_middle.' in refPath: 
        refPath = refPath.replace('_middle.', '.')
        
    dynPath = refPath.split('/')
    dynPath.insert(-1, 'work')
    dynPath.insert(-1, 'dyn')
    
    dynPath[-1] = dynPath[-1].replace('.mb', '_dyn.mb')
    dynPath = '/'.join(dynPath)
    
    if not os.path.isfile(dynPath):
        dynPath = dynPath[:-3] + '.ma'
    
    if os.path.isfile(dynPath):
        cmds.file(dynPath, loadReference=refNodes)


def comand(typeF):
    startF = cmds.textField('stField', q=1, tx=1)
    midF = cmds.textField('midField', q=1, tx=1)
    endF = cmds.textField('endField', q=1, tx=1)
    if typeF == 'render':
        mn, mx = midF, endF
    elif typeF == 'all':
        mn, mx = startF, endF
    else:
        mn, mx = startF, midF
    cmds.playbackOptions(min=mn)
    cmds.playbackOptions(max=mx)




      

def selNucleus():
    cmds.select([ x for x in   cmds.ls ()   if  cmds.nodeType(x) == 'nucleus' ])

def setStartFrame():
    solvers = [ x for x in   cmds.ls ()   if  cmds.nodeType(x) == 'nucleus' ]
    fr = cmds.playbackOptions(q=True,  min=True)
    for each in solvers:
        cmds.setAttr( each+".startFrame", fr)

def exportAlembik():
    path_name = cmds.file(q=True, sn=True)
    filename = os.path.basename(path_name)
    path = os.path.dirname(path_name)
    raw_name, extension = os.path.splitext(filename)
    targ_path = path.split('dyn/work')[0]+"cache/alembic/dyn/"
    if not os.path.exists(targ_path): 
        os.makedirs(targ_path) 
    min_f, max_f = int(cmds.playbackOptions(q=True,  min=True)), int(cmds.playbackOptions(q=True,  max=True))+1
    try: folder = cmds.ls(sl=True)[0]
    except: cmds.error( 'Select "geo_normal" folder!' )
    cmds.AbcExport ( j = "-frameRange  " + str(min_f) + " "+ str(max_f) +"  -attr material -dataFormat ogawa -root "+ folder +" -file "+targ_path+ raw_name+".abc" )


def getAlembikPath():
    
    path_name = cmds.file(q=True, sn=True)
    filename = os.path.basename(path_name)
    path = os.path.dirname(path_name)
    raw_name, extension = os.path.splitext(filename)
    return path.split('dyn/work')[0]+"cache/alembic/dyn/"
    
  
   

def openFolder():
    import subprocess
    if os.path.exists(getAlembikPath()): 
        os.system(r'Explorer "%s"' % os.path.abspath(getAlembikPath())  )
    else:
        os.system( r'Explorer "%s"' % os.path.abspath( getAlembikPath()[:-5]  ))


#dynamics_tools ()  
 















