

import maya.cmds as cmds

def an_removeInf():
    geo, jnt = cmds.ls(sl=True)[0], cmds.ls(sl=True)[1]
    skinClusterName =  cmds.ls (cmds.listHistory (geo, pdo=1), type='skinCluster')[0]
    cmds.setAttr (skinClusterName+".normalizeWeights", 0)
    cmds.skinCluster(skinClusterName, edit=True, ri=jnt)
    cmds.setAttr (skinClusterName+".normalizeWeights", 1)
    cmds.skinPercent (skinClusterName,   normalize=True )