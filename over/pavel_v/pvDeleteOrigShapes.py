import maya.cmds as mc
import maya.OpenMaya as om
from pvProcedures import *


def pvDeleteOrigShapes(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        args = pvGetAllMeshTransform()
    if not args:
        return

    deleted_shapes_counter = 0
    deletedShapes = []

    for obj in args:
        shapes = mc.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            for shp in shapes:
                isOrig = mc.getAttr (shp + '.intermediateObject')
                if isOrig:
                    isConnected = mc.listConnections(shp, source=True, destination=True)
                    if not isConnected:
                        try:
                            deletedShapes.append(shp)
                            mc.delete(shp)
                            deleted_shapes_counter += 1
                        except:
                            om.MGlobal.displayInfo('Can\'t delete "Orig" shape: ' + shp)

    if deletedShapes:
        om.MGlobal.displayInfo('-------------------------------------------------------------')
        om.MGlobal.displayInfo('Deleted %s shapes.'%deleted_shapes_counter)
        om.MGlobal.displayInfo('Deleted shapes:')
        om.MGlobal.displayInfo('%s'%deletedShapes)
    else:
        om.MGlobal.displayInfo('No "Orig" shapes deleted.')

    return deletedShapes

#pvDeleteOrigShapes()