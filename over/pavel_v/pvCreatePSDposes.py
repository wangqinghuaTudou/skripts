import maya.cmds as mc
import maya.OpenMaya as om


def pvCreatePSDposes():

    rotateAttributes = ['rx', 'ry', 'rz']
    controllersDictionary = {'spine_bind':['spineFront_geo', 'spineBack_geo', 'spineBendLeft_geo', 'spineBendRight_geo', 'spineTwistLeft', 'spineTwistRight'], \
                             'clavicles_bind':['claviclesFront_geo', 'claviclesBack_geo', 'claviclesUp_geo', 'claviclesDown_geo'], \
                             'uparms_bind':['uparmsFront_geo', 'uparmsBack_geo', 'uparmsUp_geo', 'uparmsDown_geo']}

    currentKeyframe = 0
    keyframeInterval = 10
    for ctrlsDict in controllersDictionary:
        om.MGlobal.displayInfo('--------------')
        om.MGlobal.displayInfo(ctrlsDict)
        om.MGlobal.displayInfo('--------------')
        leftSide = 'l_' + ctrlsDict
        rightSide = 'r_' + ctrlsDict
        spineJointsList = []
        necessaryValue = 90
        spineJointsNumber = 6
        value = necessaryValue / (spineJointsNumber - 2)
        for rtAttr in rotateAttributes:
            if 'spine' in ctrlsDict:
                for i in xrange(spineJointsNumber - 2):
                    spineJointsName = ctrlsDict.replace('spine', 'spine0%s'%(i + 2))
                    spineJointsList.append(spineJointsName + '.%s'%rtAttr)
                mc.setKeyframe(spineJointsList, value=0, time=currentKeyframe)
                currentKeyframe += keyframeInterval
                mc.setKeyframe(spineJointsList, value=value, time=currentKeyframe)
        geometryNames = controllersDictionary.get(ctrlsDict)
        for geoName in geometryNames:
            om.MGlobal.displayInfo(geoName)

pvCreatePSDposes()