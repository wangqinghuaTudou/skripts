from maya import cmds

def pvCreateCtrl():
    objList = cmds.ls(selection=True)
    for o in objList:
        obj = o.split('|')[-1]
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

        oriNull = cmds.group(empty=True, name=oriNull, world=True)
        conNull = cmds.group(empty=True, name=conNull, world=True)

        ctrl = mainName + '_CT'
        ctrl = cmds.circle(center=[0, 0, 0], \
                         normal=[0, 1, 0], \
                         sweep=360, \
                         radius=1, \
                         degree=3, \
                         useTolerance=0, \
                         tolerance=0.01, \
                         sections=8, \
                         constructionHistory=0, \
                         name=ctrl)
        shps = cmds.listRelatives(ctrl, shapes=True)
        for s in shps:
            try:
                cmds.setAttr(s + '.overrideEnabled', 1)
                cmds.setAttr(s + '.overrideRGBColors', 0)
                cmds.setAttr(s + '.overrideColor', 17)
            except:
                pass

        cmds.delete(cmds.parentConstraint (obj, oriNull, maintainOffset=False))
        cmds.delete(cmds.parentConstraint (obj, conNull, maintainOffset=False))
        cmds.delete(cmds.parentConstraint (obj, ctrl, maintainOffset=False))
        cmds.parent(ctrl, conNull)
        cmds.parent(conNull, oriNull)

        cmds.parentConstraint (ctrl, obj, maintainOffset=True)
        cmds.select(clear=True)

#pvCreateCtrl()