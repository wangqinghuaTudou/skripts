import maya.cmds as mc
import maya.api.OpenMaya as om

def pvMirrorCurveShape(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    objects = args
    for obj in objects:
        shape = mc.listRelatives(obj, shapes=True)[0]
        degree = mc.getAttr(shape + '.degree')
        spans = mc.getAttr(shape + '.spans')
        vertexNumber = degree + spans
        halfVertexNumber = int(vertexNumber / 2)
        for i in xrange(halfVertexNumber):
            vertexTx = mc.getAttr (shape + '.controlPoints[%s].xValue'%i)
            vertexTy = mc.getAttr (shape + '.controlPoints[%s].yValue'%i)
            vertexTz = mc.getAttr (shape + '.controlPoints[%s].zValue'%i)
            j = vertexNumber - i - 1
            mc.setAttr (shape + '.controlPoints[%s].xValue'%j, -vertexTx)
            mc.setAttr (shape + '.controlPoints[%s].yValue'%j, vertexTy)
            mc.setAttr (shape + '.controlPoints[%s].zValue'%j, vertexTz)

#pvMirrorCurveShape()