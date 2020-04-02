import maya.cmds as mc
import maya.OpenMaya as om
import re


def pvUnpluggedAnimCurves():

    unpluggedAnimCurves = []
    animCurvesList = mc.ls(type='animCurve')
    if animCurvesList:
        for animCurve in animCurvesList:
            if not mc.listConnections(animCurve, source=False, destination=True):
                unpluggedAnimCurves.append(animCurve)

    return unpluggedAnimCurves

def pvReconnectReferenceAnimCurve(anim, ref, objType):

    rexLong = re.compile(r'^(([a-zA-Z0-9_]*:)*[a-zA-Z]{1}[a-zA-Z0-9_]*' + objType + r')_([a-zA-Z0-9_]*)$')
    rexShort = re.compile(r'^([a-zA-Z]{1}[a-zA-Z0-9_]*' + objType + r')_([a-zA-Z0-9_]*)$')

    lookLikeLong = rexLong.match(anim)
    lookLikeShort = rexShort.match(anim)

    if lookLikeLong:
        ctrl = lookLikeLong.groups()[0]
        attr = lookLikeLong.groups()[2]
    elif lookLikeShort:
        ctrl = lookLikeShort.groups()[0]
        attr = lookLikeShort.groups()[1]
    else:
        ctrl = ''
        attr = ''

    if mc.objExists('%s.%s'%(ctrl, attr)):
        if not mc.listConnections('%s.%s' % (ctrl,attr), source=True, destination=False):
            if ref:
                plHolder = mc.listConnections('%s.output' % anim, source=False, destination=True, plugs=True)
                mc.disconnectAttr('%s.output' % anim, plHolder[0])
            mc.connectAttr('%s.output' % anim, '%s.%s' % (ctrl,attr), force=True)

def pvAnimRestore():

    objectsTypes = ['_CT', '_cam', '_place']
    refList = mc.ls(references=True)

    for ref in refList:
        animCurves = mc.listConnections(ref, type='animCurve', source=True, destination=False)
        if animCurves:
            om.MGlobal.displayInfo('Scene has reference animation curves.')
            om.MGlobal.displayInfo('Try to reconnect reference animation curves...')
            for anim in animCurves:
                for objType in objectsTypes:
                    pvReconnectReferenceAnimCurve(anim, True, objType)

    if mc.objExists('_UNKNOWN_REF_NODE_'):
        animCurves = mc.listConnections('_UNKNOWN_REF_NODE_', type='animCurve', source=True, destination=False)
        if animCurves:
            for anim in animCurves:
                for objType in objectsTypes:
                    pvReconnectReferenceAnimCurve(anim, True, objType)

    om.MGlobal.displayInfo('Reference animation curves reconnected successful.')

    unpluggedAnimCurves = pvUnpluggedAnimCurves()
    if unpluggedAnimCurves:
        om.MGlobal.displayInfo('Scene has unplugged animation curves.')
        om.MGlobal.displayInfo('Try to reconnect unplugged animation curves...')
        for unpAnim in unpluggedAnimCurves:
            for objType in objectsTypes:
                pvReconnectReferenceAnimCurve(unpAnim, False, objType)

    unpluggedAnimCurves = pvUnpluggedAnimCurves()
    if not unpluggedAnimCurves:
        om.MGlobal.displayInfo('All animation curves reconnected successful.')
    else:
        om.MGlobal.displayInfo('Scene has unidentified animation curves.')
        mc.select(unpluggedAnimCurves, replace=True)


