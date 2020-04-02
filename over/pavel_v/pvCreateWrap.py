import maya.cmds as cmds
import maya.OpenMaya as om

def pvMakeWrap(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    wrap_driver = args.pop(0)
    for obj in args:
        hist = cmds.listHistory(obj, pruneDagObjects=True)
        cmds.select([obj, wrap_driver], replace=True)
        cmds.CreateWrap()
        if hist:
            for h in hist:
                if cmds.objExists(h + '.envelope'):
                    cmds.setAttr(h + '.envelope', 0)

pvMakeWrap()