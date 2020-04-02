import maya.cmds as cmds
import maya.OpenMaya as om

def pvMakeCtrl():

    if (cmds.window('pvMakeCtrl_ui', exists=True)):
        cmds.deleteUI('pvMakeCtrl_ui')

    cmds.window('pvMakeCtrl_ui', \
                resizeToFitChildren=True, \
                sizeable=False, \
                title='Make Controller')

    cmds.columnLayout(adjustableColumn=True)
    cmds.text('<< Select Joint then Ctrl >>', align='center')
    cmds.separator (height=5, style='out')

    cmds.checkBox('pvCheckMCtr', value=1, label='Move Ctrl to Join', align='left')
    cmds.checkBox('pvCheckOCtr', value=1, label='Orient Ctrl by Join', align='left')
    cmds.checkBox('pvCheckRCtr', value=1, label='Rotate Ctrl by Joint', align='left')
    cmds.separator(height=5, style='in')

    cmds.text(align='left', label='Translate:')
    cmds.radioCollection('pvDriverTrRadColl')
    cmds.radioButton('pvDriverTrRadButtNone', label='None')
    cmds.radioButton('pvDriverTrRadButtConst', label='Constraint')
    cmds.radioButton('pvDriverTrRadButtConn', label='Connection')
    cmds.radioCollection('pvDriverTrRadColl', edit=True, select='pvDriverTrRadButtConst')
    cmds.separator(height=5, style='in')

    cmds.text(align='left', label='Rotate:')
    cmds.radioCollection('pvDriverRtRadColl')
    cmds.radioButton('pvDriverRtRadButtNone', label='None')
    cmds.radioButton('pvDriverRtRadButtConst', label='Constraint')
    cmds.radioButton('pvDriverRtRadButtConn', label='Connection')
    cmds.radioCollection('pvDriverRtRadColl', edit=True, select='pvDriverRtRadButtConst')

    cmds.button(label='Run', command='pvMakeCtrlMain ()')
    
    cmds.showWindow('pvMakeCtrl_ui')

def pvMakeCtrlMain (*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return
    if len(args) != 2:
        om.MGlobal.displayWarning('Must be selected two objects "joint" and "controller".')
        return

    source, ctrl = args
    if ('_bind' in source):
        conNull = source.replace('_bind', '_con')
        oriNull = source.replace('_bind','_ori')
        mainName = source[:-5]
    elif ('_jnt' in source):
        conNull = source.replace('_jnt', '_con')
        oriNull = source.replace('_jnt', '_ori')
        mainName = source[:-4]
    else:
        conNull = source + '_con'
        oriNull = source + '_ori'
        mainName = source

    rotOrd = cmds.getAttr('%s.rotateOrder'%source)

    parCtrl = cmds.listRelatives(ctrl, parent=True)
    if parCtrl:
        conNull = cmds.group(parent=str(parCtrl), empty=True, name=conNull)
    else:
        conNull = cmds.group(empty=True, name=conNull)

    cmds.setAttr('%s.rotateOrder'%conNull, rotOrd)
    cmds.setAttr('%s.rotateOrder'%ctrl, rotOrd)

    if cmds.checkBox('pvCheckOCtr', query=True, value=True):
        cmds.delete(cmds.orientConstraint (source, conNull, maintainOffset=False))
    if cmds.checkBox('pvCheckRCtr', query=True, value=True):
        cmds.delete(cmds.orientConstraint(source, ctrl, maintainOffset=False))

    cmds.delete(cmds.pointConstraint(source, conNull, maintainOffset=False))

    if cmds.checkBox('pvCheckMCtr', query=True, value=True):
        cmds.delete(cmds.pointConstraint (source, ctrl, maintainOffset=False))

    cmds.duplicate(conNull, name=oriNull)
    cmds.parent(ctrl, conNull)
    cmds.parent(conNull, oriNull)
    cmds.makeIdentity(ctrl, apply=True)

    if cmds.radioButton('pvDriverTrRadButtConst', query=True, select=True):
        cmds.pointConstraint(ctrl, source, maintainOffset=True)
    if cmds.radioButton('pvDriverTrRadButtConn', query=True, select=True):
        cmds.connectAttr(ctrl + '.translate', source + '.translate', force=True)
    if cmds.radioButton('pvDriverRtRadButtConst', query=True, select=True):
        cmds.orientConstraint(ctrl, source, maintainOffset=True)
    if cmds.radioButton('pvDriverRtRadButtConn', query=True, select=True):
        cmds.connectAttr(ctrl + '.rotate', source + '.rotate', force=True)

    cmds.rename(ctrl, ('%s_CT'%mainName))
    cmds.select(clear=True)

# pvMakeCtrl()