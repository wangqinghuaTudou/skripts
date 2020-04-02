
#new -  add shoulder skin jnt for shoulder stretching

import maya.cmds as cmds 
#from An_Controllers import An_Controllers  as ctrl 
from An_Skeleton import An_Skeleton  as An_Skeleton 
from CharacterNames import CharacterNames as chn
from  anProcedures import  *
from  an_soft2JntIK import  *
from An_Space import An_Space as An_Space
from an_classControllers import AnControllers as ctrl 

def an_04_limbRig(action = 'rig', limb=''):    #'delRig', 'option' 
    
    if action =='rig':          ######### if rig mod  
        limbRig(limb)
    
    elif action =='option':     ######### if option mod: 
        win = "armRigOptionWin"
        if  cmds.window (win, exists=True ): cmds.deleteUI (win)
        cmds.window (win, t="Limb Rig Option", width=420,  height=40, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ( adjustableColumn=True)
        cmds.canvas( height=10 )
        cmds.checkBoxGrp( 'AutoSysCHBG' ,  numberOfCheckBoxes=1, label='Auto systym:  ', v1=True)
        cmds.checkBoxGrp( 'SoftCHBG' ,  numberOfCheckBoxes=1, label='Soft ik systym:  ', v1=True)
        cmds.columnLayout ('bridgLayout', adjustableColumn=True)
        cmds.showWindow()
    elif action =='delRig':     ######### if delete mod:                                                                         
        delLimbRig(limb)

############################################################################ del
#an_04_limbRig(action = 'delRig', limb='')

def delLimbRig(limb=''):
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0]  
    info = getInfo(limb)

    cmds.parent (info['reversJnt'][0], 'skeleton_grp') 
    an_delSys( info['grp'][1])
    an_delSys( info['grp'][0])

 
############################################################################  info

def getInfo(limb): 
   
    info = {'side':chn(limb).divideName()[0], }   #get side  
    info['pfx'] =  info['side']+'arm' if 'Arm' in chn(limb).divideName()[1] else info['side']+'leg'    #get arm or leg    
                 #if arm                                                                            #if leg
    info['rootJnt'] = An_Skeleton().torsoJnt        if 'arm' in info['pfx'] else          An_Skeleton().hipsJnt 
    info['ct']= chn().getArm(info['side'])          if 'arm' in info['pfx'] else          chn().getLeg(info['side']) 
    info['limbAttr'] = info['side']+'arm'           if 'arm' in info['pfx'] else          info['side']+'leg' 
    
    if 'arm' in info['pfx']: #if arm  
        jnt = [An_Skeleton().shoulderJnt, An_Skeleton().upArmJnt, An_Skeleton().foreArmJnt, An_Skeleton().handJnt]  
        info['reversJnt'] = [info['side']+chn(x).divideName()[1]+chn(x).divideName()[2] for x in An_Skeleton().armRevers]
        info['grp'] = [info['side']+x for x in  ['armRig_grp', 'fkArmRig_grp', 'ikArmRig_grp']]
    else:                    #if leg
        jnt = [An_Skeleton().hipJnt, An_Skeleton().upLegJnt, An_Skeleton().lowLegJnt,  An_Skeleton().footJnt,  An_Skeleton().toeJnt[0], An_Skeleton().toeJnt[1]]
        info['reversJnt'] = [info['side']+chn(x).divideName()[1]+chn(x).divideName()[2] for x in An_Skeleton().legRevers]
        info['grp'] = [info['side']+x for x in  ['legRig_grp', 'fkLegRig_grp', 'ikLegRig_grp']]
    
    info['jnt']= [info['side']+chn(x).divideName()[1]+chn(x).divideName()[2] for x in jnt]
    info['generalCt']= chn().general 
    info["color"] = ('left' if info['side']=='l_' else 'right')
    return info

############################################################################  Limb rig

def an_shoulderRig (info): 
    
    pos=cmds.xform(info['jnt'][0], q=True, worldSpace=True, t=True )  # ofset rotation pivot for rotation mod
    cmds.xform (info['ct'][5], ws=True, piv=pos)
    ikSysManualHandle=cmds.ikHandle (n=info['pfx']+"ManualShoulder_ik", sol='ikSCsolver', shf=0, sj=info['ikJnt'][0], ee=info['ikJnt'][1])             
    cmds.parent (ikSysManualHandle[0], info['ct'][5])# parent ik handle to controller 
    ctrl(info ['ct'][5]).hideAttr(['sx', 'sy', 'sz','v']) 
    an_connectRigVis (info['grp'][0], [ikSysManualHandle[0],])

    
