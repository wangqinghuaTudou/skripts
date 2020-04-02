def pvCreateGeoControllers():
    if mc.window('pvCGCwindow_ui', exists=True):
        mc.deleteUI('pvCGCwindow_ui')
    mc.window('pvCGCwindow_ui', \
              sizeable=False, \
              width=350, \
              height=100, \
              title='Create Geo Controllers.')
    mc.columnLayout(adjustableColumn=True)
    mc.separator(height=3, style='none')
    mc.columnLayout(adjustableColumn=False, \
                    columnAttach=['left', 10])
    mc.text(align='left', label='Assign skinned geometry:')
    mc.setParent('..')
    mc.separator(height=5, style='in')
    mc.rowColumnLayout(numberOfColumns=2, \
                       columnAttach=[1, 'left', 5], \
                       columnWidth=[[1, 140], [2, 50]])
    mc.textField('pvCGCtexFld', text='', width=135)
    mc.button('pvCGCassignButt', \
           label='Assign', \
           width=50, \
           command="mc.textField('pvCGCtexFld', edit=True, text=mc.ls(selection=True)[0])")
    mc.setParent('..')
    mc.columnLayout(adjustableColumn=False, \
                    columnAttach=['left', 5])
    mc.button('pvCGCrunButt', \
           label='Create Controllers', \
           width=135, \
           command='pvCreateGeoControllersMain()')

    mc.showWindow('pvCGCwindow_ui')

def pvCreateGeoControllersMain():
    mc.select(clear=True)
    mainMesh = mc.textField('pvCGCtexFld', query=True, text=True)
    ctList = [u'body_CT', u'dw_waist_CT', u'head_CT', u'hips_CT', u'l_armMidBend__CT', u'l_footIk_CT', u'l_foot_CT', \
              u'l_foreArmBend_CT', u'l_foreArm_CT', u'l_handIk_CT', u'l_hand_CT', u'l_index_CT', u'l_knee_CT', u'l_legMidBend__CT', \
              u'l_lowLegBend_CT', u'l_middle_CT', u'l_pinky_CT', u'l_ring_CT', u'l_shoulder_CT', u'l_thumb_CT', u'l_upArmBend_CT', \
              u'l_upArm_CT', u'l_upLegBend_CT', u'l_upLeg_CT', u'neckBend_CT', u'neck_CT', u'pelvis_CT', u'r_armMidBend__CT', \
              u'r_footIk_CT', u'r_foot_CT', u'r_foreArmBend_CT', u'r_foreArm_CT', u'r_handIk_CT', u'r_hand_CT', u'r_index_CT', \
              u'r_knee_CT', u'r_legMidBend__CT', u'r_lowLegBend_CT', u'r_middle_CT', u'r_pinky_CT', u'r_ring_CT', u'r_shoulder_CT', \
              u'r_thumb_CT', u'r_upArmBend_CT', u'r_upArm_CT', u'r_upLegBend_CT', u'r_upLeg_CT', u'torso_CT', u'up_torso_CT', \
              u'up_waist_CT']

    for ct in ctList:
        tgName = ct.replace('_CT', 'CT') + '_tg'
        meshName = mc.listRelatives(ct, shapes=True)[0]
        mc.createNode('transformGeometry', name=tgName)
        mc.connectAttr ('%s.worldInverseMatrix[0]'%ct, '%s.transform'%tgName, force=True)
        mc.connectAttr ('%s.outMesh'%mainMesh, '%s.inputGeometry'%tgName, force=True)
        meshName = mc.createNode('mesh', parent=ct, name=meshName)
        mc.connectAttr ('%s.outputGeometry'%tgName, '%s.inMesh'%meshName, force=True)