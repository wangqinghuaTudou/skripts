import maya.cmds as cmds 
from an_classSkeletonQuadro import AnSkeletonQuadro
from an_classNames import AnNames as chnm
from an_classNames import AnNamesQuadro as chnQd
from  anProcedures import  *
from  an_soft2JntIK import  *
from An_Space import An_Space as An_Space
from an_classControllers import AnControllers  as ctrl

'''
    limbQuadro()
    
__________________________________________________
    - an_04_limbQuadroRig()
    - getInfo()
    - limbQuadroRig()
    - an_autoShoulderQuadro ()
    - ikQuadroLimb()
    - fkLimb(info)
'''

######################################################################### ___________________________________  

def an_04_limbQuadroRig(action = 'rig', limb=''):  #'delRig', 'option'     
    if action =='rig':         ######### if rig mod  
        limbQuadroRig(limb)
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
        delQuadroLimbRig(limb)
############################################################################  info ___________________________________

def getInfo(limb): 
    info = {'side':chnm(limb).divideName()[0], }   #get side  
    info['pfx'] =  info['side']+'arm' if 'Arm' in chnm(limb).divideName()[1] else info['side']+'leg'    #get arm or leg    
                 #if arm                                                                            #if leg
    info['rootJnt'] = chnm().getBodyJnt()[5]       if 'arm' in info['pfx'] else          chnm().getBodyJnt()[1] 
    info['ct']= chnQd().getArm(info['side'])          if 'arm' in info['pfx'] else        chnQd().getLeg(info['side'])   
    info['limbAttr'] = info['side']+'arm'           if 'arm' in info['pfx'] else        info['side']+'leg' 
    info['prefAngle'] = -80           if 'arm' in info['pfx']  else     80   
    jnt = AnSkeletonQuadro().getJntList()[16:23]    if 'arm' in info['pfx'] else        AnSkeletonQuadro().getJntList()[2:9] 
    info['jnt']= [info['side']+chnm(x).divideName()[1]+chnm(x).divideName()[2] for x in jnt] 
    info['ikJnt']= [x for x in jnt[1:4]]    if 'arm' in info['pfx'] else  [x for x in jnt[2:5] ]   # for setting preferred Angle
    info['reversJnt']=AnSkeletonQuadro().getJntList( info['side'] )[31:39]  if 'arm' in info['pfx'] else  AnSkeletonQuadro().getJntList(info['side'])[23:31]  
    info['grp'] = [ info['pfx'] +x for x in ['Rig_grp', 'FkRig_grp', 'IkRig_grp', 'IkJnt_grp', 'IkControls_grp']]  
    info['generalCt']= chnm().general() 
    info["color"] = ('left' if info['side']=='l_' else 'right') 
    return info 


############################################################################  Limb rig ___________________________________

#info = limbQuadroRig(limb='l_Arm')