def limbRig(limb=''):
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0]  
    info = getInfo(limb)
    
    cmds.setAttr (info['jnt'][2]+".preferredAngleZ", 80)   #  set preferred Angle
    
    for grp  in info['grp']:  cmds.group ( n=grp, em=True) ################### create rig grp
    cmds.parent ( info['grp'][1], info['grp'][2], info['grp'][0])
    cmds.parent (info['grp'][0], info['generalCt'][2])
    
    ctArm =  chn().getArm(info['side'])     
    ctLeg =  chn().getLeg(info['side'])
                                                                   ################### create and place controllers
    ctData =   { 
                ctArm[0]:{'type':'sphere', 'sz':1, 'pos':info['jnt'][1], 'posType':'pVector', 'ori':[0, 90, 90],}, #elbowIk_CT
                ctArm[1]:{'type':'handIk', 'sz':2, 'pos':info['jnt'][3], 'posType':'parent', 'ori':[0, 180, 90],}, #handIk_CT
                ctArm[2]:{'type':'fk', 'sz':2,     'pos':info['jnt'][1], 'posType':'parent', 'ori':[0, 90, 90],},#upArm_CT
                ctArm[3]:{'type':'fk', 'sz':2,     'pos':info['jnt'][2], 'posType':'parent', 'ori':[0, 90, 90],}, #foreArm_CT
                ctArm[4]:{'type':'fk', 'sz':2,     'pos':info['jnt'][3], 'posType':'parent', 'ori':[0, 90, 90],}, #hand_CT
                ctArm[5]:{'type':'shoulder', 'sz':2,'pos':info['jnt'][1], 'posType':'point', 'ori':[0, 90, 90],}, #shoulder_CT
                
                ctLeg[0]:{'type':'sphere', 'sz':1, 'pos':info['jnt'][1], 'posType':'pVector', 'ori':[0, 90, 90],},# kneeIk_CT
                ctLeg[1]:{'type':'legIk',  'sz':4, 'pos':info['jnt'][3], 'posType':'point', 'ori':[0, 0, 0],}, # l_footIk_CT
                ctLeg[2]:{'type':'fk', 'sz':2,     'pos':info['jnt'][1], 'posType':'parent', 'ori':[0, 90, 90],}, # l_upLeg_CT
                ctLeg[3]:{'type':'fk', 'sz':2,     'pos':info['jnt'][2], 'posType':'parent', 'ori':[0, 90, 90],}, # l_knee_CT 
                ctLeg[4]:{'type':'fk', 'sz':2,     'pos':info['jnt'][3], 'posType':'parent', 'ori':[0, 90, 90],}, # l_foot_CT
                ctLeg[5]:{'type':'shoulder', 'sz':2,'pos':info['jnt'][1], 'posType':'point', 'ori':[0, 0, 0],}, # hip_CT
                }

    polVecIkObj, limbIkObj, upFkObj, midFkObj, EndObj, shoulderObj = [ctrl(x)for x in  info['ct']] # criate  ct objects

    for ctObj in [polVecIkObj, limbIkObj, upFkObj, midFkObj, EndObj, shoulderObj]: 
        ctObj.makeController( ctData[ctObj.name]["type"], ctData[ctObj.name]["sz"]*cmds.floatSliderGrp('ISG_gScale', q=True, v= True ) ) # make Controller
        ctObj.rotateCt(ctData[ctObj.name]["ori"]) 
        #ctObj.gropeCT()
        addLimbAttr (ctObj.name, info['limbAttr'])
        
        if ctObj.name == shoulderObj.name and info['side']=='r_': cmds.setAttr (ctObj.oriGrp+'.rx', 180)
          
        ctObj.placeCT (ctData[ctObj.name]["pos"] , ctData[ctObj.name]["posType"])
        ctObj.addColor ( info['generalCt'][0], info['color'])
            
    for ctObj in ([shoulderObj.oriGrp, info['grp'][0] ],  [limbIkObj.oriGrp, info['grp'][2] ]):   cmds.parent ( ctObj) #place ct in grp
           
    for each in [polVecIkObj, limbIkObj]:  cmds.connectAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch", each.oriGrp+'.v') # connect vis attr for all controllers
    revers = an_connectReversAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch", upFkObj.oriGrp +'.v' ) 

    info ['obj']= [polVecIkObj, limbIkObj, upFkObj, midFkObj, EndObj, shoulderObj] 

    aSys = True   if 'arm' in info['pfx'] else  False  # auto shoulder sys 
    if cmds.window ("armRigOptionWin", exists=True ):   aSys = cmds.checkBoxGrp( 'AutoSysCHBG' , q=True, v1=True) 

    reversLimb(info)  # criate  revers system
    addLengthAttr (info)
    info['fkJnt'] = fkLimb(info) # criate  Fk rig
    info['ikJnt'] = ikLimb(info) # criate  Ik rig
    
    if aSys: an_autoShoulderRig (info)
    else:    an_shoulderRig (info)
    if  'leg' in info['pfx'] and not aSys :
        cmds.delete (shoulderObj.oriGrp)    
    
    armIkFkMix(info)
    spaceRig(info)
   

    info['ct'].pop()
    info['match'] = matchObjects(info)    
        
    cmds.pointConstraint (info['ikJnt'][1], info['obj'][2].oriGrp)  # connect fk arm controllers  
    an_connectRigVis (info['grp'][0], [info ['reversJnt'][0] ,  info ['pfx']+'IkJnt_grp',  info ['fkJnt'][0]])
    
 
    # joint to correct shoulder skinning
    endJnt=cmds.duplicate( info['jnt'][1], n=info['jnt'][0].replace( '_bind','')+'End_jnt', rc=True)[0]
    cmds.delete(cmds.listRelatives(endJnt, c=True))
    ofs = round(an_distans(info['jnt'][0], info['jnt'][1])/20, 3)
    vPMA = cmds.createNode ('plusMinusAverage', n = info['jnt'][0].replace( '_bind','')+'Ofs_PMA')
    cmds.connectAttr (info['jnt'][1]+'.tx', vPMA+'.input1D[0]', force=True )
    cmds.setAttr(vPMA+'.input1D[1]', ofs)
    cmds.connectAttr ( vPMA+'.output1D', endJnt+'.tx' , force=True )
    if info['side'] == 'l_': cmds.setAttr(vPMA+'.operation', 2)
      

    an_delSys( info['grp'][0], [info['grp'][1], info['grp'][2], revers, limbIkObj.oriGrp, endJnt, vPMA])
    for ct in [shoulderObj, limbIkObj]:   # correct semetry of rigth controllers
        if info['side']=='r_':
            oppozitCt = 'l_'+''.join(chn(ct.name).divideName()[1:])
            if cmds.objExists(oppozitCt) :
                ctrl(oppozitCt).mirrorShape(ct.name)
                
    for attr in ['reversJnt', 'jnt', 'fkJnt', 'ikJnt', 'ct', 'match']:
        an_madeInfoConnection (info['grp'][0], {attr: info[attr]}) 
    cmds.connectAttr (info['generalCt'][0]+'.'+info['pfx']+'Ctrls', info['grp'][0]+'.v')
    return info 

