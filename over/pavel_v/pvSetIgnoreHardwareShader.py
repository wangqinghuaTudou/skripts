import maya.cmds as cmds
import maya.OpenMaya as om

def pvSetIgnoreHardwareShader(*args):

    if not args:
        args = cmds.ls(selection=True)
        if args:
            args = cmds.listRelatives(args, shapes=True, fullPath=True)
    if not args:
        args = cmds.ls(type='mesh', allPaths=True)
    if not args:
        om.MGlobal.displayInfo('No one object specified and scene hasn\'t any "mesh".')
        return False

    for msh in args:
        if cmds.objExists(msh + '.ignoreHwShader') and not cmds.getAttr(msh + '.intermediateObject'):
            cmds.setAttr(msh + '.ignoreHwShader', 1)
    return True

# pvSetIgnoreHardwareShader()