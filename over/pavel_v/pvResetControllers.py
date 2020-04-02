import maya.cmds as mc
import maya.OpenMaya as om
import re
from pvProcedures import *

selectedChar = ''

def pvResetControllers():

    global selectedChar

    win = 'pvResetControllers_ui'

    if mc.window(win, exists=True):
        mc.deleteUI(win)

    mc.window(win, \
              sizeable=False, \
              width=210, \
              height=50, \
              title='Reset Controllers.')

    mc.columnLayout(adjustableColumn=True)
    mc.separator(height=5, style='none')
    mc.columnLayout(adjustableColumn=False, columnAttach=['left', 15])
    mc.text(align='left', label='Select Character or Controller(s):')
    mc.setParent('..')
    mc.rowColumnLayout(numberOfColumns=4, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[1, 150], [2, 70], [3, 20], [4, 50]])
    mc.optionMenuGrp('pvResetControllersOptMenGrp', columnWidth=[1, 150], enable=False)
    nsList = pvGetNameSpaces()
    if nsList:
        selectedChar = nsList[0]
    else:
        selectedChar = ''
    if not mc.ls(selection=True) and nsList:
        nsList.sort()
        mc.optionMenuGrp('pvResetControllersOptMenGrp', edit=True, enable=True)
        for item in nsList:
            mc.menuItem(label=item)

    mc.text('Add Attrs: ', align='right')
    mc.checkBox('pvResetControllersCheckBox', value=False, label='')

    mc.button('pvResetControllersRunButt', \
               label='Reset', \
               width=50, \
               command='pvResetControllersMain()')

    mc.showWindow(win)

    mc.scriptJob(parent=win, event=['SelectionChanged', 'pvResetControllersRefreshUI()'])

def pvResetControllersClearUI():

    global selectedChar

    if not mc.window('pvResetControllers_ui', exists=True):
        return
    
    menuState = mc.optionMenuGrp('pvResetControllersOptMenGrp', query=True, enable=True)
    if menuState:
        selectedChar = mc.optionMenuGrp('pvResetControllersOptMenGrp', query=True, value=True)
        menuItems = mc.optionMenuGrp('pvResetControllersOptMenGrp', query=True, itemListLong=True)
        if menuItems:    
            for item in menuItems:
                mc.deleteUI(item)
            mc.optionMenuGrp('pvResetControllersOptMenGrp', edit=True, enable=False)
    else:
        #pvResetControllersClearUI()
        return

def pvResetControllersRefreshUI():

    if not mc.window('pvResetControllers_ui', exists=True):
        return

    nsList = pvGetNameSpaces()
    if not mc.ls(selection=True) and nsList:
        nsList.sort()
        pvResetControllersClearUI()
        mc.optionMenuGrp('pvResetControllersOptMenGrp', edit=True, enable=True)
        for item in nsList:
            mc.menuItem(label=item, parent='pvResetControllersOptMenGrp|OptionMenu')
        mc.optionMenuGrp('pvResetControllersOptMenGrp', edit=True, value=selectedChar)
    else:
        pvResetControllersClearUI()

