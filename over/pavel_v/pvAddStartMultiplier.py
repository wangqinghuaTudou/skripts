import maya.cmds as cmds
import maya.OpenMaya as om

def pvAddStartMultiplier():

    selection_list = cmds.ls(selection=True)
    if not selection_list:
        om.MGlobal.displayInfo('Must be specified some object(s).')
        return

    #driver_axis = 'tx'
    driver_axis = raw_input()
    if driver_axis != 'tx' and driver_axis != 'ty' and driver_axis != 'tz':
        om.MGlobal.displayInfo('Driver axis must be in format: tx or ty or tz.')
        return

    pose_reader = False

    for corr in selection_list:
        hist = cmds.listHistory(corr)
        pose_reader = cmds.ls(hist, type='poseReader')
        if not cmds.objExists(corr + '.startMultiplier'):
            cmds.addAttr(corr, longName='startMultiplier', attributeType='double', defaultValue=0)
            cmds.setAttr(corr + '.startMultiplier', edit=True, keyable=True)
        if not cmds.objExists(corr + '.endRotation'):
            cmds.addAttr(corr, longName='endRotation', attributeType='double', defaultValue=0)
            cmds.setAttr(corr + '.endRotation', edit=True, keyable=True)
            cmds.setAttr(corr + '.endRotation', 90)
        sr_name = corr.replace('_bind', 'BindTr_sr')
        set_range = cmds.createNode('setRange', name=sr_name)
        input_tr = cmds.listConnections(corr + '.%s'%driver_axis, source=True, destination=False, plugs=True)
        if not input_tr:
            om.MGlobal.displayInfo('Corrective joint "%s" has not input connection in "%s".'%(corr, driver_axis))
        else:
            input_tr = input_tr[0]
            cmds.disconnectAttr(input_tr, corr + '.%s'%driver_axis)
            cmds.connectAttr(sr_name + '.outValueX', corr + '.%s'%driver_axis, force=True)
            cmds.connectAttr(input_tr, set_range + '.valueX', force=True)
            mult_value = cmds.getAttr(corr + '.multiplier')
            if mult_value > 0:
                cmds.connectAttr(corr + '.startMultiplier', sr_name + '.oldMinX', force=True)
                cmds.connectAttr(corr + '.multiplier', sr_name + '.maxX', force=True)
                cmds.connectAttr(corr + '.multiplier', sr_name + '.oldMaxX', force=True)
            else:
                cmds.connectAttr(corr + '.startMultiplier', sr_name + '.oldMaxX', force=True)
                cmds.connectAttr(corr + '.multiplier', sr_name + '.minX', force=True)
                cmds.connectAttr(corr + '.multiplier', sr_name + '.oldMinX', force=True)
            if not pose_reader:
                input_mdv_attr = input_tr.replace('output', 'input1')
                input_mdv = cmds.listConnections(input_mdv_attr, source=True, destination=False, plugs=True)
                if not input_mdv:
                    om.MGlobal.displayInfo('mdv node "%s" has not input connection.'%input_mdv_attr)
                else:
                    input_mdv = input_mdv[0]
                    name_normalize = input_tr.split('.')[0] + 'RotYnorm_mdv'
                    name_normalize = cmds.createNode('multiplyDivide', name=name_normalize)
                    cmds.disconnectAttr(input_mdv, input_mdv_attr)
                    cmds.connectAttr(name_normalize + '.outputX', input_mdv_attr, force=True)
                    cmds.connectAttr(input_mdv, name_normalize + '.input1X', force=True)
                    cmds.connectAttr(corr + '.endRotation', name_normalize + '.input2X', force=True)
                    #cmds.setAttr(name_normalize + '.input2X', 90)
                    cmds.setAttr(name_normalize + '.operation', 2)
                    cmds.setAttr(corr + '.multiplier', mult_value * 90)
                    cmds.setAttr(corr + '.startMultiplier', mult_value * 90 / 2)
            else:
                cmds.setAttr(corr + '.startMultiplier', mult_value / 2)
        om.MGlobal.displayInfo('"startMultiplier" attribute successfuly added on corrective joint "%s".'%corr)
    cmds.select(selection_list, replace=True)

#pvAddStartMultiplier()