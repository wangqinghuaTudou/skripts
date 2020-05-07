#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, cPickle
import maya.mel as mm
import maya.cmds as cmds
"""

1 Понятие т поза:
      путь персонажа : {'name': имя персонажа,
                        'ct' - контроллер,
                        'tObjects' : {geo1:psList1, geo2:psList2,} } 
                
2 Сохранение т позы

3 Микс т позы.

"""

T_FILE = 'D:/work/Project/tChar.dat'
T_CT = 'body_CT'
SFX='tmanager'

def getPointPos(geo):
    pPos =[]
    for i in xrange(cmds.polyEvaluate(geo, v=True )):
        pPos.append(cmds.xform (geo+'.vtx['+str(i)+']',q=1, t=1, ws=1))     
    return pPos

def addTPos(t_ct=''):  #сохраняет обьекты стоящий в т позе в набор 
    geometrys = cmds.ls(sl=True)
    selLen = len(cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True ).split('.m')[0])+3
    ref = cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True )[:selLen]  
    name= os.path.basename(ref).split(".")[0]
    if not t_ct:  t_ct=T_CT
    pObj ={}
    for geo in geometrys:
        pObj[geo.split(':')[-1]]= getPointPos(geo)
    return ref, {'name':name, 'ct':t_ct, 'tObjects':pObj }
    
def newFile():
    global FILE, GLOB_DIC
    FILE = cmds.fileDialog2(fileFilter='*.dat', fileMode=0, caption="Save position" )[0]
    GLOB_DIC = {}
    f = open(T_FILE, 'w')
    cPickle.dump(TPOS_DIC , f )
    f.close()
    cmds.textFieldButtonGrp(SFX+"pathF", e=True, text=FILE)



import maya.mel as mm

def setTPos(keys =[-20, -10]):
    geometrys = cmds.ls(sl=True)
    selLen = len(cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True ).split('.m')[0])+3
    ref = cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True )[:selLen]  
    name= os.path.basename(ref).split(".")[0]
    
    general = geometrys[0].split(':')[0]+':pivotOffset_CT'
    t_grp = cmds.group(n=name+"_tPos", em=1)
    cmds.addAttr(t_grp, ln='t_val', k=True, max=1, min=0)
    
    for geo in geometrys:
        cmds.select(geo)
        mm.eval('displayNClothMesh "input";') 
        typ=['wrap', 'melnitsaWrap', 'blendShape', 'skinCluster'] 
        nodes = [x for x in cmds.listHistory(geo) if cmds.nodeType(x) in typ]
        for nod in nodes:
            cmds.setAttr (nod+".envelope", 0)
        t_geo = cmds.duplicate(geo)[0]
        bl_shape = cmds.blendShape(t_geo, geo, o="world" )
        cmds.connectAttr(t_grp+'.t_val', bl_shape[0]+'.'+t_geo )
        cmds.parent(t_geo, t_grp)
        for nod in nodes:
            cmds.setAttr (nod+".envelope", 1)
        cmds.setAttr (t_geo+".v", 0)
        cmds.select(geo)
        mm.eval('displayNClothMesh "current";') 
    
    cmds.delete(cmds.parentConstraint(general, t_grp))

    cmds.setKeyframe( t_grp+'.t_val', v=1, t=keys[0])
    cmds.setKeyframe( t_grp+'.t_val', v=0, t=keys[1])



 