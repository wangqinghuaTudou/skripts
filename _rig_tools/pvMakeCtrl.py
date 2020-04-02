"""
-------------------------------------------------------------------------
       Script: pvMakeCtrl.py
       Author: Pavel Volokushin
        email: p.volokushin@gmail.com
Creation date: 15.02.2006
        Usage: pvMakeCtrl()
  Description: This script make controller from selected curve, oriented
               and rotated by source joint. And create point and orient
               constraints from controller to joint if necessary.
-------------------------------------------------------------------------
"""

import maya.cmds as mc

def pvMakeCtrl():
    if (mc.window('pvMakeCtrl_ui', exists=True)):
        mc.deleteUI('pvMakeCtrl_ui')
    mc.window('pvMakeCtrl_ui', \
              resizeToFitChildren=True, \
              sizeable=False, \
              title='Make Controller')
    mc.columnLayout(adjustableColumn=True)
    mc.text('<< Select Joint then Ctrl >>', align='center')
    mc.separator (height=5, style='out')
    # checkBox for moving controller to the joint
    mc.checkBox('pvCheckMCtr', value=0, label='Move Ctrl to Join', align='left')
    mc.separator(height=5, style='in')
    # checkBox for orienting controller by the joint
    mc.checkBox('pvCheckOCtr', value=1, label='Orient Ctrl by Join', align='left')
    mc.separator(height=5, style='in')
    # checkBox for rotating controller by the joint
    mc.checkBox('pvCheckRCtr', value=1, label='Rotate Ctrl by Joint', align='left')
    mc.separator(height=5, style='in')
    # checkBox for creating orient constraint from the controller to the joint
    mc.checkBox('pvCheckOCns', label='Orient Constraint to Joint', align='left')
    mc.separator(height=5, style='in')
    # checkBox for creating point constraint from the  controller to the joint
    mc.checkBox('pvCheckPCns', label='Point Constraint to Joint', align='left')
    mc.button(label='Run', command='pvMakeCtrlMain ()')
    mc.showWindow('pvMakeCtrl_ui')
	
def pvMakeCtrlMain ():
    # checking selection list 
    objList = mc.ls(selection=True)
    if len(objList) != 2:
        warning ('pvMakeCtrl :: Must be selected two objects "joint" and "controller".')
        return
    else:
        # define joint as source and controller as ctrl 
        source, ctrl = objList
        # extract main part of the joint's name 
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
        # define joints's rotation order
        rotOrd = mc.getAttr('%s.rotateOrder'%source)
        # define parent of controller
        parCtrl = mc.listRelatives(ctrl, parent=True)
        # create empty group under controller's parent 
        if parCtrl:
            currGrp = mc.group(parent=str(parCtrl), empty=True, name=conNull)
        else:
            currGrp = mc.group(empty=True, name=conNull)
        # set rotation order for the  controller and empty group
        mc.setAttr('%s.rotateOrder'%conNull, rotOrd)
        mc.setAttr('%s.rotateOrder'%ctrl, rotOrd)
        # orient empty group as joint if the corresponding check box is on
        if mc.checkBox('pvCheckOCtr', query=True, value=True):
            mc.delete(mc.orientConstraint (source, conNull, maintainOffset=False))
        # orient empty group as joint if the corresponding check box is on
        if mc.checkBox('pvCheckRCtr', query=True, value=True):
            mc.delete(mc.orientConstraint (source, ctrl, maintainOffset=False))
        # move empty group to the joint 
        mc.delete(mc.pointConstraint (source, conNull, maintainOffset=False))
        # move controller to the joint if the corresponding check box is on
        if mc.checkBox('pvCheckMCtr', query=True, value=True):
            mc.delete (mc.pointConstraint (source, ctrl, maintainOffset=False))
        # create new empty group for orientation
        mc.duplicate(conNull, name=oriNull)
        # parent groups and controller to each others in necessary order
        mc.parent(ctrl, conNull)
        mc.parent(conNull, oriNull)
        # freeze transformations one the controller
        mc.makeIdentity (ctrl, apply=True)
        # create constraints from controller to the joint if the corresponding check boxes is on
        if mc.checkBox('pvCheckPCns', query=True, value=True):
            mc.pointConstraint (ctrl, source, maintainOffset=True)
        if mc.checkBox('pvCheckOCns', query=True, value=True):
            mc.orientConstraint(ctrl, source, maintainOffset=True)
        # rename controller how it should be named 
        mc.rename(ctrl, ('%s_CT'%mainName))
        mc.select(clear=True)

# pvMakeCtrl()