def limbQuadroRig(limb=''):   
        
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0]  
    info = getInfo(limb)
    
    
    cmds.setAttr (info['ikJnt'][1]+".preferredAngleZ", info['prefAngle'])   #  set preferred Angle
    
    
    for grp  in info['grp']:  cmds.group ( n=grp, em=True) # create rig grp
    cmds.parent ( info['grp'][1], info['grp'][2], info['grp'][0])
    cmds.parent (info['grp'][0], info['generalCt'][2])
    for i in [3,4]: cmds.parent (info['grp'][i], info['grp'][2])
    
    
    ctList =  chnQd().getArm(info['side'])    if 'arm' in info['pfx'] else     chnQd().getLeg(info['side'])
    
    polVecIkObj = ctrl(ctList[0]).makeController ( 'sphere',   size=1,     orient="Y",   pos=info['jnt'][1],    posType='pVector')
    polVecDwObj = ctrl(ctList[1]).makeController ( 'sphere',   size=1,     orient="Y",   pos=info['jnt'][3],    posType='point')
    limbIkObj =   ctrl(ctList[2]).makeController ( 'legIk',    size=3,     orient="Y",   pos=info['jnt'][4],    posType='point')
    upFkObj =     ctrl(ctList[3]).makeController ( 'fk',       size=2,     orient="X",   pos=info['jnt'][1],    posType='parent')
    midFkObj =    ctrl(ctList[4]).makeController ( 'fk',       size=2,     orient="X",   pos=info['jnt'][2],    posType='parent')
    EndObj   =    ctrl(ctList[5]).makeController ( 'fk',       size=2,     orient="X",   pos=info['jnt'][3],    posType='parent')
    addFk =       ctrl(ctList[6]).makeController ( 'fk',       size=2,     orient="X",   pos=info['jnt'][4],    posType='parent')
    shoulderObj = ctrl(ctList[7]).makeController ( 'shoulder', size=2,     orient="X",   pos=info['jnt'][1],    posType='point')
    
    info['ctObj']= [polVecIkObj, polVecDwObj, limbIkObj, upFkObj, midFkObj, EndObj,  addFk,   shoulderObj]
    for ctObj in  info['ctObj']: ctObj.addColor ( info['generalCt'][0], info['color'])
    
    for each in [polVecIkObj, limbIkObj, polVecDwObj]:  cmds.connectAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch", each.oriGrp+'.v') # connect vis attr for all controllers
    an_connectReversAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch", upFkObj.oriGrp +'.v' ) 
    
    for i in [6, 5, 4]: cmds.parent (info['ct'][i].replace('_CT', '_ori'),  info['ct'][i-1]) # bild Fk hierarhy
    
    reversLimb(info)
    
    ctrl(limbIkObj.name).addDevideAttr()
    for each in (['stretching', 1, 0, 1],  ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3], ['softIKOff', 0, 0, 1], ['softness', 1, 1, 3],   ): #add list of attributes
        cmds.addAttr (info['ct'][2], longName=each[0], dv=each[1], min=each[2], max=each[3], keyable=True)
    
    info = an_autoShoulderQuadro(info)
    info = ikQuadroLimb(info)
    info = fkLimb(info)  
    armIkFkMix(info)


    spaceRig(info)
    return info 
############################################################################  auto Shoulder Quadro ___________________________________


