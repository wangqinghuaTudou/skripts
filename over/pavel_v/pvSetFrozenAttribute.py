import maya.cmds as cmds
import maya.OpenMaya as om

def pvSetFrozenAttribute():

    if cmds.window('pvSetFrozenAttribute_ui', exists=True):
        cmds.deleteUI('pvSetFrozenAttribute_ui')

    cmds.window('pvSetFrozenAttribute_ui', \
              sizeable=False, \
              width=150, \
              height=100, \
              title='Rename Objects')

    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=3, style='none')
    cmds.rowColumnLayout(numberOfColumns=4, \
                       columnAttach=[1, 'left', 20], \
                       columnWidth=[[1, 90], [2, 150], [3, 50], [4, 80]])
    cmds.text(align='left', label='Prefix:')
    cmds.text(align='left', label='Name:')
    cmds.text(align='left', label='Digits:')
    cmds.text(align='left', label='Suffix:')
    cmds.setParent('..')

    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(numberOfColumns=4, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[1, 80], [2, 150], [3, 50], [4, 80]])
    cmds.optionMenuGrp('pvRenPrefOptMenGrp', columnWidth=[1, 50])
    for item in prefixList:
        cmds.menuItem(label=item)
    cmds.optionMenuGrp('pvRenPrefOptMenGrp', edit=True, select=2)
    cmds.textField('pvRenNameTexFld', text='')
    cmds.textField('pvRenDigTexFld', text='##')
    cmds.optionMenuGrp('pvRenSuffOptMenGrp', columnWidth=[1, 50])
    for item in suffixList:
        cmds.menuItem(label=item)
    cmds.optionMenuGrp('pvRenSuffOptMenGrp', edit=True, select=2)
    cmds.setParent('..')

    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='in')
    cmds.rowColumnLayout(numberOfColumns=3, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[1, 100], [2, 155], [3, 80]])
    cmds.radioCollection('pvRenRadCol')
    cmds.radioButton('pvRenRadButtSel', label='Selected')
    cmds.radioButton('pvRenRadButtHier', label='Hierarchy')
    cmds.radioCollection('pvRenRadCol', edit=True, select='pvRenRadButtSel')
    cmds.button('pvRenRunButt', \
           label='OK', \
           width=80, \
           command='pvSetFrozenAttributeMain(%s)'%state)

    cmds.showWindow('pvSetFrozenAttribute_ui')

def pvSetFrozenAttributeMain(state=1):
    parents_list = cmds.ls(selection=True)
    for par in parents_list:
        try:
            cmds.setAttr(par + '.frozen', state)
        except Exception, err:
            om.MGlobal.displayInfo(par)
            om.MGlobal.displayInfo(err)
        desc_list = cmds.listRelatives(par, allDescendents=True, fullPath=True)
        if desc_list:
            for desc in desc_list:
                try:
                    cmds.setAttr(desc + '.frozen', state)
                except Exception, err:
                    om.MGlobal.displayInfo(desc)
                    om.MGlobal.displayInfo(err)
        meshes_list = cmds.listRelatives(par, allDescendents=True, fullPath=True, type='mesh')
        if meshes_list:
            for mesh in meshes_list:
                hist_list = cmds.listHistory(mesh, pruneDagObjects=True)
                if hist_list:
                    for deform in hist_list:
                        try:
                            cmds.setAttr(deform + '.frozen', state)
                        except Exception, err:
                            om.MGlobal.displayInfo(deform)
                            om.MGlobal.displayInfo(err)