#info = limbRig(limb='')

############################################################################ revers Limb 
  
def reversLimb(info): 
    JntGrp = cmds.group (info ['reversJnt'][0], n=info ['pfx']+'ReversJnt_grp' ) #group revers joints
    if 'arm' in info['pfx']:               ####if arm revers 
    
        cmds.delete(cmds.parentConstraint(info['jnt'][3], info['reversJnt'][3])) #correct orientation of end revers joint
        ctrl(info ['ct'][1]).addDevideAttr() #add attributes
        for attr in ["bend","side"]:
            cmds.addAttr  (info ['ct'][1],  ln=attr,  keyable=True)
        cmds.connectAttr(info ['ct'][1]+'.bend', info ['reversJnt'][2]+'.rz' ) #connect to joint
        cmds.setDrivenKeyframe(info ['reversJnt'][0]+'.rz', cd=info['ct'][1]+'.side', dv=0, v=0 , itt='linear', ott='linear'  )   
        cmds.setDrivenKeyframe(info ['reversJnt'][0]+'.rz', cd=info['ct'][1]+'.side', dv=180, v=180 , itt='linear', ott='linear'  )
        cmds.setDrivenKeyframe(info ['reversJnt'][1]+'.rz', cd=info['ct'][1]+'.side', dv=0, v=0 , itt='linear', ott='linear'  )
        cmds.setDrivenKeyframe(info ['reversJnt'][1]+'.rz', cd=info['ct'][1]+'.side', dv=-180, v=180 , itt='linear', ott='linear'  )
        
    else:          #### else leg revers 

        ctrl(info ['ct'][1]).addDevideAttr() #add attributes
        for attr in ["footRoll", "footBreak", "ballRise", "toeRise", "heelRise", "toeTwist", "ballTwist", "heelTwist", "ballLean", "side", "clenchFoot", "FingersBend"]:
            cmds.addAttr  (info ['ct'][1],  ln=attr,  keyable=True)  
        if True:  #if not create nod
            vClamp1 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp01')   # l_legRevers6_jnt
            cmds.connectAttr ( info ['ct'][1]+'.footBreak ',  vClamp1+'.maxR')
            cmds.connectAttr ( info ['ct'][1]+'.footRoll ',  vClamp1+'.inputR')
            vClamp2 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp02')
            cmds.setAttr (  vClamp2+'.maxR', 360)
            cmds.connectAttr ( vClamp1+'.outputR ',  vClamp2+'.inputR')  
            vPMA1 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA1')
            cmds.connectAttr ( info ['ct'][1]+'.ballRise ',  vPMA1+'.input1D[0]')
            cmds.connectAttr ( vClamp2+'.outputR ',  vPMA1+'.input1D[1]')  
            cmds.connectAttr ( vPMA1+'.output1D ',  info ['reversJnt'][5]+'.rz', f= True) 
            
            vPMA2 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA2') # l_legRevers5_jnt
            cmds.setAttr (  vPMA2+'.operation', 2)
            cmds.connectAttr ( info ['ct'][1]+'.footRoll ',  vPMA2+'.input1D[0]')
            cmds.connectAttr ( info ['ct'][1]+'.footBreak ',  vPMA2+'.input1D[1]')
            vClamp3 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp03')
            cmds.setAttr (  vClamp3+'.maxR', 90)
            cmds.connectAttr ( vPMA2+'.output1D ',  vClamp3+'.inputR') 
            vPMA3 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA3') 
            cmds.connectAttr ( vClamp3+'.outputR',  vPMA3+'.input1D[0]')  
            cmds.connectAttr ( info ['ct'][1]+'.toeRise ',  vPMA3+'.input1D[1]') 
            cmds.connectAttr ( vPMA3+'.output1D ',  info ['reversJnt'][4]+'.rz', f= True) 
            cmds.connectAttr ( info ['ct'][1]+'.toeTwist ',  info ['reversJnt'][4]+'.ry', f= True) 
            cmds.connectAttr ( info ['ct'][1]+'.ballTwist ',  info ['reversJnt'][3]+'.ry', f= True) # l_legRevers4_jnt 
                
            v_MDV1 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV1')   # l_legRevers3_jnt
            cmds.connectAttr ( info ['ct'][1]+'.footRoll ',  v_MDV1+'.input1X')
            cmds.setAttr (  v_MDV1+'.input2X', -1)
            vClamp4 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp04') 
            cmds.connectAttr ( v_MDV1+'.outputX', vClamp4+'.inputR'    ) 
            cmds.setAttr (  vClamp4+'.maxR', 360)
            vPMA4 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA4') 
            cmds.connectAttr ( vClamp4+'.outputR',  vPMA4+'.input1D[0]')
            cmds.connectAttr ( info ['ct'][1]+'.heelRise ',  vPMA4+'.input1D[1]')
            cmds.connectAttr ( vPMA4 +'.output1D ',  info ['reversJnt'][2]+'.rz', f= True)
            cmds.connectAttr ( info ['ct'][1]+'.heelTwist ',  info ['reversJnt'][2]+'.ry', f= True)      
            
            vClamp5 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp05') # l_legRevers1_jnt
            cmds.connectAttr ( info ['ct'][1]+'.side ', vClamp5+'.inputR'    ) 
            cmds.setAttr (  vClamp5+'.minR', -360)
            v_MDV2 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV2')   
            cmds.connectAttr ( vClamp5+'.outputR',  v_MDV2+'.input1X')
            cmds.setAttr (  v_MDV2+'.input2X', -1)
            cmds.connectAttr ( v_MDV2+'.outputX', info ['reversJnt'][0]+'.rz', f= True)
            
            vClamp6 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp06') # l_legRevers2_jnt
            cmds.connectAttr ( info ['ct'][1]+'.side ', vClamp6+'.inputR'    ) 
            cmds.setAttr (  vClamp6+'.maxR', 360)
            cmds.connectAttr (  vClamp6+'.outputR', info ['reversJnt'][1]+'.rz', f= True)    
                
            cmds.connectAttr ( info ['ct'][1]+'.ballLean', info ['reversJnt'][5]+'.ry', f= True)
            an_delSys( info['grp'][0], [vClamp1, vClamp2, vPMA1, vPMA2, vClamp3, vPMA3, v_MDV1, vClamp4, vPMA4, vClamp5, v_MDV2, vClamp6])   
    
    #for arn and leg
    cmds.parent (JntGrp,  info['grp'][2]) #place rig in corresponding group 
    
    ctrl(info ['ct'][1]).hideAttr(['sx', 'sy', 'sz', 'v']) #hide attr
    cmds.parentConstraint (info['ct'][1], JntGrp, mo=True)    

