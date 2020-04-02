import maya.cmds as mc
import maya.OpenMaya as om
import re
from pvProcedures import *

selectedChar = ''

def pvMirrorPose():

    global selectedChar

    win = 'pvMirrorPose_ui'

    if mc.window(win, exists=True):
        mc.deleteUI(win)
    mc.window(win, \
              sizeable=False, \
              width=210, \
              height=50, \
              title='Mirror Pose.')

    mc.columnLayout(adjustableColumn=True)
    mc.separator(height=5, style='none')
    mc.columnLayout(adjustableColumn=False, columnAttach=['left', 15])
    mc.text(align='left', label='Select Character or Controller(s):')
    mc.setParent('..')
    mc.rowColumnLayout(numberOfColumns=3, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[2, 30], [2, 130], [3, 50]])
    mc.button('pvMirrorPoseSelButt', \
               label='Sel', \
               width=30, \
               command='pvMirrPoseSelChar()', \
               enable=False)
    mc.optionMenuGrp('pvMirrorPoseOptMenGrp', columnWidth=[1, 130], enable=False)
    nsList = pvGetNameSpaces()
    if nsList:
        selectedChar = nsList[0]

    if not mc.ls(selection=True) and nsList:
        nsList.sort()
        mc.button('pvMirrorPoseSelButt', edit=True, enable=True)
        mc.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=True)
        for item in nsList:
            mc.menuItem(label=item)

    mc.button('pvMirrorPoseRunButt', \
               label='Mirror', \
               width=50, \
               command='pvMirrPoseMain()')

    mc.showWindow(win)

    mc.scriptJob(parent=win, event=['SelectionChanged', 'pvMirrorPoseRefreshUI()'])

def pvMirrorPoseClearUI():

    global selectedChar

    if not mc.window('pvMirrorPose_ui', exists=True):
        return

    menuState = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)
    if menuState:
        selectedChar = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)
        menuItems = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, itemListLong=True)
        if menuItems:   
            for item in menuItems:
                mc.deleteUI(item)
            mc.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=False)
    else:
        return

def pvMirrorPoseRefreshUI():

    if not mc.window('pvMirrorPose_ui', exists=True):
        return

    nsList = pvGetNameSpaces()
    if not mc.ls(selection=True) and nsList:
        nsList.sort()
        pvMirrorPoseClearUI()
        mc.button('pvMirrorPoseSelButt', edit=True, enable=True)
        mc.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, enable=True)
        for item in nsList:
            mc.menuItem(label=item, parent='pvMirrorPoseOptMenGrp|OptionMenu')
        mc.optionMenuGrp('pvMirrorPoseOptMenGrp', edit=True, value=selectedChar)
    else:
        pvMirrorPoseClearUI()
        mc.button('pvMirrorPoseSelButt', edit=True, enable=False)

