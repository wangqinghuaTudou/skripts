

def pvSwitchLimbIkFk (limbParts, limbJoints,  currLimb, limbMatches, limbNamespace):

    currState = mc.getAttr ($nameSpace + "switch_CT." + $currLimb + "IkFkSwitch")` ;
    string $mainName[] ;
    string $temp[] ;
    float $limbAfkR[] ; 
    float $limbBfkR[] ; 
    float $limbCfkR[] ; 
    for ($i = 0; $i < 5; $i++)
    {
        tokenize $limbParts[$i] "_" $temp ;
        $mainName[$i] = $temp[0] + "_" + $temp[1] ;
    }

    if ($currState == 0)
    {
        $limbAikT = `xform -query -worldSpace -translation ($nameSpace + $limbMatches[3])` ;
        $limbAikR = `xform -query -worldSpace -rotation ($nameSpace + $limbMatches[3])` ;
        $limbBikT = `xform -query -worldSpace -translation ($nameSpace + $limbMatches[4])` ; 
        xform -worldSpace -translation $limbAikT[0] $limbAikT[1] $limbAikT[2] ($nameSpace + $limbParts[3]) ;
        xform -worldSpace -rotation $limbAikR[0] $limbAikR[1] $limbAikR[2] ($nameSpace + $limbParts[3]) ; 
        xform -worldSpace -translation $limbBikT[0] $limbBikT[1] $limbBikT[2] ($nameSpace + $limbParts[4]) ;

        $limbAlength1 = `getAttr ($nameSpace + $limbParts[0] + ".length")` ;
        $limbAlength2 = `getAttr ($nameSpace + $limbParts[1] + ".length")` ;
        setAttr ($nameSpace + $limbParts[3] + ".upLength") $limbAlength1 ;
        setAttr ($nameSpace + $limbParts[3] + ".dwLength") $limbAlength2 ;

        $k = `getAttr ($nameSpace + $limbJoints[1] + ".K_soft")` ;
        $softness = `getAttr ($nameSpace + $limbParts[3] + ".softness")` ;
        setAttr ($nameSpace + $limbParts[3] + ".upLength") ($limbAlength1 * (1 + $k)) ;
        setAttr ($nameSpace + $limbParts[3] + ".dwLength") ($limbAlength2 * (1 + $k)) ;
    }
    if ($currState == 1)
    {
        
        print ($nameSpace + $limbMatches[0]) ;
        $limbAfkR = `xform -query -worldSpace -rotation ($nameSpace + $limbMatches[0])` ;
        $limbBfkR = `xform -query -worldSpace -rotation ($nameSpace + $limbMatches[1])` ;
        $limbCfkR = `xform -query -worldSpace -rotation ($nameSpace + $limbMatches[2])` ;
        xform -worldSpace -rotation $limbAfkR[0] $limbAfkR[1] $limbAfkR[2] ($nameSpace + $limbParts[0]) ; 
        xform -worldSpace -rotation $limbBfkR[0] $limbBfkR[1] $limbBfkR[2] ($nameSpace + $limbParts[1]) ;
        xform -worldSpace -rotation $limbCfkR[0] $limbCfkR[1] $limbCfkR[2] ($nameSpace + $limbParts[2]) ; 

        $ikArmStretch = `getAttr ($nameSpace + $limbJoints[1] + ".translateX")` ;
        $ikForearmStretch = `getAttr ($nameSpace + $limbJoints[2] + ".translateX")` ;
        $ikUpDefLength = `getAttr ($nameSpace + $limbJoints[0] + ".defLength")` ;
        $ikDwDefLength = `getAttr ($nameSpace + $limbJoints[1] + ".defLength")` ;
        $ikArmStretch = $ikArmStretch / $ikUpDefLength ;
        $ikForearmStretch = $ikForearmStretch / $ikDwDefLength ;
        setAttr ($nameSpace + $limbParts[0] + ".length") $ikArmStretch ;
        setAttr ($nameSpace + $limbParts[1] + ".length") $ikForearmStretch ;
    }
    setKeyframe -t (`currentTime -q` - 1) ($nameSpace + "switch_CT." + $currLimb + "IkFkSwitch") ;
    $switch = `abs(1 - $currState)` ;
    setAttr ($nameSpace + "switch_CT." + $currLimb + "IkFkSwitch") $switch ;
    select -cl ;

def pvSwitchkIkFkmatchPose(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any controller.')
        return
    if len(args) > 1:
        om.MGlobal.displayWarning('Must be specified only one controller.')
        return

    object = args[0]
    limbAttribute = object + '.limb'

    isLimb = objExists(limbAttribute)

    if not isLimb:
        om.MGlobal.displayWarning('Must be specified part of any limb.')
        return 

    limbNamespace = ''
    limbNamespaces = object.split(':')
    if len(limbNamespaces) > 1:
        for ln in limbNamespaces[:-1]:
            limbNamespace = ln + ':'

    currLimb = mc.getAttr(limbAttribute)

    if currLimb == 'l_arm':
        pvSwitchLimbIkFk(limbLarm, jointsLarmIk, currLimb, matchLarm, limbNamespace)
    elif ($currLimb == "r_arm")
        pvSwitchLimbIkFk ($limbRarm, $jointsRarmIk, $currLimb, $matchRarm, $nameSpace) ;
    elif ($currLimb == "l_leg")
        pvSwitchLimbIkFk ($limbLleg, $jointsLlegIk, $currLimb, $matchLleg, $nameSpace) ;
    elif ($currLimb == "r_leg")
        pvSwitchLimbIkFk ($limbRleg, $jointsRlegIk, $currLimb, $matchRleg, $nameSpace) 
    else:
        om.MGlobal.displayWarning('Unknown limb: ' + currLimb)
        return 

# pvSwitchIkFkMatchPose()