############################################################################  fk Rig

def fkLimb(info): 
    fkJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Fk_jnt' for x in  info['jnt']]  #define fk jnt names
    copy = cmds.duplicate(info['jnt'][0], rc=True) 
                                                 #duplicate , del fingers and rename 
    child = cmds.listRelatives (copy[len(fkJnt)-1], c=True) #get fingers if need
    if child: cmds.delete (child) 
    for names in zip(copy, fkJnt ): cmds.rename (names[0], names[1])

    for i in [1, 2, 3]: cmds.parentConstraint (info['ct'][i+1], fkJnt[i]) # connect joint to controller
    for i in [4, 3]: cmds.parent (info['ct'][i].replace('_CT', '_ori'),  info['ct'][i-1])# bild Fk hierarhy
    for i in [2, 3]:                                                                        #set length setup
        cmds.addAttr  (info ['ct'][i],  ln='length',  keyable=True, dv=1, min=0, max=5)
        mdv = cmds.createNode ("multiplyDivide", n= info['ct'][i].replace('_CT', 'Length_mdv'))
        cmds.setAttr (mdv+'.input2X', cmds.getAttr (fkJnt[i]+'.tx'))
        cmds.connectAttr (info ['ct'][i]+".length", mdv+".input1X")
        cmds.connectAttr (  mdv+".outputX", info['ct'][i+1].replace('_CT', '_ori')+'.tx')   

    cmds.connectAttr(info ['generalCt'][0]+"."+info['pfx']+"Ctrls", info ['ct'][2]+'.v') # connect vis attr  
    
    for i in [2, 4]: ctrl(info ['ct'][i]).hideAttr(['tx', 'ty', 'tz',  'sx', 'sy', 'sz','v']) #hide attr
    ctrl(info ['ct'][3]).hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'sx', 'sy', 'sz','v']) 
    
    JntGrp = cmds.group (fkJnt[0], n=info ['pfx']+'FkJnt_grp')
    cmds.parentConstraint (info['jnt'][0], JntGrp, mo=True) 
    cmds.parent (JntGrp, info['ct'][2].replace('_CT', '_ori'), info['grp'][1]) 
    
    if 'leg' in info['pfx']:
        cmds.addAttr  (info ['ct'][4], ln="FingersBend", dv=0, keyable=True )
        cmds.connectAttr    (info ['ct'][4]+".FingersBend", fkJnt[4]+".rz")
    return fkJnt

