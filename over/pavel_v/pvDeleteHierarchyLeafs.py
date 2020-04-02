import maya.cmds as cmds
import Maya.OpenMaya as om

def pvDeleteHierarchyLeafs(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return False

    for parent in args:
        om.MGlobal.displayInfo('Info: Parent - %s'%parent)
        while len(cmds.ls(parent, dagObjects=True, leaf=True)) > 1:
            leafs_list = cmds.ls(parent, dagObjects=True, leaf=True)
            om.MGlobal.displayInfo('Info: Leafs list - %s'%leafs_list)
            for l in leafs_list:
                if cmds.objExists(l) and l != parent:
                    try:
                        cmds.delete(l)
                    except Exception, err:
                        om.MGlobal.displayWarning('Info: %s'%err)