import maya.cmds as mc
import maya.api.OpenMaya as om

def pvDuplicatePose(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    objects = args
    dupList = []

    for obj in objects:

        dup_name = 'dup_' + obj
        dup = mc.duplicate(obj, name= dup_name, returnRootsOnly=True)[0]

        for attr in attributes:
            try:
                mc.setAttr('%s.%s' % (dup, attr), lock=False)
            except:
                pass

        shapes = mc.listRelatives(dup, shapes=True, fullPath=True)
        if shapes:
            for shp in shapes:
                if mc.getAttr(shp + '.intermediateObject'):
                        mc.delete(shp)

        dupList.append(dup)

    if dupList:
        mc.select(dupList, replace=True)

    return dupList

# pvDuplicatePose()