
import sys, os
from anProcedures import *
import maya.cmds as cmds


def dynamics_tools ():
    leyouts = an_turnBasedUi('dtls', title ='dynamics_tools',  stepsLabel =['playback_options', 'dynamic version', 'export alembic'])
    playback_options(leyouts[0])
    dynamic_version (leyouts[1])
    export_alembicUI(leyouts[2])


def playback_options(par):
    st_dyn_val = -21
    def_mid_val = 1 #cmds.playbackOptions(q=True,  min=True)
    def_max_val = cmds.playbackOptions(q=True,  max=True)
    end_dyn_val = 1
    
    cmds.rowColumnLayout('Layout', nc =4,  p=par)
    cmds.text('  Input offset', al='left',  width= 105)
    cmds.text('  Start', al='left',  width= 105)
    cmds.text('  End', al='left',  width= 105)
    cmds.text('  Add MB frames', al='left',  width= 105)
    cmds.textField('stField', tx= st_dyn_val, w=105 )
    cmds.textField('midField', tx=def_mid_val, w=105)
    cmds.textField('endField', tx=def_max_val, w=105)
    cmds.textField('mbField', tx="+"+str(end_dyn_val), w=105)
    
    cmds.rowColumnLayout('Layout2', nc=3, p=par, columnSpacing = [(2,2),(3,2)])
    cmds.button(l='Set previos', c= 'comand("previos")', w=103)
    cmds.button(l='Set render', c='comand("render")', w=208)
    cmds.button(l='Set dynamics', c='comand("dynamics")', w=103)
    

def comand(typeF):
    st_dyn_val = cmds.textField('stField', q=1, tx=1)
    midF = cmds.textField('midField', q=1, tx=1)
    endF = cmds.textField('endField', q=1, tx=1)
    mbF = cmds.textField('mbField', q=1, tx=1)
    mbF = mbF[1:] if mbF[0]== "+" else mbF

    if typeF == 'render':
        mn, mx = midF, endF
    elif typeF == 'previos':
        mn = float(midF)+float(st_dyn_val)
        mx = midF
    else:
        mn = float(midF)+float(st_dyn_val)
        mx = float(endF)+float(mbF)
    cmds.playbackOptions(min=mn)
    cmds.playbackOptions(max=mx)
 
def dynamic_version(par):
    cmds.columnLayout(  p=par,)
    w=420
    cmds.button(l='Referens to DynVersion', c='refToDynVersion()', w=w )
    cmds.button(l='Select all nucleus', c='selNucleus()', w=w)
    cmds.button(l='Set start frame', c='setStartFrame()', w=w)


def export_alembicUI(par):
    cmds.columnLayout('pathCL',    p=par)
    cmds.textField('pathField',  w=420, tx=getAlembikPath())
    cmds.rowColumnLayout('pathRCL', nc =3,  p=par, columnSpacing = [(2,2),(3,2)])
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


if __name__ == '__main__':
    dynamics_tools ()












