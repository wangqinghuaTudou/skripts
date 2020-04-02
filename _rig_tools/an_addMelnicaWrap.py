import maya.cmds as cmds
def an_addMelnicaWrap():

    sel = cmds.ls(sl=True)
    cage = sel.pop(-1)
    cageShape = cmds.listRelatives( cage, s=True )[0]
    for obj in sel:
        cmds.select(obj)
        deform = cmds. deformer (type='melnitsaWrap')[0]
        cmds. connectAttr (cageShape+'.worldMesh[0]', deform+'.obstacleMesh')