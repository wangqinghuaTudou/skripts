
# -*- coding: utf-8 -*-

import maya.mel as mm
import maya.cmds as cmds
"""
        dynamics
        
    -setObjToTPos() 
    -setCharToTPos()
    
"""
#geo = cmds.ls(sl=True)
#dfgdg=setObjToTPos(geo)


def setObjToTPos(geo):
    TYPE=['wrap', 'melnitsaWrap', 'blendShape', 'skinCluster'] 
    cmds.select(geo)
    mm.eval('displayNClothMesh "input";') 
    nodes = [x for x in cmds.listHistory(geo) if cmds.nodeType(x) in TYPE]
    for nod in nodes:
        cmds.setAttr (nod+".envelope", 0)
    t_geo = cmds.duplicate(geo)[0]
    bl_shape = cmds.blendShape(t_geo, geo, o="world" )
    #
    for nod in nodes:
        cmds.setAttr (nod+".envelope", 1)
    cmds.setAttr (t_geo+".v", 0)
    cmds.select(geo)
    mm.eval('displayNClothMesh "current";')
    return bl_shape[0]+'.'+t_geo, t_geo

def setCharToTPos(geometrys = '', keys =[-20, -10]):
 
    if not geometrys: geometrys = cmds.ls(sl=True)
    selLen = len(cmds.referenceQuery(geometrys[0],filename=True ).split('.m')[0])+3
    ref = cmds.referenceQuery(geometrys[0],filename=True )[:selLen]  
    name= os.path.basename(ref).split(".")[0]
    
    general = geometrys[0].split(':')[0]+':pivotOffset_CT'
    t_grp = cmds.group(n=name+"_tPos", em=1)
    cmds.addAttr(t_grp, ln='t_val', k=True, max=1, min=0)
    for geo in geometrys:
        bl_shape, t_geo = setObjToTPos(geo)
        cmds.connectAttr(t_grp+'.t_val', bl_shape  )
        cmds.parent(t_geo, t_grp)
         
    cmds.delete(cmds.parentConstraint(general, t_grp))
    cmds.setKeyframe( t_grp+'.t_val', v=1, t=keys[0])
    cmds.setKeyframe( t_grp+'.t_val', v=0, t=keys[1])



def getDynamicsData():
    referenceList =  [x for x in  cmds.ls(rf = True) if not cmds.file(rfn=x, q=True, deferReference=True )]
    file -unloadReference "BabushkaMiddleRN" "D:/work/Project/MALYSH/assets/chars/babushka/maya/babushka_dyn.mb";
    cmds.file(  query=True, referenceNode=True )
    cmds.file("BabushkaMiddleRN",   loadReference=True)