def an_autoShoulderQuadro (info):  

    polVecIkObj, polVecDwObj, limbIkObj, upFkObj, midFkObj, EndObj, addFk, shoulderObj = info['ctObj']
    out=[]
    for  string in ('Target_jnt', 'Aim_jnt'): # target and aim joint
        jnt = [chn(x).divideName()[0]+chn(x).divideName()[1]+string for x in  info['jnt']]     
        copy = cmds.duplicate(info['jnt'][0], rc=True)
        out.append(jnt)  
        for names in zip(copy, jnt ): cmds.rename (names[0], names[1])

        
    cmds.delete(out[1][2])
    cmds.delete(out[0][4])
    targetJnt, aimJnt = out[0][0:4] , out[1][0:2] 
    cmds.parent(targetJnt[0], aimJnt[0], info['grp'][3])
    
    ### correction auto       
    distans = an_distans( targetJnt[2], info['jnt'][4])     if info['side']=='l_'     else  an_distans( targetJnt[2], info['jnt'][4])*-1
    cmds.setAttr(targetJnt[3]+'.tx', distans )
    ##__________________________________________      
    
    autoSholdGrp = cmds.group (em=True, n=info ['pfx']+'AutoSys_grp') 
    info['grp'].append(autoSholdGrp)
    cmds.parent (autoSholdGrp, info['grp'][2])
    
    targetGrp = []
    for jntAim, rotJnt,  in zip ([aimJnt[0], info['reversJnt'][6] ],     [info['rootJnt'], info['reversJnt'][5]]  ):
        aim = 1 if info['side']=='l_' else -1
        tmp = cmds.aimConstraint( targetJnt[2], jntAim, aim= [aim, 0, 0])
        grp = cmds.group (n=chnm(jntAim).sfxMinus()+'Tg_grp', em=True)   
        targetGrp.append (grp)                    
        tmp2 = cmds.pointConstraint( cmds.listRelatives( jntAim, c=True )[0], grp)
        cmds.delete(tmp, tmp2)
        cmds.setAttr(jntAim+'.rotate', 0, 0, 0)
        cmds.parentConstraint(  rotJnt, grp, mo=True)
        cmds.parent (grp, autoSholdGrp)
    
    ikShldHandle=cmds.ikHandle(n=info['pfx']+"AutoSys_ik", sol='ikSCsolver', shf=0, sj=aimJnt[0], ee=aimJnt[1])#ik handl for aim joints
    ikShldHandleDw=cmds.ikHandle(n=info['pfx']+"AutoSysDw_ik", sol='ikSCsolver', shf=0, sj=info['reversJnt'][6], ee=info['reversJnt'][7])#ik handl for aim joints
    shConstr = an_mixedSpace([targetGrp[0], targetJnt[2]] , ikShldHandle[0], type='point', mo=False )
    ftConstr = an_mixedSpace([targetGrp[1], targetJnt[2]] , ikShldHandleDw[0], type='point', mo=False )
    cmds.parentConstraint(aimJnt[0],  shoulderObj.oriGrp, mo=True)
    cmds.parentConstraint(info['reversJnt'][6],  polVecDwObj.oriGrp, mo=True)
    cmds.orientConstraint (info['rootJnt'], ikShldHandle[0], mo=True) #orient handl
    cmds.orientConstraint (info['ct'][2], ikShldHandleDw[0], mo=True) #orient handl Dw
    
    for ct, constr in zip([polVecDwObj.name,  shoulderObj.name ], [ftConstr, shConstr] ):  #connect attr  
        cmds.addAttr (ct, longName='autoSys', dv=1, min=0, max=1, keyable=True)
        atr = cmds.pointConstraint (constr, q=True, weightAliasList=True)[1]
        #print ct+'.autoSys', constr[0]+'.'+atr
        
        if ct == polVecDwObj.name:
            cmds.connectAttr( ct+'.autoSys', constr[0]+'.'+atr )
        else: 
            Blend = cmds.createNode ( 'blendTwoAttr', n=info['pfx']+"_auSys")   #turn off if arm Ik off
            cmds.connectAttr(info ['generalCt'][0]+"."+info ['pfx']+"IkFkSwitch",     Blend+".attributesBlender")
            cmds.setAttr (Blend+".input[0]", 0)
            #cmds.setAttr (Blend+".input[1]", 1)
            cmds.connectAttr(ct+'.autoSys', Blend+".input[1]")
            cmds.connectAttr(Blend+".output", constr[0]+'.'+atr)
            
    #target ik
    softSys = cmds.checkBoxGrp( 'SoftCHBG' , q=True, v1=True)     if cmds.window ("armRigOptionWin", exists=True )     else       True 
    if softSys : targetIk = an_soft2JntIK ( targetJnt[1], info['ct'][0])        
    else:  targetIk = an_2JntIK ( targetJnt[1], info['ct'][0] )     
    for each in ('stretching',  'upLength', 'dwLength', 'softIKOff', 'softness' ): #
        cmds.connectAttr(info['ct'][2]+"."+each, targetIk[0]+'.'+each) # connect to target ik  
    
    #cmds.parentConstraint (info['reversJnt'][5],  targetIk[0], mo=True)
    
    cmds.parentConstraint (info['reversJnt'][5],  targetIk[0], mo=True)  #/////////////////////////////////////////////////////////////////////////////////////////////
    
    cmds.parent ( ikShldHandle[0], ikShldHandleDw[0], targetIk[1], autoSholdGrp)
    
    ctrl(info ['ct'][7]).hideAttr(['rx', 'ry', 'rz',  'sx', 'sy', 'sz', 'v'])
    
    an_connectRigVis (info['grp'][0], [autoSholdGrp,  ])
    
    return info


############################################################################  ik Rig  ___________________________________

