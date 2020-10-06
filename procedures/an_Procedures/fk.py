import maya.cmds as cmds
from anProcedures import *
from CharacterNames import CharacterNames as chn
from an_classControllers import AnControllers as ctrl



'''
        fk()

an_fkControllerss()          -   put controlers to plase and connect jnt to parent
an_fkToJntDevider()          - 

 

'''


def an_fkController( name, jnt, p=None, pType='constraint'): 
    obj = ctrl(name)
    obj.makeController ( shapeType= "fk", size=1, offset =[0, 0, 0], orient="X", pos=jnt, posType='parent')
    if p and pType=='constraint':   
        cmds.parentConstraint(p, obj.oriGrp, mo = True)

def an_fkToJntDevider(ct, jnts):
    mpdv = cmds.createNode ('multiplyDivide',  n = chn(ct).sfxMinus()+'_mpdv') 
    cmds.setAttr (mpdv+".operation", 2) 
    cmds.addAttr (ct, longName='mult', dv=1,  keyable=True) 
    for d in  ['x', 'y', 'z']:
        cmds.connectAttr (ct+'.mult',   mpdv+".input2"+d.upper()) 
        cmds.connectAttr (ct+'.r'+d  , mpdv+'.input1'+d.upper())
        for jnt in jnts:
            cmds.connectAttr(mpdv+'.output'+d.upper(), jnt+'.rotate'+d.upper())