def pvResetControllersMain():

    objList = mc.ls(selection=True)
    menuState = mc.optionMenuGrp('pvResetControllersOptMenGrp', query=True, enable=True)
    
    if not objList and not menuState:
        om.MGlobal.displayWarning('Must be specified any character or controller(s).')
        return
        
    if objList:
        for currCT in objList:
            allAttrsList = mc.listAttr(currCT, k=True, u=True)
            keyAttrsList = mc.listAttr(currCT, ud=True, k=True, u=True)
            unkeyAttrsList = mc.listAttr(currCT, ud=True, v=True, u=True, cb=True)
            if keyAttrsList and unkeyAttrsList:
                addAttrsList = keyAttrsList + unkeyAttrsList
            elif keyAttrsList:
                addAttrsList = keyAttrsList
            elif unkeyAttrsList:
                addAttrsList = unkeyAttrsList
            else:
                addAttrsList = []

            if allAttrsList and addAttrsList:
                mainAttrsList = list(set(allAttrsList) - set(addAttrsList))
            elif allAttrsList:
                mainAttrsList = allAttrsList
                addAttrsList = []
            elif addAttrsList:
                mainAttrsList = []
                addAttrsList = allAttrsList
            else:
                om.MGlobal.displayInfo('Controller "%s" has no any attributes.'%currCT)
                mainAttrsList = []
                addAttrsList = []

            if mainAttrsList:
                for attr in mainAttrsList:
                    if 'scale' in attr or 'visibility' in attr:
                        try: 
                            mc.setAttr('%s.%s'%(currCT, attr), 1)
                        except:
                            pass
                    else:
                        try:
                            mc.setAttr('%s.%s'%(currCT, attr), 0)
                        except:
                            pass

            isAddAttrCheckBox = mc.checkBox('pvResetControllersCheckBox', query=True, value=True)
            if addAttrsList and isAddAttrCheckBox:
                for attr in addAttrsList:
                    try:
                        if attr == 'waistWide' or attr == 'length' or attr == 'Length' or attr == 'stretching' \
                        or attr == 'upLength' or attr == 'dwLength' or attr == 'softIK' or 'armCtrls' in attr \
                        or 'legCtrls' in attr or 'legIkFkSwitch' in attr or 'hairVis' in attr or 'jacketFurVis' in attr \
                        or attr == 'proxyBody' or attr == 'proxyHead' or attr == 'hairsVis' or attr == 'addCtrls':
                            mc.setAttr('%s.%s'%(currCT, attr), 1)
                        elif attr == 'AutoShoulder':
                            mc.setAttr('%s.%s'%(currCT, attr), 0.3)
                        elif attr == 'follow':
                            mc.setAttr('%s.%s'%(currCT, attr), 0.4)
                        elif attr == 'bodyCtrls' or attr == 'softness':
                            mc.setAttr('%s.%s'%(currCT, attr), 1)
                        elif 'Cloth' in attr:
                            mc.setAttr('%s.%s'%(currCT, attr), 2)
                        elif 'space' in attr:
                            if 'elbowIk_CT' in currCT: #or 'handIk_CT' in currCT or 'elbowIk_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 0)
                            elif 'kneeIk_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 3)
                        elif 'tSpace' in attr:
                            if 'head_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 3)
                        elif 'rSpace' in attr:
                            if 'head_CT' in currCT or 'upLeg_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 0)
                            elif 'eyesAim_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 2)
                            elif 'upArm_CT' in currCT:
                                mc.setAttr('%s.%s'%(currCT, attr), 3)
                        else:
                            mc.setAttr('%s.%s'%(currCT, attr), 0)
                    except:
                            print 'Attribute "%s" on controller "%s" can not be setting to default.'%(attr, currCT)

    if menuState:
        ns = mc.optionMenuGrp('pvResetControllersOptMenGrp', query=True, value=True)

        objList = ['switch_CT', 'general_CT', 'pivotOffset_CT', 'body_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', \
                   'up_torso_CT', 'hips_CT', 'head_CT', 'neck_CT', 'neckBend_CT', 'l_shoulder_CT', \
                   'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'r_shoulder_CT', 'r_upArm_CT', 'r_foreArm_CT', 'r_hand_CT', \
                   'r_upLeg_CT', 'r_knee_CT', 'r_foot_CT', 'l_upLeg_CT', 'l_knee_CT', 'l_foot_CT', 'l_upArmBend_CT', \
                   'l_foreArmBend_CT', 'l_armMidBend__CT', 'r_upArmBend_CT', 'r_foreArmBend_CT', 'r_armMidBend__CT', \
                   'l_upLegBend_CT', 'l_lowLegBend_CT', 'l_legMidBend_CT', 'r_upLegBend_CT', 'r_lowLegBend_CT', \
                   'r_legMidBend_CT', 'l_pinky_CT', 'l_ring_CT', 'l_middle_CT', 'l_index_CT', 'r_index_CT', 'r_middle_CT', \
                   'r_ring_CT', 'r_pinky_CT', 'l_thumb_CT', 'r_thumb_CT', 'eyesAim_CT', 'r_eye_CT', 'l_eye_CT', 'l_elbowIk_CT ', \
                   'l_handIk_CT ', 'r_elbowIk_CT ', 'r_handIk_CT ', 'r_footIk_CT ', 'r_kneeIk_CT ', 'l_footIk_CT ', 'l_kneeIk_CT', \
                   'l_pinkyIk_CT ', 'l_ringIk_CT ', 'l_middleIk_CT ', 'l_indexIk_CT ', 'r_indexIk_CT ', 'r_middleIk_CT ', \
                   'r_ringIk_CT ', 'r_pinkyIk_CT ', 'l_thumbIk_CT ', 'r_thumbIk_CT']

        for each in objList:
            currCT = ns + each
            if mc.objExists(currCT):
                allAttrsList = mc.listAttr(currCT, k=True, u=True)
                keyAttrsList = mc.listAttr(currCT, ud=True, k=True, u=True)
                unkeyAttrsList = mc.listAttr(currCT, ud=True, v=True, u=True, cb=True)
                if keyAttrsList and unkeyAttrsList:
                    addAttrsList = keyAttrsList + unkeyAttrsList
                elif keyAttrsList:
                    addAttrsList = keyAttrsList
                elif unkeyAttrsList:
                    addAttrsList = unkeyAttrsList
                else:
                    addAttrsList = []
    
                if allAttrsList and addAttrsList:
                    mainAttrsList = list(set(allAttrsList) - set(addAttrsList))
                elif allAttrsList:
                    mainAttrsList = allAttrsList
                    addAttrsList = []
                elif addAttrsList:
                    mainAttrsList = []
                    addAttrsList = allAttrsList
                else:
                    om.MGlobal.displayInfo('Controller "%s" has no any attributes.'%currCT)
                    mainAttrsList = []
                    addAttrsList = []
    
                if mainAttrsList:
                    for attr in mainAttrsList:
                        if 'scale' in attr or 'visibility' in attr: 
                            mc.setAttr('%s.%s'%(currCT, attr), 1)
                        else:
                            mc.setAttr('%s.%s'%(currCT, attr), 0)
    
                if addAttrsList:
                    for attr in addAttrsList:
                        try:
                            if attr == 'waistWide' or attr == 'length' or attr == 'Length' or attr == 'stretching' \
                            or attr == 'upLength' or attr == 'dwLength' or attr == 'softIK' or 'armCtrls' in attr \
                            or 'legCtrls' in attr or 'armIkFkSwitch' in attr or 'legIkFkSwitch' in attr or 'hairVis' in attr or 'jacketFurVis' in attr \
                            or attr == 'bodyState' or attr == 'headState':
                                mc.setAttr('%s.%s'%(currCT, attr), 1)
                            elif attr == 'AutoShoulder':
                                mc.setAttr('%s.%s'%(currCT, attr), 0.3)
                            elif attr == 'follow':
                                mc.setAttr('%s.%s'%(currCT, attr), 0.4)
                            elif attr == 'bodyCtrls' or 'Cloth' in attr:
                                mc.setAttr('%s.%s'%(currCT, attr), 2)
                            elif 'space' in attr:
                                if 'kneeIk_CT' in currCT or 'handIk_CT' in currCT or 'elbowIk_CT' in currCT:
                                    mc.setAttr('%s.%s'%(currCT, attr), 0)
                                elif 'head_CT' in currCT:
                                    mc.setAttr('%s.%s'%(currCT, attr), 3)
                                elif 'eyesAim_CT' in currCT or 'upArm_CT' in currCT or 'upLeg_CT' in currCT:
                                    mc.setAttr('%s.%s'%(currCT, attr), 1)
                            else:
                                mc.setAttr('%s.%s'%(currCT, attr), 0)
                        except:
                            om.MGlobal.displayInfo('Attribute "%s" on controller "%s" can not be setting to default.'%(attr, currCT))