def ikQuadroLimb(info):



    
    polVecIkObj, polVecDwObj, limbIkObj, upFkObj, midFkObj, EndObj, addFk, shoulderObj = info['ctObj']
    cmds.parent ( polVecIkObj.oriGrp, polVecDwObj.oriGrp, limbIkObj.oriGrp, shoulderObj.oriGrp,     info['grp'][4])
    ikJnt = [chnm(x).divideName()[0]+chnm(x).divideName()[1]+'Ik_jnt' for x in  info['jnt']]  #define ik jnt names
    copy = cmds.duplicate(info['jnt'][0], rc=True) #duplicate , del fingers and rename 
    for names in zip(copy, ikJnt ): cmds.rename (names[0], names[1])
    info['ikJnt'] = ikJnt
    
    cmds.parent (ikJnt[0],  info['grp'][3])
    cmds.parentConstraint ( info['rootJnt'],  info['grp'][3], mo=True)
    
    softSys = cmds.checkBoxGrp( 'SoftCHBG' , q=True, v1=True)     if cmds.window ("armRigOptionWin", exists=True )     else       True 
    
    if softSys : mineIk = an_soft2JntIK ( ikJnt[1], info['ct'][0] )        ####  stretch mine ik   
    else: mineIk =  an_2JntIK ( ikJnt[1], info['ct'][0] )    #####
    
    for ct in [info ['ct'][0] , info ['ct'][2]]:  ctrl(ct).addDevideAttr()  #add devide attr
    cmds.addAttr (info ['ct'][0],  ln="lock", dv=0, min=0, max=1, keyable=True ) #add attr
    cmds.connectAttr(info['ct'][0]+".lock" , mineIk[0]+'.lock') # connect lock attr
    
    for each in (['stretching', 1, 0, 1],  ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3], ['softIKOff', 0, 0, 1], ['softness', 1, 1, 3],   ): #add list of attributes
        cmds.connectAttr(info['ct'][2]+"."+each[0], mineIk[0]+'.'+each[0]) # connect to target ik
    
    cmds.pointConstraint (info['ct'][1],  mineIk[0])      
    cmds.parent (mineIk[1], info['grp'][2])   
    ctrl(info ['ct'][0]).hideAttr(['rx', 'ry', 'rz',  'sx', 'sy', 'sz', 'v'])
    ctrl(info ['ct'][1]).hideAttr(['rx', 'ry', 'rz',  'sx', 'sy', 'sz', 'v'])
    an_connectRigVis (info['grp'][0], [mineIk[0],  ])
    
    ikShldHandle=cmds.ikHandle(n=info['pfx']+"Shld_ik", sol='ikSCsolver', shf=0, sj=ikJnt[0], ee=ikJnt[1]) 
    cmds.parent (ikShldHandle[0],  info ['ct'][7])
    
    ikHandles, grpIks = [],[]
    
    for i in range (3,6):  
        ik = cmds.ikHandle(n=info['pfx']+"End0"+str(i-2) +"_ik", sol='ikSCsolver', shf=0, sj=ikJnt[i], ee=ikJnt[i+1]) 
        ikHandles.append(ik[0])
        if not i == 5:
            grpOf =cmds.group( n=info['pfx']+"Ofs0"+str(i-2) +"_ikGrp", em=True)
            grpIk =cmds.group( grpOf, n=info['pfx']+"End0"+str(i-2) +"_ikGrp")
            cmds.delete( cmds.parentConstraint (ikJnt[i+1], grpIk))
            grpIks.append(grpIk)
            cmds.parent (ik[0], grpOf)
        else:
            cmds.parent (ik[0], grpOf)
    
    cmds.connectAttr(info['ct'][2]+".FingersBend", info['pfx']+'Ofs02_ikGrp.rz')
    
    for grp, jntRev in zip([1, 0], [4, 5]):
        cmds.parentConstraint ( info['reversJnt'] [jntRev], grpIks[grp], mo=True)
    
    
    distans = an_distans( info['ct'][1], info['reversJnt'][6], act='createSys')    
    
    
    
    if info ['side'] == 'l_': cmds.connectAttr(distans[0], ikJnt[4]+'.tx')
    else : an_connectByMultiplier(distans[0], ikJnt[4]+'.tx', -1)
    
    '''
    outputAttr = ikJnt[4]+'.tx'
    
    inputAttr = distans[0]
    val =-1
    def connectByMultiplier (inputAttr, outputAttr, val ):
        unConvers = cmds.createNode ('unitConversion',  n = info['pfx']+'unitConversion01')
        cmds.setAttr (unConvers+".conversionFactor", val)
        cmds.connectAttr( input , unConvers+'.input')
        cmds.connectAttr( unConvers+'.output', outputAttr)
        return unConvers
    '''
    
    for grp in  grpIks+[distans[1],]:  
        cmds.parent ( grp, info['grp'][2])
        
    an_connectRigVis (info['grp'][0], [grpIks[0], grpIks[1], ikShldHandle[0]])
    return info

