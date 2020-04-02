import maya.cmds as cmds
import maya.OpenMaya as om
import pvProcedures as pvp
import CharacterNames as chn


def pvCheckIkFk ( *args ):

    if not args:
        args = cmds.ls( selection=True )
    if not args:
        om.MGlobal.displayWarning( 'Must be specified any object(s).' )
        return False

    controller_parts = chn.CharacterNames()
    suffixes_list = controller_parts.suffixes
    match_suffix = suffixes_list[9]
    #joint_suffix = suffixes_list[1]

    for controller in args:
        limb_attribute = controller + '.limb'
        if cmds.objExists( limb_attribute ):
            controller_namespace = pvp.pvGetNameSpaces()[0]
            current_limb = cmds.getAttr( limb_attribute )

            if current_limb == 'l_arm':
                controllers_list = controller_parts.getArm('l_')
                joints_list = controller_parts.getArmJnt('l_')
                match_list = []
                for c in controllers_list:
                    match_list.append( c.replace( '_CT', match_suffix ) )
                ik_joints_list = []
                for j in joints_list:
                    if '_jnt' in j:
                        ik_joints_list.append( j.replace( '_jnt', 'Ik_jnt' ) )
                    elif '_bind' in j:
                        ik_joints_list.append( j.replace( '_bind', 'Ik_jnt' ) )
                pvSwitchLimbIkFk ( controllers_list, ik_joints_list, current_limb, match_list, controller_namespace, controller_parts )

            if current_limb == 'r_arm':
                controllers_list = controller_parts.getArm('r_')
                joints_list = controller_parts.getArmJnt('r_')
                match_list = []
                for c in controllers_list:
                    match_list.append( c.replace( '_CT', match_suffix ) )
                ik_joints_list = []
                for j in joints_list:
                    if '_jnt' in j:
                        ik_joints_list.append( j.replace( '_jnt', 'Ik_jnt' ) )
                    elif '_bind' in j:
                        ik_joints_list.append( j.replace( '_bind', 'Ik_jnt' ) )
                pvSwitchLimbIkFk ( controllers_list, ik_joints_list, current_limb, match_list, controller_namespace, controller_parts )

            if current_limb == 'l_leg':
                controllers_list = controller_parts.getArm('l_')
                joints_list = controller_parts.getArmJnt('l_')
                match_list = []
                for c in controllers_list:
                    match_list.append( c.replace( '_CT', match_suffix ) )
                ik_joints_list = []
                for j in joints_list:
                    if '_jnt' in j:
                        ik_joints_list.append( j.replace( '_jnt', 'Ik_jnt' ) )
                    elif '_bind' in j:
                        ik_joints_list.append( j.replace( '_bind', 'Ik_jnt' ) )
                pvSwitchLimbIkFk ( controllers_list, ik_joints_list, current_limb, match_list, controller_namespace, controller_parts )

            if current_limb == 'r_leg':
                controllers_list = controller_parts.getArm('r_')
                joints_list = controller_parts.getArmJnt('r_')
                match_list = []
                for c in controllers_list:
                    match_list.append( c.replace( '_CT', match_suffix ) )
                ik_joints_list = []
                for j in joints_list:
                    if '_jnt' in j:
                        ik_joints_list.append( j.replace( '_jnt', 'Ik_jnt' ) )
                    elif '_bind' in j:
                        ik_joints_list.append( j.replace( '_bind', 'Ik_jnt' ) )
                pvSwitchLimbIkFk ( controllers_list, ik_joints_list, current_limb, match_list, controller_namespace, controller_parts )

