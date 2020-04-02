import maya.cmds as cmds
import maya.OpenMaya as om
from pvProcedures import *
import re


selectedChar = ''

def pvMirrorPose():

    om.MGlobal.displayInfo('Successful.')
    global selectedChar
    win = 'pvMirrorPose_ui'

    if cmds.window(win, exists=True):
        cmds.deleteUI(win)
    cmds.window(win, \
              sizeable=False, \
              width=210, \
              height=50, \
              title='Mirror Pose.')

    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='none')
    cmds.columnLayout(adjustableColumn=False, columnAttach=['left', 15])
    cmds.text(align='left', label='Select Character or Controller(s):')
    cmds.setParent('..')
    cmds.rowColumnLayout(numberOfColumns=3, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[2, 30], [2, 130], [3, 50]])
    cmds.button('pvMirrorPoseSelButt', \
               label='Sel', \
               width=30, \
               command='pvMirrPoseSelChar()', \
               enable=False)
    cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', columnWidth=[1, 130], enable=False)
    nsList = pvGetNameSpaces()
    if nsList:
        selectedChar = nsList[0]

    if not cmds.ls(selection=True) and nsList:
        nsList.sort()
        cmds.button('pvMirrorPoseSelButt', edit=True, enable=True)
        cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=True)
        for item in nsList:
            cmds.menuItem(label=item)

    cmds.button('pvMirrorPoseRunButt', \
               label='Mirror', \
               width=50, \
               command='pvMirrPoseMain()')

    cmds.showWindow(win)

    cmds.scriptJob(parent=win, event=['SelectionChanged', 'pvMirrorPoseRefreshUI()'])


def pvMirrorPoseClearUI():

    global selectedChar

    if not cmds.window('pvMirrorPose_ui', exists=True):
        return

    menuState = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)
    if menuState:
        selectedChar = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)
        menuItems = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, itemListLong=True)
        if menuItems:   
            for item in menuItems:
                cmds.deleteUI(item)
            cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=False)
    else:
        return


def pvMirrorPoseRefreshUI():

    if not cmds.window('pvMirrorPose_ui', exists=True):
        return

    nsList = pvGetNameSpaces()
    if not cmds.ls(selection=True) and nsList:
        nsList.sort()
        pvMirrorPoseClearUI()
        cmds.button('pvMirrorPoseSelButt', edit=True, enable=True)
        cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=True)
        for item in nsList:
            cmds.menuItem(label=item, parent='pvMirrorPoseOptMenGrp|OptionMenu')
        cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, value=selectedChar)
    else:
        pvMirrorPoseClearUI()
        cmds.button('pvMirrorPoseSelButt', edit=True, enable=False)