############################################################################  mix Rig


def  armIkFkMix(info):
    for drJnt in (info['fkJnt'], info['jnt']): 
        cmds.parentConstraint(info['ikJnt'][0], drJnt[0])  #clavicle
        cmds.connectAttr (info['ikJnt'][1]+".t", drJnt[1]+".t") #upArm pos 
    
    constr = cmds.orientConstraint(info['ikJnt'][1],  info['fkJnt'][1], info['jnt'][1]) #upArm rotate 
    cmds.connectAttr (info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['ikJnt'][1]+"W0" ) # setup Constraint value value 
    deleteList = [ an_connectReversAttr(info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['fkJnt'][1]+"W1" ), ]
    
    #an_delSys( info['grp'][1], [ an_connectReversAttr(info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch",  constr[0]+"."+info['fkJnt'][1]+"W1" ), ]) 
    
    attrData = ([2, "r"], [2, "t"], [3, "r"], [3, "t"], [4, "r"], [4, "t"], [5, "r"])  
    
    for i, atr in attrData:
    
        objects = (info['ikJnt'][i], info['fkJnt'][i], info['jnt'][i])
        if atr == "r": 
            deleteList.append(an_mixViaConstraint (objects, type='orient', mixAttr = info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch")[2])
        if atr == "t": 
            deleteList.append(an_mixViaConstraint (objects, type='point', mixAttr = info['generalCt'][0]+'.'+info ['pfx']+"IkFkSwitch")[2])
    
    #an_delSys( info['grp'][1], deleteList)



############################################################################  fk Limb rig

def fkLimb(info): 

    cmds.parent ( info['ctObj'][3].oriGrp, info['grp'][1])
    #cmds.pointConstraint( info['ikJnt'][1],  info['ctObj'][3].oriGrp, mo=False)
    
    fkJnt = [chnm(x).divideName()[0]+chnm(x).divideName()[1]+'Fk_jnt' for x in  info['jnt']]  #define fk jnt names
    copy = cmds.duplicate(info['jnt'][0], rc=True) 
                                                 #duplicate , del fingers and rename 
    for names in zip(copy, fkJnt ): cmds.rename (names[0], names[1])
    
    for i, x in zip([1, 2, 3, 4], [3, 4, 5, 6 ]): cmds.parentConstraint (info['ct'][x], fkJnt[i]) # connect joint to controller 
    
    for i, x in zip([3, 4, 5],[2, 3, 4]):                                                                        #set length setup
        cmds.addAttr  (info ['ct'][i],  ln='length',  keyable=True, dv=1, min=0, max=5)
        mdv = cmds.createNode ("multiplyDivide", n= info['ct'][i].replace('_CT', 'Length_mdv'))
        cmds.setAttr (mdv+'.input2X', cmds.getAttr (fkJnt[x]+'.tx'))
        cmds.connectAttr (info ['ct'][i]+".length", mdv+".input1X")
        cmds.connectAttr (  mdv+".outputX", info['ct'][i+1].replace('_CT', '_ori')+'.tx')   
    
    cmds.connectAttr(info ['generalCt'][0]+"."+info['pfx']+"Ctrls", info ['ct'][3]+'.v') # connect vis attr  
    
    for i in [3, 6]: ctrl(info ['ct'][i]).hideAttr(['tx', 'ty', 'tz',  'sx', 'sy', 'sz','v']) #hide attr
    for i in [4, 5]: ctrl(info ['ct'][i]).hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'sx', 'sy', 'sz','v']) 
    
    JntGrp = cmds.group (fkJnt[0], n=info ['pfx']+'FkJnt_grp')
    cmds.parentConstraint (info['jnt'][0], JntGrp, mo=True) 
    cmds.parent (JntGrp, info['ct'][2].replace('_CT', '_ori'), info['grp'][1]) 
    
    cmds.addAttr  (info ['ct'][6], ln="FingersBend", dv=0, keyable=True )
    cmds.connectAttr    (info ['ct'][6]+".FingersBend", fkJnt[5]+".rz")
    
    info['fkJnt'] = fkJnt
    
    an_connectRigVis (info['grp'][0], [fkJnt[0],]) 
    
    return info

