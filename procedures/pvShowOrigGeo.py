import maya.cmds as cmds
import maya.OpenMaya as om

def pvShowOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 1)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 0)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) shown successful.')

def pvHideOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 0)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 1)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) hided successful.')