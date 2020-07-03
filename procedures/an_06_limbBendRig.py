
import maya.cmds as cmds 
from CharacterNames import CharacterNames as chn
from An_Skeleton import An_Skeleton  as An_Skeleton 
from anProcedures import *
#from an_twistSegment import  an_twistSegment
#from an_twistSegmentOld import  an_twistSegmentOld
from an_classControllers import AnControllers as ctrl 
from an_classTwSegment import AnTwSegment
 
def an_06_limbBendRig(action = 'rig', limb=''):    #'delRig', 
    win = "limbBendOptionWin"
    if action =='rig':          ######### if rig mod  
    
        if  cmds.window (win, exists=True ):
            if cmds.checkBoxGrp('CHBlVer', q=True,   v1= True ):
                limbLightVerRig(limb)
            else:
                limbRig(limb)
        else:
            limbLightVerRig(limb)

    elif action =='delRig':     ######### if delete mod:                                                                         
        delLimbBendRig(limb)
        
    elif action =='option': 
        if  cmds.window (win, exists=True ): cmds.deleteUI (win)
        cmds.window (win, t="Limb Rig Option", width=420,  height=390, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ('bridgLayout', adjustableColumn=True)
        cmds.text ('          Resolution:',h=30, al='left')
        cmds.floatSliderGrp('ISG_radius', label='Radius:', field=True, min=0, max=10,  v=0.5 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_rSab', label='Radius subdivisions:', field=True, min=1, max=30,  v=8 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_jnt', label='Bend joint number:', field=True, min=3, max=30,  v=8 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.checkBoxGrp('CHBlVer', label='Light version :     ', v1=1 )  
        cmds.showWindow()  
    
def getInfo(limb): 
    
    info = {'side':chn(limb).divideName()[0]}   #geoPar=[radius, subdAxis, subdHight] 
    win = "limbBendOptionWin"
    info['lightVersion'] = True
    if  cmds.window (win, exists=True ):  
        #info ['radius']= cmds.floatSliderGrp('ISG_radius', q=True,   v= True )
        info['lightVersion'] =  cmds.checkBoxGrp('CHBlVer', q=True,   v1= True ) 

    info ['rSab'] = cmds.intSliderGrp('ISG_rSab', q=True,   v= True )      if  cmds.window (win, exists=True )  else 8
    info ['jntNum'] = cmds.intSliderGrp('ISG_jnt', q=True,   v= True )     if  cmds.window (win, exists=True )  else 8
            
    info['pfx'] =  info['side']+'armBend' if 'Arm' in chn(limb).divideName()[1] else info['side']+'legBend'    #get arm or leg    
                     #if arm                                                                            #if leg
    #info['rootJnt'] = An_Skeleton().torsoJnt        if 'arm' in info['pfx'] else          An_Skeleton().hipsJnt 
    info['ct']= chn().bends(info['side']) [0:3]     if 'arm' in info['pfx'] else          chn().bends(info['side']) [3:]
    
            # upVector for liht version    
    if info['lightVersion']: 
        info['upAxis'] = [ 'z', 'y']                      if 'arm' in info['pfx'] else          [ 'z', 'z']      # upAxis for m path orient  
        
    else:   # upVector for Old version 
        info['upAxis'] = ['y', 'z', 'y']                      if 'arm' in info['pfx'] else          ['z', 'z', 'z']      # upAxis for m path orient  
        info['worldUp']= ['y', 'z', 'y']                       if 'arm' in info['pfx'] else         ['z', 'z', 'z'] 
    
        if info['side'] == 'r_' and 'arm' in info['pfx']  : info['worldUp'][1]= '-'+info['worldUp'][1] 

    if 'arm' in info['pfx']: #if arm  
        jnt = [An_Skeleton().shoulderJnt, An_Skeleton().upArmJnt, An_Skeleton().foreArmJnt, An_Skeleton().handJnt]  
    else:                    #if leg
        jnt = [An_Skeleton().hipJnt, An_Skeleton().upLegJnt, An_Skeleton().lowLegJnt,  An_Skeleton().footJnt,  An_Skeleton().toeJnt[0], An_Skeleton().toeJnt[1]]
    info['jnt']= [info['side']+chn(x).divideName()[1]+chn(x).divideName()[2] for x in jnt]
    info['generalCt']= chn().general 
    info['gScale'] = cmds.floatSliderGrp('ISG_gScale', q=True, v= True )
    info['limbAttr'] = info['side']+'arm'           if 'arm' in info['pfx'] else          info['side']+'leg' 
    return info    
    
def delLimbBendRig(limb=''):
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0] 
    info = getInfo(limb)     
    an_delSys(info['pfx']+'Rig_grp')
    
    
def addLimbAttr (ctName, limbName):
    if not cmds.objExists (ctName+'.'+limbName):
        cmds.addAttr (ctName,  dt="string", ln="limb")
    else:
        cmds.setAttr (ctName+ ".limb", l=False ) 
    cmds.setAttr (ctName+ ".limb",  limbName,  type="string" )
    cmds.setAttr (ctName+ ".limb", l=True )    



####*******************************************************************************************************************************

#limb = 'l_Arm'

def limbLightVerRig(limb=''):
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0] 
    #limb = "l_Arm"    
    info = getInfo(limb) 
     
        # 1. Make rig group and special controller for sholder twist orientation_____________________________
    
    
    axisCt = ctrl(info['pfx']+'axis_tr')
    axisCt.makeOrientAxis(info['gScale'])  
    #axisCt.gropeCT()
    if 'arm' in info['pfx']:
        axisCt.placeCT ( info['jnt'][0],  tape = "parent")
        axisCt.placeCT ( info['jnt'][1],  tape = "point")
        
        # system for setup shoulders up axises 

        stTarg =cmds.createNode ('transform',  n = info['pfx']+'StTarg') 
        cmds.parent(stTarg , axisCt.oriGrp ) 
        
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']: cmds.setAttr( stTarg+'.'+attr, 0 )
        cmds.setAttr( stTarg+'.tx',  cmds.getAttr( info['jnt'][2]+'.tx' ))
        midTarg = cmds.createNode ('transform',  n = info['pfx']+'MidTarg') 
        
        cmds.pointConstraint( info['jnt'][2], stTarg, midTarg)
        aim =[1, 0, 0]      if 'l_arm' in info['pfx']    else [-1, 0, 0]   
        cmds.aimConstraint( midTarg, axisCt.conGrp,  aim=aim,  u=[0, 1, 0], wu=[0, 1, 0],  wuo= info['jnt'][0], wut="objectrotation"   )  
        cmds.parent(midTarg , axisCt.oriGrp ) 
         
    else:
        axisCt.placeCT ( info['jnt'][1],  tape = "parent")
    
    
    cmds.parentConstraint( info['jnt'][0], axisCt.oriGrp, mo=True)
    
    
    
    axisCt.hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v']) 
    info['rigGrp'] = rigGrp = cmds.group(axisCt.oriGrp, n=info['pfx']+'Rig_grp')# rig grp
    cmds.addAttr (rigGrp, ln="upAxisVis", at="enum", en="off:on", keyable=True)
    
    cmds.connectAttr(rigGrp+'.upAxisVis ',  axisCt.oriGrp+'.v') 
        # 2. Make controllers _____________________________________________________
    
    MDV1 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV1')   # multiplyDivide for follow effect    
         
    upCtObj, midCtObj, dwCtObj = [ctrl(x)for x in  info['ct']] # criate  ct objects
    
    for i, ctObj in enumerate([upCtObj, midCtObj, dwCtObj]): 
        ctObj.makeController('circle', 2*info['gScale'])               
        ctObj.rotateCt([0, 90, 90]) 
        #ctObj.gropeCT()  
        ctObj.addColor ( info['generalCt'][0], "add")
        cmds.connectAttr ( info['generalCt'][0]+'.addCtrls', ctObj.name+'.v' ) 
        ctObj.hideAttr(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']) 
        addLimbAttr(ctObj.name, info['limbAttr'])
        
        if ctObj.name == midCtObj.name:  
            cmds.addAttr (ctObj.name, longName='follow', dv=0.4,  min=0, max=1, keyable=True )
            for cord in ('Y', 'Z'): 
                cmds.connectAttr(ctObj.name+'.follow ',  MDV1+'.input1'+cord)
                cmds.connectAttr(ctObj.name+'.t'+cord.lower(), MDV1+'.input2'+cord)
        else:  
            for cord in ('Y', 'Z'): cmds.connectAttr(MDV1+'.output'+cord,  ctObj.conGrp+'.t'+cord.lower())
            
                                       # 3. Make aim group, place controllers and constraint it_____________________________________________________
        
        cmds.delete (cmds.pointConstraint( info['jnt'][i+1], ctObj.oriGrp )) 
            
    ofsetGrp = [] 
    for jnt, obj, aim in ( [info['jnt'][1], upCtObj, 1], [info['jnt'][3], dwCtObj, -1]):
        grp = cmds.group (em=True, n= chn(obj.name).divideName()[0]+chn(obj.name).divideName()[1]+'Aim_grp')
        ofsetGrp.append (grp)
        cmds.pointConstraint( jnt, grp)    
        constr = cmds.aimConstraint(midCtObj.name, info['jnt'][2], grp, aim=[aim,0,0], u=[0,0,1], wuo= info['jnt'][2], wu=[0,0,1], wut= "objectrotation" )
        cmds.parent(obj.oriGrp, grp)
    
        cmds.connectAttr(midCtObj.name+'.follow ',  constr[0]+'.'+midCtObj.name+'W0')   #turn of aim constrain via revers nod
        revNod = cmds.createNode ('reverse',  n = chn(obj.name).divideName()[0]+chn(obj.name).divideName()[1]+'Ofs_Revers')
        cmds.connectAttr ( midCtObj.name+'.follow ', revNod+'.inputX', force=True )
        cmds.connectAttr ( revNod+'.outputX', constr[0]+'.'+info['jnt'][2]+'W1', force=True )
        cmds.setAttr(obj.oriGrp +'.r', 0,0,0)
    
    for jntA, jntB, obj in ([ info['jnt'][1], info['jnt'][2], upCtObj ],  [info['jnt'][3], info['jnt'][2], dwCtObj]):
        cmds.delete (cmds.pointConstraint( jntA, jntB, obj.oriGrp ))
    
    cmds.pointConstraint(info['jnt'][2], midCtObj.oriGrp )
    const = cmds.orientConstraint(info['jnt'][1], info['jnt'][2], midCtObj.oriGrp )[0]
    if  info['side'] =='r_': cmds.setAttr (const+'.offsetZ', 180)
    cmds.setAttr (const+'.interpType', 2) 
    
    conGrp = cmds.group (ofsetGrp[0], midCtObj.oriGrp, ofsetGrp[1], n= info['pfx']+'Controllers_grp')
    cmds.parent (conGrp, rigGrp)
    
    # 3. Make curves and clasters for it 
    pointsForCurves = [axisCt.name, upCtObj.name, midCtObj.name], [midCtObj.name, dwCtObj.name, info['jnt'][3] ]
    
    twCurves = []
    for i in [0, 1]:
        curv = cmds.curve(n=info['pfx']+['Up', 'Dw'] [i] +"_crv", p=[[0,0,0], [0,0,0], [0,0,0]], d=2)
        cmds.setAttr (curv+".inheritsTransform", 0)
        cmds.parent(curv, rigGrp)
        twCurves.append(curv)
        for x in [0, 1, 2]:
            clst = cmds.cluster (curv+ '.cv['+str(x)+']' ,  n=info['pfx']+['Up', 'Dw'] [i] +str(x)+ "_clst" )[1]
            cmds.parent(clst, pointsForCurves[i][x])
            cmds.setAttr (clst+'.translate', 0,0,0)
            cmds.setAttr (clst+'.rotate', 0,0,0) 
            an_connectRigVis (rigGrp, [clst])
            
    # 4 Make tw
    
    upTwSegment = AnTwSegment( info['side']+ 'up', baseObjects= [axisCt.name, info['jnt'][2]], parentObj= info['rigGrp'])
    upTwSegment.curve= twCurves[0]
    upTwSegment.makeTwSegment()

    dwTwSettings = AnTwSegment( info['side']+ 'dw', baseObjects= [info['jnt'][2], info['jnt'][3]], parentObj= info['rigGrp'])
    upTwSegment.curve= twCurves[1]
    dwTwSettings.makeTwSegment()


    
    '''
    upTwSettings= [(axisCt.name, info['upAxis'][0]), (info['jnt'][2], info['upAxis'][0])]
    dwTwSettings= [(info['jnt'][2], info['upAxis'][1]), (info['jnt'][3], info['upAxis'][1])]
    twData =[]
    for data in [('Up', twCurves[0], upTwSettings, upCtObj.name ),    ('Dw', twCurves[1], dwTwSettings, dwCtObj.name ) ]:
        twInfo = {'pfx': info['pfx']+data[0]}
        twInfo ['curveName'] = data[1]
        twInfo ['jntNum'] = info ['jntNum']
        twInfo ['stretchable']=True
        twInfo['twSettings']= data[2]
        twInfo['scaleObj']= info['generalCt'][1]
        twInfo['geo']=True
        twInfo['subAx'] = info ['jntNum']
        twInfo = an_twistSegment (twInfo)       
        cmds.addAttr (data[3], ln="squashSwitch", min=0, max=5 , keyable=True)
        cmds.connectAttr(data[3]+'.squashSwitch ',  twInfo['rigGrp']+'.sqSwitch')  
        twData.append(twInfo) 
        cmds.parent (twInfo['rigGrp'], info['rigGrp'])
    info ['twData'] = twData
   
    
    an_delSys(rigGrp, objList =[info['twData'][0]['rigGrp'], info['twData'][1]['rigGrp']]) 
    an_connectRigVis (rigGrp, [    info['twData'][0]['rigGrp'],    info['twData'][1]['rigGrp'], twCurves[0],   twCurves[1], ])
    '''
    
    an_delSys(rigGrp, objList =[upTwSegment.rigGrp, dwTwSettings.rigGrp]) 
    an_connectRigVis (rigGrp, [ upTwSegment.rigGrp, dwTwSettings.rigGrp , twCurves[0], twCurves[1] ])
        
    cmds.parent (rigGrp, info['generalCt'][2])
    
    # aim constraint to axis ct from Oleg Nechaev:
    #if 'l_arm' in info['pfx']: cmds.aimConstraint( info['jnt'][2], axisCt.conGrp,  aim=[1, 0, 0],  u=[1, 0, 0], wu=[1, 0, 0],  wuo= info['jnt'][0], wut="objectrotation"   )    
    #if 'r_arm' in info['pfx']: cmds.aimConstraint( info['jnt'][2], axisCt.conGrp,  aim=[-1, 0, 0],  u=[1, 0, 0], wu=[1, 0, 0],  wuo= info['jnt'][0], wut="objectrotation"   )          
            
                
#  Make rig Old Version ///////////////////////////////////////////////////////////////////////////////////////////////////

def limbRig(limb=''):

    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0]
    info = getInfo(limb)
    
        # 1. Make rig group and special controller for sholder twist orientation_____________________________
    
    axisCt = ctrl(info['pfx']+'axis_tr')
    axisCt.makeOrientAxis(info['gScale'])  
    #axisCt.gropeCT()
    if 'arm' in info['pfx']:
        axisCt.placeCT ( info['jnt'][0],  tape = "parent")
        axisCt.placeCT ( info['jnt'][1],  tape = "point")
    else:
        axisCt.placeCT ( info['jnt'][1],  tape = "parent")
    #
    axisCt.hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v']) 
    cmds.parentConstraint(info['jnt'][0], axisCt.oriGrp, mo=True )
    
    rigGrp = cmds.group(axisCt.oriGrp, n=info['pfx']+'Rig_grp')# rig grp
    cmds.addAttr (rigGrp, ln="upAxisVis", at="enum", en="off:on", keyable=True)
    cmds.connectAttr(rigGrp+'.upAxisVis ',  axisCt.oriGrp+'.v') 
        
        # 2. Make controllers _____________________________________________________
    
    MDV1 =cmds.createNode ('multiplyDivide',  n = info['pfx']+'MDV1')   # multiplyDivide for follow effect    
         
    upCtObj, midCtObj, dwCtObj = [ctrl(x)for x in  info['ct']] # criate  ct objects
    
    for i, ctObj in enumerate([upCtObj, midCtObj, dwCtObj]): 
        ctObj.makeController('circle', 2*info['gScale'])               
        ctObj.rotateCt([0, 90, 90]) 
        #ctObj.gropeCT()  
        ctObj.addColor ( info['generalCt'][0], "add")
        cmds.connectAttr ( info['generalCt'][0]+'.addCtrls', ctObj.name+'.v' ) 
        ctObj.hideAttr(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']) 
        addLimbAttr(ctObj.name, info['limbAttr'])
        
        if ctObj.name == midCtObj.name:  
            cmds.addAttr (ctObj.name, longName='follow', dv=0.4,  min=0, max=1, keyable=True )
            for cord in ('Y', 'Z'): 
                cmds.connectAttr(ctObj.name+'.follow ',  MDV1+'.input1'+cord)
                cmds.connectAttr(ctObj.name+'.t'+cord.lower(), MDV1+'.input2'+cord)
        else:  
            for cord in ('Y', 'Z'): cmds.connectAttr(MDV1+'.output'+cord,  ctObj.conGrp+'.t'+cord.lower())
            
                                       # 3. Make aim group, place controllers and constraint it_____________________________________________________
        
        cmds.delete (cmds.pointConstraint( info['jnt'][i+1], ctObj.oriGrp ))

    ofsetGrp = [] 
    for jnt, obj, aim in ( [info['jnt'][1], upCtObj, 1], [info['jnt'][3], dwCtObj, -1]):
        grp = cmds.group (em=True, n= chn(obj.name).divideName()[0]+chn(obj.name).divideName()[1]+'Aim_grp')
        ofsetGrp.append (grp)
        cmds.pointConstraint( jnt, grp)    
        constr = cmds.aimConstraint(midCtObj.name, info['jnt'][2], grp, aim=[aim,0,0], u=[0,0,1], wuo= info['jnt'][2], wu=[0,0,1], wut= "objectrotation" )
        cmds.parent(obj.oriGrp, grp)
    
        cmds.connectAttr(midCtObj.name+'.follow ',  constr[0]+'.'+midCtObj.name+'W0')   #turn of aim constrain via revers nod
        revNod = cmds.createNode ('reverse',  n = chn(obj.name).divideName()[0]+chn(obj.name).divideName()[1]+'Ofs_Revers')
        cmds.connectAttr ( midCtObj.name+'.follow ', revNod+'.inputX', force=True )
        cmds.connectAttr ( revNod+'.outputX', constr[0]+'.'+info['jnt'][2]+'W1', force=True )
        cmds.setAttr(obj.oriGrp +'.r', 0,0,0)

    for jntA, jntB, obj in ([ info['jnt'][1], info['jnt'][2], upCtObj ],  [info['jnt'][3], info['jnt'][2], dwCtObj]):
        cmds.delete (cmds.pointConstraint( jntA, jntB, obj.oriGrp ))

    cmds.pointConstraint(info['jnt'][2], midCtObj.oriGrp )
    const = cmds.orientConstraint(info['jnt'][1], info['jnt'][2], midCtObj.oriGrp )[0]
    if  info['side'] =='r_': cmds.setAttr (const+'.offsetZ', 180)
    cmds.setAttr (const+'.interpType', 2) 
    
    conGrp = cmds.group (ofsetGrp[0], midCtObj.oriGrp, ofsetGrp[1], n= info['pfx']+'Controllers_grp')
    cmds.parent (conGrp, rigGrp)
    
        # 3 made skin jnt_____________________________________________________
        
    curveJntGrp = cmds.group(em=True, n=info['pfx']+'CurveJnt_grp')# driver grp
    nonScaleGrp = cmds.group(em=True, n=info['pfx']+'NonScale_grp')# non scale grp
    curvSkinJnt = []   
    for index, eachJnt in enumerate( [    axisCt.name, upCtObj.name, midCtObj.name, dwCtObj.name, info['jnt'][3]     ] ):
        cmds.select (cl =True)
        drJnt = cmds.joint(n=info['pfx']+'CurvSkin0'+str(index)+'_jnt')
        
        tmpGrp = cmds.group (drJnt, n=info['pfx']+'CurvSkin0'+str(index)+'_grp' )
           
        cmds.delete (cmds.pointConstraint (eachJnt, tmpGrp ))
        cmds.parent (tmpGrp, curveJntGrp)
        cmds.parentConstraint (eachJnt, tmpGrp, mo=False )
        curvSkinJnt.append(drJnt)   
    cmds.parent (curveJntGrp, rigGrp)
    
        # 4. Make curves_____________________________________________________
        
    pos =[]
    for jnt in  curvSkinJnt:
        pos.append(cmds.xform(jnt, q=True, worldSpace=True, t=True ))
    longCurve = cmds.curve(n=info['pfx']+"upSoftCurv", p=pos)
    newSkinClusterName = cmds.skinCluster( curvSkinJnt, longCurve, tsb=True)[0]
    cmds.rebuildCurve(longCurve, rt=0, s=100, ch=True ) 
    dwSoftCurv, upSoftCurv, detachNod  = cmds.detachCurve (longCurve+'.u[1]', ch=True, cos=True, rpo=True ) # detach curve
    
    cmds.addAttr (midCtObj.name, longName='sElbowPos', dv=1,  min=0, max=2, keyable=True )
    cmds.connectAttr ( midCtObj.name+'.sElbowPos', detachNod+'.parameter[0]' )
    
    upCurve = cmds.curve(n=info['pfx']+"UpCurv", p=pos[0:3], d=2, )
    upClusterName = cmds.skinCluster( curvSkinJnt[0:3], upCurve, tsb=True)[0] 
    dwCurve = cmds.curve(n=info['pfx']+"DwCurv", p=pos[2:], d=2, )
    dwClusterName = cmds.skinCluster( curvSkinJnt[2:], dwCurve, tsb=True)[0] 
    for vCurve in (dwSoftCurv, upSoftCurv, dwCurve, upCurve):
        cmds.rebuildCurve(vCurve, rt=0, s=10, ch=True )
    cmds.parent (dwSoftCurv, upSoftCurv, dwCurve, upCurve, nonScaleGrp)
        
        # 5. Make blend shapse _____________________________________________________
    cmds.addAttr (midCtObj.name, longName='elbowSoftness', dv=0,  min=0, max=1, keyable=True )
    for curvSoft, curveHard in ( [dwSoftCurv, dwCurve],  [upSoftCurv,  upCurve] ):
        vBlend = cmds.blendShape(curvSoft, curveHard)[0]
        cmds.connectAttr ( midCtObj.name+'.elbowSoftness', vBlend+ '.'+curvSoft )

    twSettings=[ (curvSkinJnt[0], info['upAxis'][0],  info['worldUp'][0]),              (info['jnt'][2],  info['upAxis'][1],  info['worldUp'][1] ),]
    jointNameA, ikHandlA, scaleGrpA, geoA, nonScaleGrpA = an_twistSegmentOld (upCurve, pfx=info['pfx']+'Up',  jntNum = info ['jntNum'],  stretchable=1,  twSettings=twSettings, scaleObj=chn().general[1], geo=True, subAx=info ['rSab'])
    
    twSettings=[  (info['jnt'][2],  info['upAxis'][1],  info['worldUp'][1]  ),          (info['jnt'][3],  info['upAxis'][2],  info['worldUp'][2] ),]
    jointNameB, ikHandlB, scaleGrpB, geoB, nonScaleGrpB = an_twistSegmentOld (dwCurve, pfx=info['pfx']+'Dw',  jntNum = info ['jntNum'],  stretchable=1,  twSettings=twSettings, scaleObj=chn().general[1], geo=True, subAx=info ['rSab'])
    
    for ct, grp in ((info['ct'][0], scaleGrpA), (info['ct'][2], scaleGrpB)): 
        cmds.addAttr (ct, ln = 'squashSwitch', min = 0, max =30, dv=1, keyable= True )
        cmds.connectAttr (ct+'.squashSwitch',  grp+'.squashSwitch')
    
    for part in ['Up', 'Dw']: 
        for attr in ['twOffs0', 'twOffs1', 'squashOffset', 'geoRadius']:
            defVal = cmds.getAttr(info['pfx']+part+'TwJnt_grp.'+attr)
            cmds.addAttr (rigGrp, ln = part+attr, dv=defVal, keyable= True )
            cmds.connectAttr (rigGrp+'.'+part+attr, info['pfx']+part+'TwJnt_grp.'+attr)
        
    cmds.parent( nonScaleGrpA, nonScaleGrpB, nonScaleGrp)
    cmds.parent( scaleGrpA, scaleGrpB, rigGrp)

    an_delSys(rigGrp, objList =[scaleGrpA, scaleGrpB, nonScaleGrp]) 
    an_connectRigVis (rigGrp, [nonScaleGrp, jointNameA[0], jointNameB[0], curveJntGrp, ikHandlA[0]])
    
    cmds.parent (rigGrp, info['generalCt'][2])
    cmds.parent (nonScaleGrp, chn().rigStructure( query=True,   rigFold=True) ['bridgeNoneScale']) 
    
    print 'limb redy' 
    
 
    
    
    
    
    
    
    

 