def pvMirrPoseSelChar():

    selCtrlsList = []
    menuState = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)

    if menuState:
        ns = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)

        middleCtList = ['body_CT', 'waist_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', 'Torso_CT', 'up_torso_CT', 'neck_CT', \
                        'head_CT', 'neckBend_CT', 'hips_CT', 'belt_CT', 'Pelvis_CT', 'vorotnik_CT', 'eyesAim_CT']

        leftCtList = ['l_handIk_CT', 'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'l_upLeg_CT', 'l_knee_CT', 'l_foot_CT', \
                      'l_upArmBend_CT', 'l_foreArmBend_CT', 'l_armMidBend__CT', 'l_armMidBend_CT', 'l_upLegBend_CT', \
                      'l_lowLegBend_CT', 'l_legMidBend__CT', 'l_legMidBend_CT', 'l_pinky_CT', 'l_ring_CT', 'l_middle_CT', \
                      'l_index_CT', 'l_thumb_CT', 'l_elbowIk_CT', 'l_shoulder_CT', 'l_footIk_CT', 'l_kneeIk_CT', 'l_pinkyIk_CT', \
                      'l_ringIk_CT', 'l_middleIk_CT', 'l_indexIk_CT', 'l_thumbIk_CT']

        for each in middleCtList:
            currCT = ns + each
            if mc.objExists(currCT):
                selCtrlsList.append(currCT)

        for each in leftCtList:
            currCT = ns + each
            if mc.objExists(currCT):
                selCtrlsList.append(currCT)
                side = ''
                mainName = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if mc.objExists(oppCT):
                    selCtrlsList.append(oppCT)
        
        mc.select(clear=True)
        for each in selCtrlsList:
            try:
                mc.select(each, add=True)
            except:
                print 'Controller "%s" has multiply instances.'%each

def pvMirrPoseMain():

    middleCtList = ['body_CT', 'waist_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', 'Torso_CT', 'up_torso_CT', 'neck_CT', \
                    'head_CT', 'neckBend_CT', 'hips_CT', 'belt_CT', 'Pelvis_CT', 'vorotnik_CT', 'eyesAim_CT']

    leftCtList = ['l_handIk_CT', 'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'l_upLeg_CT', 'l_knee_CT', 'l_foot_CT', \
                  'l_upArmBend_CT', 'l_foreArmBend_CT', 'l_armMidBend__CT', 'l_armMidBend_CT', 'l_upLegBend_CT', \
                  'l_lowLegBend_CT', 'l_legMidBend__CT', 'l_legMidBend_CT', 'l_pinky_CT', 'l_ring_CT', 'l_middle_CT', \
                  'l_index_CT', 'l_thumb_CT', 'l_elbowIk_CT', 'l_shoulder_CT', 'l_footIk_CT', 'l_kneeIk_CT', 'l_pinkyIk_CT', \
                  'l_ringIk_CT', 'l_middleIk_CT', 'l_indexIk_CT', 'l_thumbIk_CT']

    objList = mc.ls(selection=True)
    menuState = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, enable=True)
    
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

                if mainName in middleCtList:
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
    
                    if mc.objExists(oppCT):
                        try:
                            if mc.attributeQuery('limb', node=oppCT, exists=True):
                                limb = mc.getAttr('%s.limb'%oppCT)
                            if 'shoulder' in oppCT or 'elbowIk' in oppCT or 'kneeIk' in oppCT:
                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                            elif 'footIk' in oppCT:
                                switch = '%sswitch_CT'%ns
                                
                                lleg = mc.getAttr('%s.l_legIkFkSwitch'%switch)
                                rleg = mc.getAttr('%s.r_legIkFkSwitch'%switch)

                                mc.setAttr('%s.l_legIkFkSwitch'%switch, rleg)
                                mc.setAttr('%s.r_legIkFkSwitch'%switch, lleg)
                                
                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                            elif 'handIk' in oppCT or \
                                 'pinkyIk' in oppCT or \
                                 'ringIk' in oppCT or \
                                 'middleIk' in oppCT or \
                                 'indexIk' in oppCT or \
                                 'thumbIk' in oppCT:
                                switch = '%sswitch_CT'%ns
                                
                                larm = mc.getAttr('%s.l_armIkFkSwitch'%switch)
                                rarm = mc.getAttr('%s.r_armIkFkSwitch'%switch)

                                mc.setAttr('%s.l_armIkFkSwitch'%switch, rarm)
                                mc.setAttr('%s.r_armIkFkSwitch'%switch, larm)
                                
                                pvMirrorChannelsSide(currCT, oppCT, tx=-1, ty=-1, tz=-1, rx=1, ry=1, rz=1)
                            elif 'Bend' in oppCT and 'arm' in limb:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=-1, tz=1, rx=1, ry=1, rz=1)
                            elif 'Bend' in oppCT and 'leg' in limb:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=-1, rx=1, ry=1, rz=1)
                            else:
                                pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1)
        
                            pvMirrorAddChannels(currCT, oppCT)
        
                        except:
                            print 'Controller "%s" has multiply instances.'%currCT

            elif lookLikeMid:
                ns = lookLikeMid.groups()[0]
                mainName = lookLikeMid.groups()[1]

                if mainName in middleCtList:
                    if 'dw_waist_CT' in currCT or 'up_waist_CT' in currCT or 'waist_CT' in currCT or 'neck_CT' in currCT:
                        pvMirrorChannelsMiddle(currCT, tx=1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                    elif 'neckBend_CT' in currCT:
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                    else:
                        pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)

            else:
                om.MGlobal.displayWarning('Selected object "%s" isn\'t controller.'%currCT)
                return

    elif menuState:
        ns = mc.optionMenuGrp('pvMirrorPoseOptMenGrp', query=True, value=True)

        switch = '%sswitch_CT'%ns

        larm = mc.getAttr('%s.l_armIkFkSwitch'%switch)
        rarm = mc.getAttr('%s.r_armIkFkSwitch'%switch)
        lleg = mc.getAttr('%s.l_legIkFkSwitch'%switch)
        rleg = mc.getAttr('%s.r_legIkFkSwitch'%switch)

        mc.setAttr('%s.l_armIkFkSwitch'%switch, rarm)
        mc.setAttr('%s.r_armIkFkSwitch'%switch, larm)
        mc.setAttr('%s.l_legIkFkSwitch'%switch, rleg)
        mc.setAttr('%s.r_legIkFkSwitch'%switch, lleg)

        for each in middleCtList:
            currCT = ns + each
            if mc.objExists(currCT):
                if each == 'dw_waist_CT' or each == 'up_waist_CT' or each == 'waist_CT' or each == 'neck_CT':
                    pvMirrorChannelsMiddle(currCT, tx=1, ty=1, tz=1, rx=1, ry=-1, rz=-1)
                elif each == 'neckBend_CT':
                    pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=1, rz=1)
                else:
                    pvMirrorChannelsMiddle(currCT, tx=-1, ty=1, tz=1, rx=1, ry=-1, rz=-1)

        for each in leftCtList:
            currCT = ns + each
            if mc.objExists(currCT):
                side = ''
                mainName = ''
                limb = ''
                rex = re.compile(r'^([lr]{1}_)([a-zA-Z0-9]*_*CT)$')
                lookLike = rex.match(each)
                if lookLike:
                    side = lookLike.groups()[0]
                    mainName = lookLike.groups()[1]
                
                oppCT = ns + side.replace('l_', 'r_') + mainName
                if mc.objExists(oppCT):
                    try:
                        if mc.attributeQuery('limb', node=oppCT, exists=True):
                            limb = mc.getAttr('%s.limb'%oppCT)
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
                        print 'Controller "%s" has multiply instances.'%currCT

    else:
        print 'If you see this, some kind of Magic happens here!'

