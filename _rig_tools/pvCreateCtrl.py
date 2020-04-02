import maya.cmds as mc

def pvCreateCtrl():
    objList = mc.ls(selection=True)
    for obj in objList:
        if ('_bind' in obj):
            oriNull = obj.replace('_bind','_ori')
            conNull = obj.replace('_bind', '_con')
            mainName = obj[:-5]
        elif ('_jnt' in obj):
            oriNull = obj.replace('_jnt', '_ori')
            conNull = obj.replace('_jnt', '_con')
            mainName = obj[:-4]
        else:
            oriNull = obj + '_ori'
            conNull = obj + '_con'
            mainName = obj

        mc.group(empty=True, name=oriNull, world=True)
        mc.group(empty=True, name=conNull, world=True)

        ctrl = mainName + '_CT'
        mc.circle(center=[0, 0, 0], \
                  normal=[0, 1, 0], \
                  sweep=360, \
                  radius=1, \
                  degree=3, \
                  useTolerance=0, \
                  tolerance=0.01, \
                  sections=8, \
                  constructionHistory=0, \
                  name=ctrl)

        rotOrd = mc.getAttr(obj + '.rotateOrder')
        mc.setAttr(oriNull + '.rotateOrder', rotOrd)
        mc.setAttr(conNull + '.rotateOrder', rotOrd)
        mc.setAttr(ctrl + '.rotateOrder', rotOrd)

        mc.delete(mc.parentConstraint (obj, oriNull, maintainOffset=False))
        mc.delete(mc.parentConstraint (obj, conNull, maintainOffset=False))
        mc.delete(mc.parentConstraint (obj, ctrl, maintainOffset=False))
        mc.parent(ctrl, conNull)
        mc.parent(conNull, oriNull)

        mc.parentConstraint (ctrl, obj, maintainOffset=True)
        mc.select(clear=True)

#pvCreateCtrl()