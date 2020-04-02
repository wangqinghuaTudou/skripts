import maya.cmds as cmds
import maya.OpenMaya as om


def pvSetCharToDefault():

    set_attr_list = ['cmds.setAttr("switch_CT.r_armIkFkSwitch", 0)', \
    'cmds.setAttr("switch_CT.l_armIkFkSwitch", 0)', \
    'cmds.setAttr("switch_CT.r_legIkFkSwitch", 1)', \
    'cmds.setAttr("switch_CT.l_legIkFkSwitch", 1)', \
    'cmds.setAttr("switch_CT.addCtrls", 1)', \
    'cmds.setAttr("switch_CT.l_armCtrls", 1)', \
    'cmds.setAttr("switch_CT.r_armCtrls", 1)', \
    'cmds.setAttr("switch_CT.l_legCtrls", 1)', \
    'cmds.setAttr("switch_CT.r_legCtrls", 1)', \
    'cmds.setAttr("switch_CT.bodyCtrls", 1)', \
    'cmds.setAttr("switch_CT.faceTable", 0)', \
    'cmds.setAttr("switch_CT.upCloth", 1)', \
    'cmds.setAttr("switch_CT.proxyHead", 0)', \
    'cmds.setAttr("switch_CT.proxyBody", 0)', \
    'cmds.setAttr("switch_CT.fingersCtrls", 1)', \
    'cmds.setAttr("switch_CT.selfCollision", 0)', \
    'cmds.setAttr("switch_CT.volumeCollision", 0)', \
    'cmds.setAttr("switch_CT.crown", 1)', \
    'cmds.setAttr("switch_CT.hairsVis", 1)', \
    'cmds.setAttr("switch_CT.skirtCtrls", 0)', \
    'cmds.setAttr("switch_CT.renderGeometry", 0)', \
    'cmds.setAttr("switch_CT.jntVis", 0)', \
    'cmds.setAttr("switch_CT.scaleOffset", 0)', \
    'cmds.setAttr("switch_CT.jntVis", 0)', \
    'cmds.setAttr("geo_layer.enabled", 1)', \
    'cmds.setAttr("geo_layer.displayType", 2)', \
    'cmds.setAttr("geo_layer.visibility", 1)', \
    'cmds.setAttr("head_CT.rSpace", 0)', \
    'cmds.setAttr("head_CT.tSpace", 3)', \
    'cmds.setAttr("eyesAim_CT.space", 2)', \
    'cmds.setAttr("r_shoulder_CT.stretching", 0)', \
    'cmds.setAttr("r_shoulder_CT.autoShoulder", 0)', \
    'cmds.setAttr("l_shoulder_CT.autoShoulder", 0)', \
    'cmds.setAttr("l_shoulder_CT.stretching", 0)', \
    'cmds.setAttr("l_foreArmBend_CT.squashSwitch", 0)', \
    'cmds.setAttr("l_upArmBend_CT.squashSwitch", 0)', \
    'cmds.setAttr("r_foreArmBend_CT.squashSwitch", 0)', \
    'cmds.setAttr("r_upArmBend_CT.squashSwitch", 0)', \
    'cmds.setAttr("r_upArm_CT.rSpace", 3)', \
    'cmds.setAttr("l_upArm_CT.rSpace", 3)', \
    'cmds.setAttr("r_kneeIk_CT.space", 3)', \
    'cmds.setAttr("l_kneeIk_CT.space", 3)']

    for sal in set_attr_list:
        try:
            exec(sal)
        except Exception, err:
            om.MGlobal.displayWarning(err)

    bind_poses_list = cmds.ls(type='dagPose')
    if bind_poses_list:
        bind_poses_number = len(bind_poses_list)
        om.MGlobal.displayInfo(bind_poses_number)
        cmds.delete(bind_poses_list)
    else:
        om.MGlobal.displayInfo('Scene hasn\'t any "bind pose" node.')

    graph_editor_list = cmds.ls(type='nodeGraphEditorInfo')
    if graph_editor_list:
        graph_editor_number = len(graph_editor_list)
        om.MGlobal.displayInfo(graph_editor_number)
        cmds.delete(graph_editor_list)
    else:
        om.MGlobal.displayInfo('Scene hasn\'t any "node graph editor" node.')

