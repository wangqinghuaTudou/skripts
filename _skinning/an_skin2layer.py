import maya.cmds as cmds
from an_classNames import AnNames as chn

# Skript for creation sekond layer and connect controls to geometry
# If move joint and it bind pre matrtix group it dos not influens on skin geometry
# It mast be group and parent under rivet locator

skinGeo= cmds.ls (sl=True)[0]

skinClusterName = cmds.ls (cmds.listHistory (skinGeo), type='skinCluster' )[0]
jointsName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt  

for i in range(len(jointsName)): 

    if not cmds.objExists(chn(jointsName[i]).sfxMinus()+'_bpm '):
        bmpGrp = cmds.group( n=chn(jointsName[i]).sfxMinus()+'_bpm ' , em=True)  # bind pre matrtix
    else: bmpGrp =  chn(jointsName[i]).sfxMinus()+'_bpm '
    cmds.delete( cmds.parentConstraint(jointsName[i], bmpGrp))
    cmds.connectAttr ( bmpGrp+ '.worldInverseMatrix[0]',  skinClusterName+'.bindPreMatrix['+str(i)+']')