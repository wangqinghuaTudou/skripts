import maya.cmds as cmds 
from  anProcedures import *
from CharacterNames import CharacterNames as chn



def an_halfBendJnts():
    sel = cmds.ls(sl=True)
    
    for bendJnt in sel:
        
        
        parentJnt = cmds.listRelatives (bendJnt, p=True)[0]
        
        cmds.select (cl =True)
        
        parts=chn(bendJnt).divideName()
        
        halfJnt = cmds.joint (n = parts[0]+parts[1]+"HalfJntRig_jnt") 
        halfJntBnd = cmds.joint (n = parts[0]+parts[1]+"HalfJntRig_bnd", p=[0,-0.1,0]) 
        halfJntGrp = cmds.group ( n = parts[0]+parts[1]+"HalfJntRig_grp", em=True) 
        cmds.parent (halfJnt, halfJntGrp)
        
        cmds.delete (cmds.parentConstraint ( bendJnt, halfJntGrp ))
        cmds.parentConstraint ( parentJnt, halfJntGrp, mo=True)
        cmds.pointConstraint ( bendJnt, halfJnt )
        
        MDVOfset = cmds.createNode ('multiplyDivide', n=parts[0]+parts[1]+"HalfJnt_mdv") 
        cmds.setAttr (MDVOfset+".operation", 2) 
        cmds.setAttr (MDVOfset+".input2X", 2)
        cmds.connectAttr ( bendJnt+'.rz', MDVOfset+".input1X")
            
        cmds.connectAttr (  MDVOfset+".outputX", halfJnt+'.rz',)