def pvMirrorChannelsMiddle(ctrl, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1):

    tr = mc.getAttr('%s.translate'%ctrl)[0]

    if not mc.getAttr('%s.translateX'%ctrl, l=True):
        mc.setAttr('%s.translateX'%ctrl, tr[0] * tx)
    if not mc.getAttr('%s.translateY'%ctrl, l=True):
        mc.setAttr('%s.translateY'%ctrl, tr[1] * ty)
    if not mc.getAttr('%s.translateZ'%ctrl, l=True):
        mc.setAttr('%s.translateZ'%ctrl, tr[2] * tz)

    rt = mc.getAttr('%s.rotate'%ctrl)[0]

    if not mc.getAttr('%s.rotateX'%ctrl, l=True):
        mc.setAttr('%s.rotateX'%ctrl, rt[0] * rx)
    if not mc.getAttr('%s.rotateY'%ctrl, l=True):
        mc.setAttr('%s.rotateY'%ctrl, rt[1] * ry)
    if not mc.getAttr('%s.rotateZ'%ctrl, l=True):
        mc.setAttr('%s.rotateZ'%ctrl, rt[2] * rz)

def pvMirrorChannelsSide(currCT, oppCT, tx=1, ty=1, tz=1, rx=1, ry=1, rz=1):

    currTr = mc.getAttr('%s.translate'%currCT)[0]
    currRt = mc.getAttr('%s.rotate'%currCT)[0]
    
    oppTr = mc.getAttr('%s.translate'%oppCT)[0]
    oppRt = mc.getAttr('%s.rotate'%oppCT)[0]

    if not mc.getAttr('%s.translateX'%currCT, l=True):
        mc.setAttr('%s.translateX'%currCT, oppTr[0] * tx)
    if not mc.getAttr('%s.translateY'%currCT, l=True):
        mc.setAttr('%s.translateY'%currCT, oppTr[1] * ty)
    if not mc.getAttr('%s.translateZ'%currCT, l=True):
        mc.setAttr('%s.translateZ'%currCT, oppTr[2] * tz)

    if not mc.getAttr('%s.rotateX'%currCT, l=True):
        mc.setAttr('%s.rotateX'%currCT, oppRt[0] * rx)
    if not mc.getAttr('%s.rotateY'%currCT, l=True):
        mc.setAttr('%s.rotateY'%currCT, oppRt[1] * ry)
    if not mc.getAttr('%s.rotateZ'%currCT, l=True):
        mc.setAttr('%s.rotateZ'%currCT, oppRt[2] * rz)

    if not mc.getAttr('%s.translateX'%oppCT, l=True):
        mc.setAttr('%s.translateX'%oppCT, currTr[0] * tx)
    if not mc.getAttr('%s.translateY'%oppCT, l=True):
        mc.setAttr('%s.translateY'%oppCT, currTr[1] * ty)
    if not mc.getAttr('%s.translateZ'%oppCT, l=True):
        mc.setAttr('%s.translateZ'%oppCT, currTr[2] * tz)

    if not mc.getAttr('%s.rotateX'%oppCT, l=True):
        mc.setAttr('%s.rotateX'%oppCT, currRt[0] * rx)
    if not mc.getAttr('%s.rotateY'%oppCT, l=True):
        mc.setAttr('%s.rotateY'%oppCT, currRt[1] * ry)
    if not mc.getAttr('%s.rotateZ'%oppCT, l=True):
        mc.setAttr('%s.rotateZ'%oppCT, currRt[2] * rz)

def pvMirrorAddChannels(currCT, oppCT):

    keyAttrsList = mc.listAttr(currCT, ud=True, k=True, u=True)
    unkeyAttrsList = mc.listAttr(currCT, ud=True, v=True, u=True, cb=True)
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
            v = mc.getAttr('%s.%s'%(currCT, each))
            currCTattrs[each] = v
            v = mc.getAttr('%s.%s'%(oppCT, each))
            oppCTattrs[each] = v

    if addAttrsList:
        for each in addAttrsList:
            mc.setAttr('%s.%s'%(currCT, each), oppCTattrs[each])
            mc.setAttr('%s.%s'%(oppCT, each), currCTattrs[each])