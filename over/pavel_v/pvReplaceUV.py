import maya.cmds as cmds
import maya.api.OpenMaya as om
from pvShowOrigGeo import *

def pvReplaceUV(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified two objects.')
        return
    if len(args) != 2:
        om.MGlobal.displayInfo('Must be specified only two objects.')
        return

    source = args[0]
    dest = args[1]
    pvShowOrigGeo(dest)

    cmds.transferAttributes(source, dest, \
                            transferPositions=0, \
                            transferNormals=0, \
                            transferUVs=2, \
                            transferColors=0, \
                            sampleSpace=4, \
                            sourceUvSpace='map1', \
                            targetUvSpace='map1', \
                            searchMethod=3, \
                            flipUVs=0,
                            colorBorders=1)

    cmds.delete(dest, constructionHistory=True)
    pvHideOrigGeo(dest)
    cmds.select(dest, replace=True)
    om.MGlobal.displayInfo('Mapping replaced successfuly.')

# pvReplaceUV()