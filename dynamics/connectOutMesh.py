import maya.cmds as cmds

def connectOutMesh():
    sel = cmds.ls(sl=True)
    cmds.connectAttr (sel[0] +'.outMesh', sel[1]+'.inMesh', f=True )