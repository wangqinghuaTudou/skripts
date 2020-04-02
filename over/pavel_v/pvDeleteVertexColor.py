import maya.cmds as cmds
import maya.api.OpenMaya as om
from pvShowOrigGeo import *
from pvDeleteOrigShapes import *

def pvDeleteVertexColor(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified some object(s).')
        return

    for obj in args:
        pvDeleteOrigShapes(obj)
        pvShowOrigGeo(obj)
        obj_shapes = cmds.listRelatives(obj, shapes=True)
        if obj_shapes:
            obj_shape = obj_shapes[0]
        color_set = cmds.polyColorSet(obj_shape, query=True, currentColorSet=True)
        if color_set:
            cmds.polyColorSet(obj_shape, delete=True, colorSet=color_set[0])
        cmds.delete(obj, constructionHistory=True)
        pvHideOrigGeo(obj)

    om.MGlobal.displayInfo('Vertex color deleted successfully.')

# pvDeleteVertexColor()