############################################################################  revers Rig

def reversLimb(info): 
    ct = info ['ct'][2]
    JntGrp = cmds.group (info ['reversJnt'][0], n=info ['pfx']+'ReversJnt_grp' ) #group revers joints 
    cmds.parent  (JntGrp, info['grp'][3])
    
    ctrl(ct).addDevideAttr() #add attributes 
    for attr in ["footRoll", "footBreak", "ballRise", "toeRise", "heelRise", "toeTwist", "ballTwist", "heelTwist", "ballLean", "side", "clenchFoot", "FingersBend"]:
        cmds.addAttr  (ct,  ln=attr,  keyable=True)   
    #if True:  #if not create nod
    vClamp1 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp01')   # l_legRevers6_jnt 
    cmds.connectAttr ( ct+'.footBreak ',  vClamp1+'.maxR')
    cmds.connectAttr ( ct+'.footRoll ',  vClamp1+'.inputR')
    vClamp2 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp02')
    cmds.setAttr (  vClamp2+'.maxR', 360)
    cmds.connectAttr ( vClamp1+'.outputR ',  vClamp2+'.inputR')  
    vPMA1 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA1')
    cmds.connectAttr ( ct+'.ballRise ',  vPMA1+'.input1D[0]')
    cmds.connectAttr ( vClamp2+'.outputR ',  vPMA1+'.input1D[1]')  
    cmds.connectAttr ( vPMA1+'.output1D ',  info ['reversJnt'][5]+'.rz', f= True) 
    
    vPMA2 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA2') # l_legRevers5_jnt 
    cmds.setAttr (  vPMA2+'.operation', 2)
    cmds.connectAttr ( ct+'.footRoll ',  vPMA2+'.input1D[0]')
    cmds.connectAttr ( ct+'.footBreak ',  vPMA2+'.input1D[1]')
    vClamp3 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp03')
    cmds.setAttr (  vClamp3+'.maxR', 90)
    cmds.connectAttr ( vPMA2+'.output1D ',  vClamp3+'.inputR') 
    vPMA3 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA3') 
    cmds.connectAttr ( vClamp3+'.outputR',  vPMA3+'.input1D[0]')  
    cmds.connectAttr ( ct+'.toeRise ',  vPMA3+'.input1D[1]') 
    cmds.connectAttr ( vPMA3+'.output1D ',  info ['reversJnt'][4]+'.rz', f= True) 
    cmds.connectAttr ( ct+'.toeTwist ',  info ['reversJnt'][4]+'.ry', f= True) 
    cmds.connectAttr ( ct+'.ballTwist ',  info ['reversJnt'][3]+'.ry', f= True) # l_legRevers4_jnt 
    
    v_MDV1 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV1')   # l_legRevers3_jnt 
    cmds.connectAttr ( ct+'.footRoll ',  v_MDV1+'.input1X')
    cmds.setAttr (  v_MDV1+'.input2X', -1)
    vClamp4 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp04') 
    cmds.connectAttr ( v_MDV1+'.outputX', vClamp4+'.inputR'    ) 
    cmds.setAttr (  vClamp4+'.maxR', 360)
    vPMA4 = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA4') 
    cmds.connectAttr ( vClamp4+'.outputR',  vPMA4+'.input1D[0]')
    cmds.connectAttr ( ct+'.heelRise ',  vPMA4+'.input1D[1]')
    cmds.connectAttr ( vPMA4 +'.output1D ',  info ['reversJnt'][2]+'.rz', f= True)
    cmds.connectAttr ( ct+'.heelTwist ',  info ['reversJnt'][2]+'.ry', f= True)      
    
    vClamp5 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp05') # l_legRevers1_jnt
    cmds.connectAttr ( ct+'.side ', vClamp5+'.inputR'    ) 
    cmds.setAttr (  vClamp5+'.minR', -360)
    v_MDV2 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV2')   
    cmds.connectAttr ( vClamp5+'.outputR',  v_MDV2+'.input1X')
    cmds.setAttr (  v_MDV2+'.input2X', -1)
    cmds.connectAttr ( v_MDV2+'.outputX', info ['reversJnt'][0]+'.rz', f= True)
    
    vClamp6 = cmds.createNode ('clamp',  n = info['pfx']+'Clamp06') # l_legRevers2_jnt
    cmds.connectAttr ( ct+'.side ', vClamp6+'.inputR'    ) 
    cmds.setAttr (  vClamp6+'.maxR', 360)
    cmds.connectAttr (  vClamp6+'.outputR', info ['reversJnt'][1]+'.rz', f= True)    
    
    cmds.connectAttr ( ct+'.ballLean', info ['reversJnt'][5]+'.ry', f= True)
    an_delSys( info['grp'][0], [vClamp1, vClamp2, vPMA1, vPMA2, vClamp3, vPMA3, v_MDV1, vClamp4, vPMA4, vClamp5, v_MDV2, vClamp6])   
    
    #for arn and leg
    ctrl(ct).hideAttr(['sx', 'sy', 'sz', 'v']) #hide attr
    cmds.parentConstraint (info['ct'][2], JntGrp, mo=True)
    
    #an_connectRigVis (info['grp'][0], [info ['reversJnt'][0] , JntGrp ]) ###################################################################_______________________________
    
    an_connectRigVis (info['grp'][0], [info['grp'][3], ]) 
       
    info['reversGrp'] = JntGrp  
    return info

