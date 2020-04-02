import maya.cmds as mc

def pvCreateSingleJoint():

    selectionList = mc.ls(selection=True)

    if selectionList:
        mainName = selectionList[0]
    else:
        mainName = raw_input()

    baseJointName = mainName + 'Base_jnt'
    bindJointName = mainName + '_bind'

    mc.joint(name=baseJointName)
    mc.joint(name=bindJointName)

    if selectionList:
        mc.parent(baseJointName, world=True)
        mc.select(selectionList, replace=True)
    else:
        mc.select(clear=True)

# pvCreateSingleJoint()