def pvMirrPoseSelChar():

    selCtrlsList = []
    menuState = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)

    if menuState:
        ns = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)

        middleCtList = ['body_CT', 'waist_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', 'Torso_CT', 'up_torso_CT', 'neck_CT', \
                        'head_CT', 'neckBend_CT', 'hips_CT', 'belt_CT', 'Pelvis_CT', 'vorotnik_CT', 'eyesAim_CT']

        leftCtList = ['l_handIk_CT', 'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'l_upLeg_CT', 'l_knee_CT', 'l_foot_CT', \
                      'l_upArmBend_CT', 'l_foreArmBend_CT', 'l_armMidBend__CT', 'l_armMidBend_CT', 'l_upLegBend_CT', \
                      'l_lowLegBend_CT', 'l_legMidBend__CT', 'l_legMidBend_CT', 'l_pinky_CT', 'l_ring_CT', 'l_middle_CT', \
                      'l_index_CT', 'l_thumb_CT', 'l_elbowIk_CT', 'l_shoulder_CT', 'l_footIk_CT', 'l_kneeIk_CT', 'l_pinkyIk_CT', \
                      'l_ringIk_CT', 'l_middleIk_CT', 'l_indexIk_CT', 'l_thumbIk_CT']

        faceMiddleCtList = ['cntr_bendLine_CT', 'topTeeth_CT', 'botTeeth_CT', 'tongueBase01_CT', 'tongueBase02_CT', 'tongueBase03_CT', \
                            'eyesAim_CT', 'MouthFace_CT', 'jaw_CT', 'chin_CT', 'cntr_BotLip_CT', 'cntr_TopLip_CT', 'mouth_CT', \
                            'cntr_nose_CT']

        faceLeftCtList = ['l_blink_CT', 'l_eyelidBot_CT', 'l_eyelidTop_CT', 'l_eyeAim_CT', 'l_BotLip_CT', 'l_lipCornerMouth_CT', \
                          'l_cornerMouth_CT', 'l_cornerTopPinch_CT', 'l_cornerBotPinch_CT', 'l_TopLip_CT', 'l_cheek_CT', \
                          'l_cheekSquintIn_CT', 'l_noseSquint_CT', 'l_cheekSquintOut_CT', 'l_eye_CT', 'l_browIn_CT', 'l_browMid_CT', \
                          'l_browOut_CT', 'l_ear01_CT', 'l_nose_CT']

        for each in middleCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                selCtrlsList.append(currCT)

        for each in faceMiddleCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                selCtrlsList.append(currCT)

        for each in leftCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                selCtrlsList.append(currCT)
                side = ''
                mainName = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if cmds.objExists(oppCT):
                    selCtrlsList.append(oppCT)
        
        for each in faceLeftCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                selCtrlsList.append(currCT)
                side = ''
                mainName = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if cmds.objExists(oppCT):
                    selCtrlsList.append(oppCT)

        cmds.select(clear=True)
        for each in selCtrlsList:
            try:
                cmds.select(each, add=True)
            except:
                om.MGlobal.displayInfo('Controller "%s" has multiply instances.'%each)


def pvMirrPoseMain():

    middleCtList = ['body_CT', 'waist_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', 'Torso_CT', 'up_torso_CT', 'neck_CT', \
                    'head_CT', 'neckBend_CT', 'hips_CT', 'belt_CT', 'Pelvis_CT', 'vorotnik_CT', 'eyesAim_CT']

    leftCtList = ['l_handIk_CT', 'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'l_upLeg_CT', 'l_knee_CT', 'l_foot_CT', \
                  'l_upArmBend_CT', 'l_foreArmBend_CT', 'l_armMidBend__CT', 'l_armMidBend_CT', 'l_upLegBend_CT', \
                  'l_lowLegBend_CT', 'l_legMidBend__CT', 'l_legMidBend_CT', 'l_pinky_CT', 'l_ring_CT', 'l_middle_CT', \
                  'l_index_CT', 'l_thumb_CT', 'l_elbowIk_CT', 'l_shoulder_CT', 'l_footIk_CT', 'l_kneeIk_CT', 'l_pinkyIk_CT', \
                  'l_ringIk_CT', 'l_middleIk_CT', 'l_indexIk_CT', 'l_thumbIk_CT']

    faceMiddleCtList = ['cntr_bendLine_CT', 'topTeeth_CT', 'botTeeth_CT', 'tongueBase01_CT', 'tongueBase02_CT', 'tongueBase03_CT', \
                        'eyesAim_CT', 'MouthFace_CT', 'jaw_CT', 'chin_CT', 'cntr_BotLip_CT', 'cntr_TopLip_CT', 'mouth_CT', \
                        'cntr_nose_CT']

    faceLeftCtList = ['l_blink_CT', 'l_eyelidBot_CT', 'l_eyelidTop_CT', 'l_eyeAim_CT', 'l_BotLip_CT', 'l_lipCornerMouth_CT', \
                      'l_cornerMouth_CT', 'l_cornerTopPinch_CT', 'l_cornerBotPinch_CT', 'l_TopLip_CT', 'l_cheek_CT', \
                      'l_cheekSquintIn_CT', 'l_noseSquint_CT', 'l_cheekSquintOut_CT', 'l_eye_CT', 'l_browIn_CT', 'l_browMid_CT', \
                      'l_browOut_CT', 'l_ear01_CT', 'l_nose_CT']

    objList = cmds.ls(selection=True)
    menuState = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)

    if not objList and not menuState:
        om.MGlobal.displayWarning('Must be specified any character or controller(s).')
        return
    elif objList:
        for currCT in objList:
            ns = ''
            side = ''
            mainName = ''
            limb = ''

            rex = re.compile(r'^([a-zA-Z0-9]*:)*([a-zA-Z]+_)+([a-zA-Z0-9]+_{1,2}CT)$')
            lookLike = rex.match(currCT)

            rexMid = re.compile(r'^([a-zA-Z0-9]*:)*([a-zA-Z0-9]+_{1,2}CT)$')
            lookLikeMid = rexMid.match(currCT)

            if lookLike:
                ns = lookLike.groups()[0]
                side = lookLike.groups()[1]
                mainName = lookLike.groups()[2]

                if mainName in middleCtList or mainName in faceMiddleCtList:
                    if 'dw_waist_CT' in currCT or 'up_waist_CT' in currCT or 'waist_CT' in currCT or 'neck_CT' in currCT:
                        pvMirrorChannelsMiddle(currCT, tx=1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                    elif 'neckBend_CT' in currCT:
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                    else:
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                else:
                    if side=='l_':
                        oppCT = ns + side.replace('l_', 'r_') + mainName
                    else:
                        oppCT = ns + side.replace('r_', 'l_') + mainName

                    if cmds.objExists(oppCT):
                        try:
                            if cmds.attributeQuery('limb', node=oppCT, exists=True):
                                limb = cmds.getAttr('%s.limb'%oppCT)
                            if 'shoulder' in oppCT or 'elbowIk' in oppCT or 'kneeIk' in oppCT:
                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)

                            elif 'footIk' in oppCT:
                                switch = '%sswitch_CT'%ns

                                leftLeg = cmds.getAttr('%s.l_legIkFkSwitch'%switch)
                                rightLeg = cmds.getAttr('%s.r_legIkFkSwitch'%switch)

                                cmds.setAttr('%s.l_legIkFkSwitch'%switch, rightLeg)
                                cmds.setAttr('%s.r_legIkFkSwitch'%switch, leftLeg)

                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                            elif 'handIk' in oppCT or \
                                 'pinkyIk' in oppCT or \
                                 'ringIk' in oppCT or \
                                 'middleIk' in oppCT or \
                                 'indexIk' in oppCT or \
                                 'thumbIk' in oppCT:
                                switch = '%sswitch_CT'%ns

                                leftArm = cmds.getAttr('%s.l_armIkFkSwitch'%switch)
                                rightArm = cmds.getAttr('%s.r_armIkFkSwitch'%switch)

                                cmds.setAttr('%s.l_armIkFkSwitch'%switch, rightArm)
                                cmds.setAttr('%s.r_armIkFkSwitch'%switch, leftArm)

                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=-1, tz=-1, rx=1, ry=1, rz=1)
                            elif 'Bend' in oppCT and 'arm' in limb:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=-1, tz=1, rx=1, ry=1, rz=1)
                            elif 'Bend' in oppCT and 'leg' in limb:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=-1, rx=1, ry=1, rz=1)
                            else:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1)

                            pvMirrorAddChannels(currCT, oppCT)

                        except:
                            om.MGlobal.displayInfo('Controller "%s" has multiply instances.'%currCT)

            elif lookLikeMid:
                ns = lookLikeMid.groups()[0]
                mainName = lookLikeMid.groups()[1]

                if mainName in middleCtList or mainName in faceMiddleCtList:
                    try:
                        if 'dw_waist_CT' in currCT or 'up_waist_CT' in currCT or 'waist_CT' in currCT or 'neck_CT' in currCT:
                            pvMirrorChannelsMiddle(currCT, tx=1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                        elif 'neckBend_CT' in currCT:
                            pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                        else:
                            pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                    except:
                            om.MGlobal.displayInfo('Controller "%s" has locked or connected attributes.'%currCT)

            else:
                om.MGlobal.displayWarning('Selected object "%s" isn\'t controller.'%currCT)
                return

    elif menuState:
        ns = cmds.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)

        switch = ns + 'switch_CT'

        leftArm = cmds.getAttr('%s.l_armIkFkSwitch'%switch)
        rightArm = cmds.getAttr('%s.r_armIkFkSwitch'%switch)
        leftLeg = cmds.getAttr('%s.l_legIkFkSwitch'%switch)
        rightLeg = cmds.getAttr('%s.r_legIkFkSwitch'%switch)

        cmds.setAttr('%s.l_armIkFkSwitch'%switch, rightArm)
        cmds.setAttr('%s.r_armIkFkSwitch'%switch, leftArm)
        cmds.setAttr('%s.l_legIkFkSwitch'%switch, rightLeg)
        cmds.setAttr('%s.r_legIkFkSwitch'%switch, leftLeg)

        for each in middleCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                try:
                    if each == 'dw_waist_CT' or each == 'up_waist_CT' or each == 'waist_CT' or each == 'neck_CT':
                        pvMirrorChannelsMiddle(currCT, tx=1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                    elif each == 'neckBend_CT':
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                    else:
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                except:
                    om.MGlobal.displayInfo('Controller "%s" has locked or connected attributes.'%currCT)

        for each in leftCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                side = ''
                mainName = ''
                limb = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if cmds.objExists(oppCT):
                    try:
                        if cmds.attributeQuery('limb', node=oppCT, exists=True):
                            limb = cmds.getAttr('%s.limb'%oppCT)
                        if 'shoulder' in oppCT or 'elbowIk' in oppCT or 'kneeIk' in oppCT:
                            pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                        elif 'footIk' in oppCT:
                            pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                        elif 'handIk' in oppCT or \
                             'pinkyIk' in oppCT or \
                             'ringIk' in oppCT or \
                             'middleIk' in oppCT or \
                             'indexIk' in oppCT or \
                             'thumbIk' in oppCT:
                            pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=-1, tz=-1, rx=1, ry=1, rz=1)
                        elif 'Bend' in oppCT and 'arm' in limb:
                            pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=-1, tz=1, rx=1, ry=1, rz=1)
                        elif 'Bend' in oppCT and 'leg' in limb:
                            pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=-1, rx=1, ry=1, rz=1)
                        else:
                            pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1)
    
                        pvMirrorAddChannels(currCT, oppCT)

                    except:
                        om.MGlobal.displayInfo('Controller "%s" has multiply instances.'%currCT)

        for each in faceMiddleCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                try:
                    pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                except:
                    om.MGlobal.displayInfo('Controller "%s" has locked or connected attributes.'%currCT)

        for each in faceLeftCtList:
            currCT = ns + each
            if cmds.objExists(currCT):
                side = ''
                mainName = ''
                limb = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if cmds.objExists(oppCT):
                    try:
                        pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                        pvMirrorAddChannels(currCT, oppCT)
                    except:
                        om.MGlobal.displayInfo('Controller "%s" has multiply instances.'%currCT)

    else:
        om.MGlobal.displayInfo('If you see this, some kind of Magic happens here!')