def pvSwitchLimbIkFk ( controllers, ik_joints, current_limb, matches, controller_namespace, controller_parts ):

    ik_controller = controller_namespace + controllers[1]
    ik_polevector = controller_namespace + controllers[0]
    match_ik_controller = controller_namespace + matches[1]
    match_ik_polevector = controller_namespace + matches[0]
    fk_controller_upper = controller_namespace + controllers[2]
    fk_controller_lower = controller_namespace + controllers[3]
    fk_controller_tip = controller_namespace + controllers[4]
    match_fk_upper = controller_namespace + matches[2]
    match_fk_lower = controller_namespace + matches[3]
    match_fk_tip = controller_namespace + matches[4]
    ik_joint_upper = controller_namespace + ik_joints[1]
    ik_joint_lower = controller_namespace + ik_joints[2]
    ik_joint_tip = controller_namespace + ik_joints[3]
    shoulder_controller = controller_namespace + controllers[5] 
    switch_limb_attribute = controller_namespace + 'switch_CT.' + current_limb + 'IkFkSwitch'
    current_state = cmds.getAttr( switch_limb_attribute )

    ################################################
    # controllers = ['l_elbowIk_CT', 'l_handIk_CT', 'l_upArm_CT', 'l_foreArm_CT', 'l_hand_CT', 'l_shoulder_CT']
    # limbLarmMEL = ["l_upArm_CT", "l_foreArm_CT", "l_hand_CT", "l_handIk_CT", "l_elbowIk_CT"]

    # ik_joints = ['l_shoulder_jnt', 'l_upArm_jnt', 'l_foreArm_jnt', 'l_hand_bind']
    # jointsLarmIkMEL = ["l_upArm_IkJnt", "l_foreArm_IkJnt", "l_hand_IkJnt"]
    ################################################

    if (current_state == 0):

        limb_ik_translation = cmds.xform( match_ik_controller, query=True, worldSpace=True, translation=True )
        limb_ik_rotation = cmds.xform( match_ik_controller, query=True, worldSpace=True, rotation=True )
        limb_polevector_translation = cmds.xform( match_ik_polevector, query=True, worldSpace=True, translation=True )
        cmds.xform( ik_controller, worldSpace=True, translation=limb_ik_translation )
        cmds.xform( ik_controller, worldSpace=True, rotation=limb_ik_rotation )
        cmds.xform( ik_polevector, worldSpace=True, translation=limb_polevector_translation )

        limb_length_upper = cmds.getAttr( fk_controller_upper + '.length' )
        limb_length_lower = cmds.getAttr( fk_controller_lower + '.length' )
        cmds.setAttr( ik_controller + '.upLength', limb_length_upper )
        cmds.setAttr( ik_controller + '.dwLength', limb_length_lower )

        ################### soft ik ####################
        ################################################
        # k_soft = cmds.getAttr( controller_namespace + ik_joints[1] + '.K_soft' )
        # ik_softness = cmds.getAttr( ik_controller + '.softness' )
        # cmds.setAttr( ik_controller + '.upLength', limb_length_upper * (1 + k_soft) )
        # cmds.setAttr( ik_controller + '.dwLength', limb_length_lower * (1 + k_soft) )
        ################################################

        if 'arm' in current_limb:
            shoulder_translation = cmds.xform( shoulder_controller, query=True, worldSpace=True, translation=True )
            shoulder_rotation = cmds.xform( shoulder_controller, query=True, worldSpace=True, translation=True )
            cmds.setKeyframe( shoulder_controller, time=( cmds.currentTime( query=True )-1 ) )
            switch_state = abs( 1 - current_state )
            cmds.setAttr( switch_limb_attribute, switch_state )
            cmds.xform( shoulder_controller, worldSpace=True, translation=shoulder_translation )
            try:
                cmds.xform( shoulder_controller, worldSpace=True, translation=shoulder_rotation )
            except:
                pass
            switch_state = abs( 1 - current_state )
            cmds.setAttr( switch_limb_attribute, switch_state )

    elif current_state == 1:

        limb_fk_upper_rotation = cmds.xform( match_fk_upper, query=True, worldSpace=True, rotation=True )
        limb_fk_lower_rotation = cmds.xform( match_fk_lower, query=True, worldSpace=True, rotation=True )
        limb_fk_tip_rotation = cmds.xform( match_fk_tip, query=True, worldSpace=True, rotation=True )

        ik_upper_stretch = cmds.getAttr( ik_joint_lower + '.tx' )
        ik_lower_stretch = cmds.getAttr( ik_joint_tip + '.tx' )
        ik_upper_default_length = cmds.getAttr( ik_joint_upper + '.defLength' )
        ik_lower_default_length = cmds.getAttr( ik_joint_lower + '.defLength' )
        cmds.setAttr( fk_controller_upper + '.length', ik_upper_stretch / ik_upper_default_length )
        cmds.setAttr( fk_controller_lower + '.length', ik_lower_stretch / ik_lower_default_length )

        if 'arm' in current_limb:
            shoulder_translation = cmds.xform( shoulder_controller, query=True, worldSpace=True, translation=True )
            shoulder_rotation = cmds.xform( shoulder_controller, query=True, worldSpace=True, translation=True )
            cmds.setKeyframe( shoulder_controller, time=( cmds.currentTime( query=True )-1 ) )
            switch_state = abs( 1 - current_state )
            cmds.setAttr( switch_limb_attribute, switch_state )
            cmds.xform( shoulder_controller, worldSpace=True, translation=shoulder_translation )
            try:
                cmds.xform( shoulder_controller, worldSpace=True, translation=shoulder_rotation )
            except:
                pass
            switch_state = abs( 1 - current_state )
            cmds.setAttr( switch_limb_attribute, switch_state )

        cmds.xform( fk_controller_upper, worldSpace=True, rotation=limb_fk_upper_rotation )
        cmds.xform( fk_controller_lower, worldSpace=True, rotation=limb_fk_lower_rotation )
        cmds.xform( fk_controller_tip, worldSpace=True, rotation=limb_fk_tip_rotation )

    else:
        om.MGlobal.displayWarning( 'Something strange is going on here.' )

    cmds.setKeyframe( switch_limb_attribute, time=( cmds.currentTime( query=True )-1 ) )
    switch_state = abs( 1 - current_state )
    cmds.setAttr( switch_limb_attribute, switch_state )

    cmds.select( clear=True )

# pvCheckIkFk()