############################################################################  ik Rig 

def ikLimb(info):
    ikJnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+'Ik_jnt' for x in  info['jnt']]  #define fk jnt names
    copy = cmds.duplicate(info['jnt'][0], rc=True) 
                                                 #duplicate , del fingers and rename 
    child = cmds.listRelatives (copy[len(ikJnt)-1], c=True) #get fingers if need
    if child: cmds.delete (child) 
    for names in zip(copy, ikJnt ): cmds.rename (names[0], names[1])   
    
    ikJntGrp = cmds.group (ikJnt[0],  n=info ['pfx']+'IkJnt_grp') #group of joints	
    cmds.parentConstraint ( info['rootJnt'],  ikJntGrp, mo=True)


    softSys = cmds.checkBoxGrp( 'SoftCHBG' , q=True, v1=True)     if cmds.window ("armRigOptionWin", exists=True )     else       True 
    if softSys : mineIk = an_soft2JntIK ( ikJnt[1], info['ct'][0] )        ####  stretch mine ik   
    else: mineIk =  an_2JntIK ( ikJnt[1], info['ct'][0] )    #####

    for ct in [info ['ct'][0] , info ['ct'][1]]:  ctrl(ct).addDevideAttr()  #add devide attr
    cmds.addAttr (info ['ct'][0],  ln="lock", dv=0, min=0, max=1, keyable=True ) #add attr
    cmds.connectAttr(info['ct'][0]+".lock" , mineIk[0]+'.lock') # connect lock attr
    
    for each in (['stretching', 1, 0, 1],  ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3], ['softIKOff', 0, 0, 1], ['softness', 1, 1, 3],   ): #add list of attributes
        cmds.addAttr (info['ct'][1], longName=each[0], dv=each[1], min=each[2], max=each[3], keyable=True)
        cmds.connectAttr(info['ct'][1]+"."+each[0], mineIk[0]+'.'+each[0]) # connect to target ik
    
    cmds.pointConstraint (info['reversJnt'][len(info['reversJnt'])-1 ],  mineIk[0])      
    cmds.parent (mineIk[1], ikJntGrp, info['ct'][0].replace('_CT', '_ori'), info['grp'][2])   
    
    ctrl(info ['ct'][0]).hideAttr(['rx', 'ry', 'rz',  'sx', 'sy', 'sz', 'v'])
    
    an_connectRigVis (info['grp'][0], [mineIk[0],  ])

    if 'arm' in info['pfx']:  
        cmds.orientConstraint (info['reversJnt'][3],  ikJnt[3]) 

    else :  #########  leg toe rigging
        toeIKGrp = cmds.group (em=True, n = info['pfx']+"Toe_grp") 
        toeOfsetIKGrp = cmds.group (toeIKGrp,  n = info['pfx']+"ToeOffset_grp") 
        cmds.delete( cmds.parentConstraint ( info['reversJnt'][5], toeOfsetIKGrp ))
        
        ikHandleA= cmds.ikHandle (n= info['pfx']+"ToeA_ik", sol='ikSCsolver', sj=ikJnt[3], ee=ikJnt[4], shf=False)
        ikHandleB= cmds.ikHandle (n= info['pfx']+"ToeB_ik", sol='ikSCsolver', sj=ikJnt[4], ee=ikJnt[5], shf=False)
        
        for ikHandl in (ikHandleA, ikHandleB): cmds.parent(ikHandl[0], toeIKGrp)
        cmds.connectAttr(info['ct'][1]+".FingersBend", toeIKGrp+'.rz' ) 
        cmds.connectAttr(info['ct'][1]+".clenchFoot", ikHandleA[0]+'.rx' )  
        cmds.parent (toeOfsetIKGrp, info['grp'][2]) 
        cmds.parentConstraint (info['reversJnt'][4], toeOfsetIKGrp, mo=True) 
        
        an_connectRigVis (info['grp'][0], [ikHandleA[0], ikHandleB[0]])

    hLine = an_helpLine([info['jnt'][2], info['ct'][0]], name=info['pfx']+'HelpLine')
    cmds.parent (hLine, info['grp'][2]) 
    cmds.connectAttr(info['obj'][0].oriGrp+'.v', hLine+'.v') # connect lock attr
    
    an_delSys( info['grp'][2], [mineIk[0],  mineIk[1], hLine,  ])
    
    return ikJnt

