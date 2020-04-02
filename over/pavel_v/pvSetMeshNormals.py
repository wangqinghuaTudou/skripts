from maya import cmds
import maya.OpenMaya as om

def pvSetMeshNormals(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        args = cmds.ls(type='mesh')
    if not args:
        om.MGlobal.displayInfo('Info: Scene hasn\'t any mesh.')
        return False

    for mesh in args:
        cmds.polyNormalPerVertex(mesh, unFreezeNormal=True)
        cmds.polyNormalPerVertex(mesh, normalXYZ=[1,0,0])
        cmds.polySetToFaceNormal(mesh)
        cmds.polySoftEdge(mesh, angle=80, constructionHistory=False)

    om.MGlobal.displayInfo('Meshe\'s normals successfuly unlocked and setuped.')

    return True

if __name__ == "__main__":
    pvSetMeshNormals()