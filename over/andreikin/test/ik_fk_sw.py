 
from CharacterNames import CharacterNames as chn


def switchLimbIkFk():  #procedure detects the presence of selected controllers , the presence of the attribute and its value, and  namespace, after whill start switching procedure
    sel = cmds.ls(sl=True )
    if len(sel):
        for each in sel : 
            if cmds.objExists (each+'.limb'):  
                nameSpace = ':'.join(  each.split(':')[:-1]  )+':'     if  len( each.split(':')[:-1] )        else   ""
            currLimb = cmds.getAttr(each+".limb")
    currState = cmds.getAttr (nameSpace + "switch_CT." + currLimb + "IkFkSwitch")
    side      = currLimb[:2]
    ctrl      = chn().getArm(side)   if 'arm' in currLimb else     chn().getLeg(side)
    matches   =  [side +chn(ct).divideName()[1]+chn().suffixes[9] for ct in  ctrl  ]  
    if 'arm' in currLimb: 
        ikJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Ik_jnt' for x in  chn().getArmJnt(side)]  #define ik jnt names 
        fkJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Fk_jnt' for x in  chn().getArmJnt(side)]  #define fk jnt names    
    else: 
        ikJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Ik_jnt' for x in  chn().getLegJnt(side)]  #define ik jnt names  
        fkJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Fk_jnt' for x in  chn().getLegJnt(side)]  #define fk jnt names  
    if currState < 0.5:
        ikHandMatchTr = cmds.xform (nameSpace + matches[1], q=True, ws=True, t=True)        #get ct pos from matche obj
        ikHandMatchRt1 = cmds.xform (nameSpace + matches[1], q=True, ws=True, rotation=True)
        ikElbowMatchTr = cmds.xform (nameSpace + matches[0], q=True, ws=True, t=True)
        cmds.xform (nameSpace + ctrl[1],  ws=True, t=ikHandMatchTr)            # set t pos
        cmds.xform (nameSpace + ctrl[1],  ws=True, rotation=ikHandMatchRt1)
        cmds.xform (nameSpace + ctrl[0],  ws=True, t=ikElbowMatchTr)

        for i in range(20):
            for i, lenAttr in enumerate([".upLength",  ".dwLength"]):     # ik solver algoritm
                currentLen = cmds.getAttr(nameSpace+ctrl[1] + lenAttr ) 
                k = cmds.getAttr (nameSpace + fkJnt[i+2] + ".tx")/cmds.getAttr (nameSpace + ikJnt[i+2] + ".tx")
                cmds.setAttr(nameSpace + ctrl[1] + lenAttr, currentLen*k) 
        #cmds.setAttr (nameSpace + "switch_CT." + currLimb + "IkFkSwitch", 1)

        
        if cmds.objExists (nameSpace +ctrl[5]): shoulderRt = cmds.xform (nameSpace +ctrl[5], q=True, ws=True, rotation=True)
        cmds.setAttr (nameSpace + "switch_CT." + currLimb + "IkFkSwitch", 1)
        if cmds.objExists (nameSpace +ctrl[5]): cmds.xform (nameSpace +ctrl[5],  ws=True, rotation=shoulderRt)
          
    else:
        fkUpArmMatchRt1 = cmds.xform (nameSpace + matches[2], q=True, ws=True, rotation=True)
        fkForeArmMatchRt1 = cmds.xform (nameSpace + matches[3], q=True, ws=True, rotation=True)
        fkHandMatchRt1 = cmds.xform (nameSpace + matches[4], q=True, ws=True, rotation=True) 
        cmds.xform (nameSpace + ctrl[2],  ws=True, rotation=fkUpArmMatchRt1) 
        cmds.xform (nameSpace + ctrl[3],  ws=True, rotation=fkForeArmMatchRt1) 
        cmds.xform (nameSpace + ctrl[4],  ws=True, rotation=fkHandMatchRt1) 

        for i, ct in enumerate(ctrl[2:4]):                     # fk solver algoritm
            currentLen = cmds.getAttr(nameSpace + ct + ".length" ) 
            k = cmds.getAttr (nameSpace + fkJnt[i+2] + ".tx")/cmds.getAttr (nameSpace + ikJnt[i+2] + ".tx")
            cmds.setAttr(nameSpace + ct + ".length", currentLen/k) 

        #cmds.setAttr (nameSpace + "switch_CT." + currLimb + "IkFkSwitch", 0)
        
        if cmds.objExists (nameSpace +ctrl[5]): shoulderRt = cmds.xform (nameSpace +ctrl[5], q=True, ws=True, rotation=True)
        cmds.setAttr (nameSpace + "switch_CT." + currLimb + "IkFkSwitch", 0)
        if cmds.objExists (nameSpace +ctrl[5]): cmds.xform (nameSpace +ctrl[5],  ws=True, rotation=shoulderRt)
        
    cmds.select (cl=True) 
    
switchLimbIkFk()
