############################################################################ shoulder Rig 

def an_autoShoulderRig (info): 
    out=[]
    for  string in ('Target_jnt', 'Aim_jnt'): #//////////////////////////////// duplicate , del fingers and rename joints chains
        jnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+string for x in  info['ikJnt']]  #define  jnt names
        copy = cmds.duplicate(info['jnt'][0], rc=True)
        if 'arm' in info['pfx']: cmds.delete (cmds.listRelatives (copy[3], c=True))
        out.append(jnt)  
        for names in zip(copy, jnt ): cmds.rename (names[0], names[1])
    cmds.delete(out[1][2])
    
    if 'leg' in info['pfx']: cmds.delete(out[0][4])
    
    targetJnt, aimJnt = out[0], out[1][0:2]  
    
    cmds.parent(targetJnt[0], aimJnt[0], info ['pfx']+'IkJnt_grp')

    



    softSys = cmds.checkBoxGrp( 'SoftCHBG' , q=True, v1=True)     if cmds.window ("armRigOptionWin", exists=True )     else       True 
    if softSys : targetIk = an_soft2JntIK ( targetJnt[1], info['ct'][0] )        ####  stretch target ik     
    else:  targetIk = an_2JntIK ( targetJnt[1], info['ct'][0] )     #####
    
    
    
    
    autoSholdGrp = cmds.group (em=True, n=info ['pfx']+'AutoSys_grp') 
    
    cmds.parent (autoSholdGrp, info['grp'][2])
    
    for each in ('stretching',  'upLength', 'dwLength', 'softIKOff', 'softness' ): #
        cmds.connectAttr(info['ct'][1]+"."+each, targetIk[0]+'.'+each) # connect to target ik
    cmds.pointConstraint (info['ct'][1],  targetIk[0])
    
    #### autosholder 
    ikShldHandle=cmds.ikHandle(n=info['pfx']+"AutoSys_ik", sol='ikSCsolver', shf=0, sj=aimJnt[0], ee=aimJnt[1])#ik handl for aim joints
    cmds.orientConstraint (info['rootJnt'], ikShldHandle[0], mo=True) #orient handl 
    autoShldrCnstr = cmds.pointConstraint (  targetJnt[2], ikShldHandle[0] )[0]    #driver constraint
    auShldTargetGrp = cmds.group (n=info['pfx']+'AutoSesTarget_grp', em=True) # auto sholder point constraint target
    cmds.delete (cmds.parentConstraint (aimJnt[1], auShldTargetGrp)) #place target
    cmds.parentConstraint (info['rootJnt'], auShldTargetGrp, mo=True) #connect position
    cmds.pointConstraint (auShldTargetGrp, ikShldHandle[0]) 
        
    ikSysManualHandle=cmds.ikHandle (n=info['pfx']+"ManualShoulder_ik", sol='ikSCsolver', shf=0, sj=info['ikJnt'][0], ee=info['ikJnt'][1])         
    cmds.parent (ikSysManualHandle[0], info['ct'][5])# parent ik handle to controller 
    ctrl(info ['ct'][5]).addDevideAttr()     #add attributes 
    
    driverAttr = 'autoShoulder' if 'arm' in info['pfx'] else  'autoHip' 
    for attr in [driverAttr, 'stretching']: cmds.addAttr (info['ct'][5], longName=attr, dv=0, min=0, max=1, keyable=True)#add attr
    
    Blend = cmds.createNode ( 'blendTwoAttr', n=info['pfx']+"_auSys")   #turn off if arm Ik off
    cmds.connectAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch",     Blend+".attributesBlender")
    cmds.setAttr (Blend+".input[0]", 0)
    cmds.connectAttr(info ['ct'][5]+"."+driverAttr, Blend+".input[1]")
    
    an_connectReversAttr(Blend+".output", autoShldrCnstr+"."+auShldTargetGrp+"W1") # mix constraint weghts
    cmds.connectAttr(Blend+".output", autoShldrCnstr+"."+targetJnt[2]+"W0")
    
    cmds.parentConstraint (aimJnt[1], info['obj'][5].oriGrp, mo=True) 
     
    stratchBlend = cmds.createNode ( 'blendTwoAttr', n=info['pfx']+"_stShld")   ##############stretch shoulder stretch system
    cmds.connectAttr(info ['ct'][5]+".stretching", stratchBlend+".attributesBlender") 
    cmds.setAttr (stratchBlend+".input[0]", cmds.getAttr (targetJnt[1]+".tx"))  
    
    
    
    distPoint = cmds.createNode ( 'transform' , n=info['pfx']+"distPoint") #point for connect distans
    cmds.delete(cmds.parentConstraint (info['ct'][5], distPoint)) 

    #info['ct'][5]
   
    shoulderDistans = an_distans (distPoint, info['ikJnt'][0], act='createSys') 
 
    if cmds.getAttr (info['ikJnt'][1]+".tx")>0: cmds.connectAttr ( shoulderDistans[0],  stratchBlend+".input[1]")   
    else:
        revers = cmds.createNode ( 'multiplyDivide', n=info['pfx']+"_stShldMdv") #if left side 
        cmds.connectAttr(shoulderDistans[0], revers+".input1X")
        cmds.setAttr (revers+".input2X", -1)
        cmds.connectAttr ( revers+".outputX",  stratchBlend+".input[1]")  
    cmds.connectAttr  (stratchBlend+".output", info['ikJnt'][1]+".tx")
    
    if 'leg' in info['pfx']: print out[0][4] # cmds.delete(out[0][3])  #
    cmds.parent (targetIk[1], shoulderDistans[1], auShldTargetGrp, ikShldHandle[0], autoSholdGrp) #place objects in correct place
    

    pos=cmds.xform(info['jnt'][0], q=True, worldSpace=True, t=True )  # ofset rotation pivot for rotation mod
    cmds.xform (info['ct'][5], ws=True, piv=pos)
    cmds.parent (distPoint, info['ct'][5])
    
    an_connectRigVis (info['grp'][0], [targetIk[0], ikSysManualHandle[0], ikShldHandle[0]])
    
    ctrl(ikSysManualHandle[0]).hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz','v']) 
    ctrl(info['ct'][5]).hideAttr(['rx', 'sx', 'sy', 'sz','v'])
    an_delSys ( info['grp'][2], [targetIk[0], targetIk[1]])

  
