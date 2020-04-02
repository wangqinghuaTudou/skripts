import maya.cmds as cmds
import maya.OpenMaya as om

def pvSnapObject(*args):
    
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified two objects.')
        return
    if len(args) != 2:
        om.MGlobal.displayInfo('Must be specified only two objects.')
        return

    source, dest = args
    cmds.delete(cmds.parentConstraint(source, dest, maintainOffset=False))
    cmds.select(dest, replace=True)
    om.MGlobal.displayInfo('Object "%s" snaped to object "%s" successefuly.'%(dest, source))

#pvSnapObject()