############################################################################  Space rig ___________________________________

def spaceRig(info):
     
    root_grp = 'root'
    pelvis = AnSkeletonQuadro().getJntList()[1]
    torso = AnSkeletonQuadro().getJntList()[12]
    head = AnSkeletonQuadro().getJntList()[14]
    
    
    shoulder= AnSkeletonQuadro().getJntList(info ['side'])[16]         if 'arm' in info['pfx'] else      AnSkeletonQuadro().getJntList(info ['side'])[2]    
    
    
    
    targetList =( [ info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'], [pelvis, 'pelvis'], [torso, 'torso'], [head, 'head'])   # Ik_CT space
    An_Space ( info['ct'][2],  object=info['ct'][2].replace('_CT', '_ori'), targList=targetList, spaceType = 'parent').rebildSpaceObj()
    
    targetList=([ info['generalCt'][2], 'pivotOffset'], [ root_grp, 'world'],  [torso, 'torso'],  )                                      # elbow/knee  Ik_CT space
    An_Space ( info['ct'][0],  object=info['ct'][0].replace('_CT', '_ori'), targList=targetList, spaceType = 'parent').rebildSpaceObj()
    
    
    targetList=[info['generalCt'][2], 'pivotOffset'], [shoulder, 'shoulder'], [pelvis, 'body'], [torso, 'torso'] #upArm_CT space
    An_Space ( info['ct'][3],  object=info['ct'][3].replace('_CT', '_ori'), targList=targetList, spaceType = 'parent').rebildSpaceObj() 




    info['ct']= chnQd().getArm(info['side'])          if 'arm' in info['pfx'] else        chnQd().getLeg(info['side']) 
        
    
    
     



