import maya.cmds as cmds
import maya.OpenMaya as om

def pvAddSelToTF(tf_name=''):
    sel_list = cmds.ls(sl=True)
    if not sel_list:
        om.MGlobal.displayWarning('Info: Must be specified any influences and skin cluster.')
    else:
        cmds.textField(tf_name, edit=True, text=str(sel_list[0]))

def pvAddInflToSkinRun():
    if cmds.textField('textJnt', exists=True):
        infl_list = cmds.textField('textJnt', query=True, text=True)
    if cmds.textField('textSkn', exists=True):
        skin_list = cmds.textField('textSkn', query=True, text=True)
        skin_list = cmds.ls(skin_list, type='skinCluster')
    if not infl_list or not skin_list:
        om.MGlobal.displayWarning('Info: Must be specified any influences and skin cluster.')
    else:
        try:
            cmds.skinCluster(skin_list, edit=True, addInfluence=infl_list)
            om.MGlobal.displayInfo('Info: Influence "%s" successfuly added to skin cluster "%s".'%(infl_list, skin_list))
        except Exception, err:
            om.MGlobal.displayWarning('Info: %s'%err)

def pvAddInflToSkin():
    if cmds.window('pvAddInflToSkin_ui', exists=True):
        cmds.deleteUI('pvAddInflToSkin_ui')
    addInflToSkinWindow = cmds.window('pvAddInflToSkin_ui', title='Add influence to SkinClsuter.', widthHeight=(370, 80), sizeable=False)
    cmds.columnLayout(adjustableColumn=True, height=80)
    cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'right', 0), columnWidth=[(1, 70), (2, 250), (3, 50)])
    cmds.text(label='Influence')
    cmds.textField('textJnt')
    cmds.button('buttJnt', label='<<<', command="pvAddSelToTF('textJnt')")
    cmds.text(label='SkinCluster')
    cmds.textField('textSkn')
    cmds.button('buttSkn', label='<<<', command="pvAddSelToTF('textSkn')")
    cmds.setParent('..')
    cmds.button('addInflToSkinRun', label='Add', command="pvAddInflToSkinRun()")
    cmds.setParent('..')
    cmds.showWindow(addInflToSkinWindow)

# pvAddInflToSkin()