import maya.cmds as mc


def pvConvRotToJo(objList):
    for each in objList:
        rx = mc.getAttr('%s.rotateX'%each)
        ry = mc.getAttr('%s.rotateY'%each)
        rz = mc.getAttr('%s.rotateZ'%each)
        if rx!=0:
            jox = mc.getAttr('%s.jointOrientX'%each)
            mc.setAttr('%s.jointOrientX'%each, jox + rx)
            mc.setAttr('%s.rotateX'%each, 0)
        if ry!=0:
            joy = mc.getAttr('%s.jointOrientX'%each)
            mc.setAttr('%s.jointOrientY'%each, joy + ry)
            mc.setAttr('%s.rotateY'%each, 0)
        if rz!=0:
            joz = mc.getAttr('%s.jointOrientX'%each)
            mc.setAttr('%s.jointOrientZ'%each, joz + rz)
            mc.setAttr('%s.rotateZ'%each, 0)