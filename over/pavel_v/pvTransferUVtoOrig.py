import maya.cmds as mc
import maya.OpenMaya as om
from pvDuplicateDefault import *


def pvTransferUVtoOrigMain(source, dest):

    sourceShapes = mc.listRelatives(source, shapes=True)
    sourceShp = sourceShapes[0]

    if mc.getAttr(sourceShp + '.opposite'):
        mc.setAttr(sourceShp + '.opposite', 0)
        mc.polyNormal(sourceShp, normalMode=0, userNormalMode=1, constructionHistory=True)
        mc.bakePartialHistory(sourceShp, prePostDeformers=True)

    destShapes = mc.listRelatives(dest, shapes=True)
    destShp = destShapes[0]

    if mc.getAttr(destShp + '.opposite'):
        mc.setAttr(destShp + '.opposite', 0)
        mc.polyNormal(destShp, normalMode=0, userNormalMode=1, constructionHistory=True)
        mc.bakePartialHistory(destShp, prePostDeformers=True)

    dup = pvDuplicateDefault(dest)[0]
    mc.polyMapDel(dup, constructionHistory=False)

    mc.transferAttributes(source, dup, transferPositions=0, transferNormals=0, transferUVs=2, transferColors=0, sampleSpace=5, sourceUvSpace='map1', targetUvSpace='map1', searchMethod=3, flipUVs=0, colorBorders=1)

    mc.delete(constructionHistory=True)
    dupShp = mc.listRelatives(dup, shapes=True)[-1]
    
    for ds in destShapes:
        if mc.getAttr(ds + '.intermediateObject'):
            origShape = ds
    mc.parent(dupShp, dest, relative=True, shape=True)
    origConn = mc.listConnections(origShape + '.worldMesh[0]', source=False, destination=True, plugs=True)[0]
    mc.disconnectAttr(origShape + '.worldMesh[0]', origConn)
    mc.connectAttr(dupShp + '.worldMesh[0]', origConn, force=True)
    mc.setAttr(dupShp + '.intermediateObject', 1)

    mc.delete(origShape)
    mc.delete(dup)

def pvTransferUVtoOrig(*args):

    prefix = 'imp_'

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    '''
    if len(args) == 2:
        source = args[0]
        dest = args[1]
        pvTransferUVtoOrigMain(source, dest)
    else:
    '''
    for dest in args:
        source = prefix + dest
        isUnique = mc.ls(source)
        if '|' in dest:
            destName = dest.split('|')[-1]
            om.MGlobal.displayWarning('Object "%s" has non unique name.'%destName)
            return
        elif len(isUnique) > 1:
            om.MGlobal.displayWarning('Object "%s" has non unique name.'%source)
            return
        else:
            pvTransferUVtoOrigMain(source, dest)


pvTransferUVtoOrig()