############################################################################  ik fk  Mix Rig 

def  armIkFkMix(info):
    for drJnt in (info['fkJnt'], info['jnt']): 
        cmds.parentConstraint(info['ikJnt'][0], drJnt[0])  #clavicle
        cmds.connectAttr (info['ikJnt'][1]+".t", drJnt[1]+".t") #upArm pos 

    constr = cmds.orientConstraint(info['ikJnt'][1],  info['fkJnt'][1], info['jnt'][1]) #upArm rotate 

    cmds.connectAttr (info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['ikJnt'][1]+"W0" ) # setup Constraint value value 

    deleteList = [ an_connectReversAttr(info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['fkJnt'][1]+"W1" ), ]
    
    #an_delSys( info['grp'][1], [ an_connectReversAttr(info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['fkJnt'][1]+"W1" ), ]) 

    attrData = ([2, "r"], [2, "t"], [3, "r"], [3, "t"]) if 'arm' in info['pfx'] else ([2, "r"], [2, "t"], [3, "r"], [3, "t"], [4, "r"], [4, "t"])      
    for i, atr in attrData:
        
        objects = (info['ikJnt'][i], info['fkJnt'][i], info['jnt'][i])
        if atr == "r": 
            deleteList.append(an_mixViaConstraint (objects, type='orient', mixAttr = info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch")[2])
        if atr == "t": 
            deleteList.append(an_mixViaConstraint (objects, type='point', mixAttr = info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch")[2])
    
    an_delSys( info['grp'][1], deleteList)

############################################################################  match Rig 

def matchObjects(info):
    out = []
     # elbowIk, l_handIk, Arm, foreArm, hand
    #for ct, jnt in ( [info['ct'][0], info['fkJnt'][1]],     [info['ct'][1], info['fkJnt'][3]],     [info['ct'][2], info['ikJnt'][1]],      [info['ct'][3], info['ikJnt'][2]],    [info['ct'][4], info['ikJnt'][3]]): 
    for ct, jnt in ( [info['ct'][0], info['fkJnt'][2]],     [info['ct'][1], info['fkJnt'][3]],     [info['ct'][2], info['ikJnt'][1]],      [info['ct'][3], info['ikJnt'][2]],    [info['ct'][4], info['ikJnt'][3]]):     
        
        matchName = cmds.duplicate (ct, rr=True, rc=True, n= chn(ct).divideName()[0]+chn(ct).divideName()[1]+chn().suffixes[9])[0]
        for each in cmds.listRelatives(matchName, children=True): cmds.delete (each)
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz','v']: cmds. setAttr (matchName+'.'+attr, k=True, lock=False )
        cmds.parent (matchName, jnt)
        cmds.connectAttr ( ct+".rotateOrder", matchName+".rotateOrder")
        out.append(matchName)
    return out

############################################################################ 

def addLengthAttr (info):
    for i in xrange(1,4):
        currLength = cmds.getAttr (info['jnt'][i] + ".tx")
        if not cmds.objExists (info['jnt'][i-1]+".defLength"):
            cmds.addAttr (info['jnt'][i-1],  dv=currLength, ln="defLength")
            cmds.setAttr (info['jnt'][i-1]+".defLength",   l=True)
        else:   
            cmds.setAttr (info['jnt'][i-1]+".defLength",   l=False)
            cmds.setAttr (info['jnt'][i-1]+".defLength",   currLength)
            cmds.setAttr (info['jnt'][i-1]+".defLength",   l=True)

############################################################################ controller spase rig

def spaceRig(info):

    root_grp = 'root'
    targetList =( [ info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'], [An_Skeleton().hipsJnt, 'pelvis'], [An_Skeleton().torsoJnt, 'torso'], [An_Skeleton().headJnt[0], 'head'])   #Ik_CT space
    if 'leg' in info['pfx']: 
        targetList = ( [info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'], [An_Skeleton().hipsJnt, 'pelvis'],  [An_Skeleton().rootJnt, 'body']) 
    An_Space ( info['ct'][1],  object=info['ct'][1].replace('_CT', '_ori'), targList=targetList, spaceType = 'parent').rebildSpaceObj()

    targetList=([ info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'],  [An_Skeleton().torsoJnt, 'torso'],  )                                                           #elbow/knee  Ik_CT space
    if 'leg' in info['pfx']:    
        targetList=([ info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'],  [An_Skeleton().rootJnt, 'body'],  [info['ct'][1], 'foot'])  
    An_Space ( info['ct'][0],  object=info['ct'][0].replace('_CT', '_ori'), targList=targetList, spaceType = 'parent').rebildSpaceObj()

    targetList=([info['generalCt'][1], 'general'], [info['side']+''.join(chn(An_Skeleton().shoulderJnt).divideName()[1:]), 'shoulder'], [An_Skeleton().rootJnt, 'body'], [An_Skeleton().torsoJnt, 'torso'],)  #upArm_CT space
    if 'leg' in info['pfx']:   
        targetList = ([info['generalCt'][1], 'general'],    [An_Skeleton().hipsJnt, 'pelvis'],  [An_Skeleton().rootJnt, 'body'])
    An_Space ( info['ct'][2],  object=info['ct'][2].replace('_CT', '_ori'), targList=targetList, spaceType = 'orient').rebildSpaceObj()


 
############################################################################ 

def specialAnimCurves(info): 
    CtNams = info['ct'][1]
    Jnt	= info['jnt']
    ikJnt = info['ikJnt']
    
    cmds.addAttr (ikJnt[2], ln="K_soft", keyable=True) 
    
    
    blendNod = cmds.createNode  ("blendTwoAttr", n=chn(CtNams).divideName()[0]+chn(CtNams).divideName()[1]+"KSoft")                   
    cmds.connectAttr (blendNod+".output ",  ikJnt[2]+".K_soft") 
    cmds.connectAttr (CtNams+".softness",  blendNod+".attributesBlender")
    
    
    valList1=([0, 0, 0.00758467], [15, 0.034, 0.0022837], [30, 0.038, -0.000922274], [45, 0.028, -0.00198057], [60, 0.012, -0.00328864], [65, 0, -0.00676812]) 
    valList2=([0, 0, 0.0226763], [15, 0.097, 0.00834517 ], [30, 0.135, 0.00397887], [45, 0.147, 0], [60, 0.137 , -0.00310352], [75, 0.108, -0.00533169], [90, 0.07 , -0.00660493], [105, 0.025, -0.00891482], [110, 0, -0.0119366])
    
    for dv, v, angl in valList1:   cmds.setDrivenKeyframe (blendNod+".input[0]", cd=Jnt[2]+".rz", dv=dv, v=v)   # bild anim curves     
    for dv, v, angl in valList2:   cmds.setDrivenKeyframe (blendNod+".input[1]", cd=Jnt[2]+".rz", dv=dv, v=v)
    curves = cmds.listConnections( blendNod)
    import maya.mel as mm 
    for dv, v, angl in valList1:     mm.eval("keyTangent -e -a -f "+str(dv)+" -inAngle "+str(angl)+" -outAngle "+str(angl)+"  -inWeight 1 "+curves[2])
    for dv, v, angl in valList2:     mm.eval("keyTangent -e -a -f "+str(dv)+" -inAngle "+str(angl)+" -outAngle "+str(angl)+"  -inWeight 1 "+curves[3])   
         
############################################################################ 

def addLimbAttr (ctName, limbName):
    if not cmds.objExists (ctName+'.'+limbName):
        cmds.addAttr (ctName,  dt="string", ln="limb")
    else:
        cmds.setAttr (ctName+ ".limb", l=False ) 
    cmds.setAttr (ctName+ ".limb",  limbName,  type="string" )
    cmds.setAttr (ctName+ ".limb", l=True ) 








 