def pvMirrorChannelsMiddle(ctrl, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1):

    tr = cmds.getAttr('%s.translate'%ctrl)[0]

    if not cmds.getAttr('%s.translateX'%ctrl, l=True):
        cmds.setAttr('%s.translateX'%ctrl, tr[0] * tx)
    if not cmds.getAttr('%s.translateY'%ctrl, l=True):
        cmds.setAttr('%s.translateY'%ctrl, tr[1] * ty)
    if not cmds.getAttr('%s.translateZ'%ctrl, l=True):
        cmds.setAttr('%s.translateZ'%ctrl, tr[2] * tz)

    rt = cmds.getAttr('%s.rotate'%ctrl)[0]

    if not cmds.getAttr('%s.rotateX'%ctrl, l=True):
        cmds.setAttr('%s.rotateX'%ctrl, rt[0] * rx)
    if not cmds.getAttr('%s.rotateY'%ctrl, l=True):
        cmds.setAttr('%s.rotateY'%ctrl, rt[1] * ry)
    if not cmds.getAttr('%s.rotateZ'%ctrl, l=True):
        cmds.setAttr('%s.rotateZ'%ctrl, rt[2] * rz)


def pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1):

    currTr = cmds.getAttr('%s.translate'%currCT)[0]
    currRt = cmds.getAttr('%s.rotate'%currCT)[0]
    
    oppTr = cmds.getAttr('%s.translate'%oppCT)[0]
    oppRt = cmds.getAttr('%s.rotate'%oppCT)[0]

    if not cmds.getAttr('%s.translateX'%currCT, l=True):
        cmds.setAttr('%s.translateX'%currCT, oppTr[0] * tx)
    if not cmds.getAttr('%s.translateY'%currCT, l=True):
        cmds.setAttr('%s.translateY'%currCT, oppTr[1] * ty)
    if not cmds.getAttr('%s.translateZ'%currCT, l=True):
        cmds.setAttr('%s.translateZ'%currCT, oppTr[2] * tz)

    if not cmds.getAttr('%s.rotateX'%currCT, l=True):
        cmds.setAttr('%s.rotateX'%currCT, oppRt[0] * rx)
    if not cmds.getAttr('%s.rotateY'%currCT, l=True):
        cmds.setAttr('%s.rotateY'%currCT, oppRt[1] * ry)
    if not cmds.getAttr('%s.rotateZ'%currCT, l=True):
        cmds.setAttr('%s.rotateZ'%currCT, oppRt[2] * rz)

    if not cmds.getAttr('%s.translateX'%oppCT, l=True):
        cmds.setAttr('%s.translateX'%oppCT, currTr[0] * tx)
    if not cmds.getAttr('%s.translateY'%oppCT, l=True):
        cmds.setAttr('%s.translateY'%oppCT, currTr[1] * ty)
    if not cmds.getAttr('%s.translateZ'%oppCT, l=True):
        cmds.setAttr('%s.translateZ'%oppCT, currTr[2] * tz)

    if not cmds.getAttr('%s.rotateX'%oppCT, l=True):
        cmds.setAttr('%s.rotateX'%oppCT, currRt[0] * rx)
    if not cmds.getAttr('%s.rotateY'%oppCT, l=True):
        cmds.setAttr('%s.rotateY'%oppCT, currRt[1] * ry)
    if not cmds.getAttr('%s.rotateZ'%oppCT, l=True):
        cmds.setAttr('%s.rotateZ'%oppCT, currRt[2] * rz)


def pvMirrorAddChannels(currCT, oppCT):

    keyAttrsList = cmds.listAttr(currCT, ud=True, k=True, u=True)
    unkeyAttrsList = cmds.listAttr(currCT, ud=True, v=True, u=True, cb=True)
    if keyAttrsList and unkeyAttrsList:
        addAttrsList = keyAttrsList + unkeyAttrsList
    elif keyAttrsList:
        addAttrsList = keyAttrsList
    elif unkeyAttrsList:
        addAttrsList = unkeyAttrsList
    else:
        addAttrsList = None

    currCTattrs = {}
    oppCTattrs = {}
    if addAttrsList:
        for each in addAttrsList:
            v = cmds.getAttr('%s.%s'%(currCT, each))
            currCTattrs[each] = v
            v = cmds.getAttr('%s.%s'%(oppCT, each))
            oppCTattrs[each] = v

    if addAttrsList:
        for each in addAttrsList:
            cmds.setAttr('%s.%s'%(currCT, each), oppCTattrs[each])
            cmds.setAttr('%s.%s'%(oppCT, each), currCTattrs[each])