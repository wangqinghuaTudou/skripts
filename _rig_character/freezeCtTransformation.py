import maya.cmds as cmds


def freezeCtTransformation():
    sels = cmds.ls(sl=True)
    for sel in sels:
        copy = cmds.duplicate(sel, n = sel.replace('_CT', '_offs'))[0]
        cmds.delete( cmds.listRelatives (copy, c=True, path=1))
        cmds.parent(sel, copy)
