from CharacterNames import CharacterNames as chn

def pvSetRotationOrder():
    nameSpace = 'dasha:'
    def setOrder(contr, rOrd):
        rotOrdVal = {"xyz":0, "yzx":1, "zxy":2, "xzy":3, "yxz":4, "zyx":5}
        if cmds.objExists(nameSpace + contr): cmds.setAttr( nameSpace + contr + '.rotateOrder', rotOrdVal[rOrd] )

    setOrder (chn('').general[1],       "zxy")            # general_CT                 
    setOrder (chn('').general[2],       "zxy")            # pivotOffset_CT
    setOrder (chn('').body[0],          "zxy")            # body_CT
    setOrder (chn('').body[1],          "zxy")            # hips_CT 
    setOrder (chn('').body[2],          "zxy")            # dw_waist_CT
    setOrder (chn('').body[3],          "zxy")            # up_waist_CT  
    setOrder (chn('').body[4],          "zxy")            # torso_CT 
    setOrder (chn('').body[5],          "zxy")            # shoulders_CT
    setOrder (chn('').neck[0],          "zxy")            # neck_CT
    setOrder (chn('').head[0],          "zxy")            # head_CT
    
    for side in ('l_', 'r_'):
        setOrder (side+chn('').getArm()[1],       "yxz")            # handIk_CT                   
        setOrder (side+chn('').getArm()[2],       "xzy")            # upArm_CT
        setOrder (side+chn('').getArm()[3],       "xyz")            # foreArm_CT
        setOrder (side+chn('').getArm()[4],       "yzx")            # hand_CT
        
        setOrder (side+chn('').getLeg()[1],       "zxy")            # footIk_CT                     
        setOrder (side+chn('').getLeg()[2],       "xyz")            # upLeg_CT
        setOrder (side+chn('').getLeg()[3],       "xyz")            # knee_CT
        setOrder (side+chn('').getLeg()[4],       "zxy")            # foot_CT
        
        [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[1]] # thumb_CT   
        [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[2]] # index_CT
        [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[3]] # middle_CT
        [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[4]] # ring_CT
        [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[5]] # pinky_CT

pvSetRotationOrder()