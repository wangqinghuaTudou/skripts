
import maya.cmds as cmds


def breathJntAdd(parentObj='spine03_bind'):
    cmds.select (cl=True)
    bJnt = cmds.joint (n='breath_jnt')
    
    if not cmds.objExists ('torso_CT.breath'): 
        cmds.addAttr ('torso_CT', longName='breath', keyable=True) #add list of attributes
        
    cmds.parent(bJnt, parentObj)
    cmds.setAttr (bJnt+".t", 0.1, 0, 0)
    MDVnod = cmds.shadingNode ('multiplyDivide', n='breathMDV',  asUtility=True)
    cmds.setAttr (MDVnod+".input2X", 20)
    cmds.connectAttr ('torso_CT.breath', MDVnod+".input1X")
    PMAnod = cmds.shadingNode ('plusMinusAverage', n='breathPMA',  asUtility=True)
    cmds.connectAttr ( MDVnod+".outputX", PMAnod+'.input1D[0]')
    cmds.setAttr (PMAnod+".input1D[1]", 1)
    
    for dir in ['x', 'y', 'z']: cmds.connectAttr ( PMAnod+".output1D", bJnt+'.s'+dir)

