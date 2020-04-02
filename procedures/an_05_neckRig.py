import maya.cmds as cmds 
#from An_Controllers import An_Controllers  as ctrl 
from An_Skeleton import An_Skeleton  as An_Skeleton 
from CharacterNames import CharacterNames as chn
from  anProcedures import  an_distans,  an_childCapture, an_delSys, an_connectRigVis, an_connectReversAttr, an_helpLine, an_madeInfoConnection
from an_twistSegment import  an_twistSegment
from an_classControllers import AnControllers as ctrl 

def an_05_neckRig(action = 'rig'):     
    if action =='rig':          ######### if rig mod  
        neckRig()
    elif action =='option':     ######### if option mod:
        win = "neckRigOptionWin"
        if  cmds.window (win, exists=True ): cmds.deleteUI (win)
        cmds.window (win, t="Nack Rig Option", width=420,  height=390, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ( adjustableColumn=True)
        cmds.canvas( height=10 )
        cmds.checkBoxGrp( 'bridgCHB' ,  numberOfCheckBoxes=1, label='Made bridge:  ',    
                                cc= "cmds.columnLayout ('neckBridgLayout', e=True, en=cmds.checkBoxGrp( 'bridgCHB' , q=True, v1=True))",
                                v1=True)
        cmds.columnLayout ('neckBridgLayout', adjustableColumn=True)
        cmds.text ('      Bridge option:',h=30, al='left')
        cmds.floatSliderGrp('FSG_ofs', label='Length offset:', field=True, minValue=0.5, maxValue=3.0,  value=1.5, cw = [(1, 124), (2, 50) ] )
        cmds.text ('      Cylinder resolution:',h=30, al='left')
        cmds.intSliderGrp('ISG_hSab', label='Height subdivisions:', field=True, min=1, max=30,  v=6 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_rSab', label='Radius subdivisions:', field=True, min=1, max=30,  v=8 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.showWindow(win)
    elif action =='delRig': 
        print "del"                ######### if delete mod:
        an_delSys('neckRig_grp', []) 
            
def neckRig():
    gScale = cmds.floatSliderGrp('ISG_gScale', q=True, v= True )
    neckJnt, headJnt, torsoJnt = An_Skeleton().neckJnt, An_Skeleton().headJnt[0], An_Skeleton().torsoJnt
    pfx = chn(neckJnt).divideName()[1] 
    switch, genCT = chn().general[0], chn().general[2]
    ct = chn().neck [0]
    ctAdd = chn().neck [1]
    bridgeNoneScale = chn().rigStructure( query=True, rigFold=True) ['bridgeNoneScale']     
    lenOfs = 1.5*gScale
    geoPar=[0.5*gScale,  8, 6]     # geoPar = [radius, subdivisionsAxis, subdivisionsHight]
    upAxisDir=([0,0,1], [0,0,1])
    
    if  cmds.window ("neckRigOptionWin", exists=True ):  # if Option window is open get value 
        lenOfs = cmds.floatSliderGrp('FSG_ofs', q=True,  value=True )
        geoPar[1] = cmds.intSliderGrp('ISG_rSab', q=True,  value=True )
        geoPar[2] = cmds.intSliderGrp('ISG_hSab', q=True,  value=True ) 
         
    neckObj = ctrl(ct) 
    neckObj.makeController( "fk",  size=3*gScale ) # make Controller 
    nOffsJnt = cmds.joint (n=pfx+'Offs_jnt')
    cmds.parent(nOffsJnt,  neckObj.name)
    #neckObj.gropeCT() 
    neckObj.placeCT (neckJnt , "point")
    cmds.delete( cmds.aimConstraint( headJnt, neckObj.oriGrp,  aim=[0, 1, 0],  u=[1, 0, 0],  wu=[0, 0, 1] ,  wut="objectrotation" ,  worldUpObject = neckJnt )) #orient controller
    neckObj.addColor ( switch, "cntrFk")
    
    cmds.connectAttr ( switch+'.'+"bodyCtrls", neckObj.name+'.v' )
 
    neckObj.hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
    cmds.parentConstraint(ct, neckJnt, mo=True)
    cmds.parentConstraint(torsoJnt, neckObj.oriGrp, mo=True)
        
    neckAddObj = ctrl(ctAdd)                # make add Controller 
    neckAddObj.makeController('circle', 2*gScale)
    nAddJnt = cmds.joint (n=pfx+'Add_jnt')
    cmds.parent(nAddJnt,  neckAddObj.name)
    #neckAddObj.gropeCT()
    neckAddObj.placeCT (neckObj.name, "parent")
    cmds.delete(cmds.pointConstraint( neckJnt, headJnt, neckAddObj.oriGrp, mo=False))
    cmds.connectAttr( switch+".addCtrls", neckAddObj.name+'.v')
    neckAddObj.hideAttr(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
    neckAddObj.addColor ( switch, "add")
    oriOfset = cmds.group(em=True, n=pfx+'AddCtOffset_grp')# ofset grp
    cmds.delete(cmds.parentConstraint( neckObj.name,  oriOfset,  mo=False))
    cmds.parent(neckAddObj.oriGrp, oriOfset)
    cmds.parent(oriOfset, neckObj.name)
    cmds.orientConstraint(torsoJnt, neckJnt, oriOfset, mo=True)
    cmds.select (cl=True)
    
    torsoOffsJnt = cmds.joint (n=pfx+'TorsoOffs_jnt')   
    torsoOffsGrp = cmds.group (torsoOffsJnt, n=pfx+'TorsoOffs_ori')
    
    cmds.pointConstraint( torsoJnt,  torsoOffsGrp, w=2 )
    cmds.delete( cmds.pointConstraint( neckJnt,  torsoOffsGrp, w=6 ))
    cmds.delete(cmds.orientConstraint(torsoJnt,  torsoOffsGrp))
    cmds.parentConstraint( torsoJnt,  torsoOffsGrp, mo=True  )
    
    rigGrp = cmds.group(neckObj.oriGrp, torsoOffsGrp, n=pfx+'Rig_grp') 
    cmds.parent(rigGrp, genCT)
    
    for jnt, dir in ([nAddJnt, 'y'],[nOffsJnt, 'y'],[torsoOffsJnt, 'x']): #made ofset attr and connection
                cmds.addAttr(rigGrp, ln=jnt, keyable= True)
                cmds.connectAttr( rigGrp+'.'+jnt, jnt+'.t'+dir    )
    
    vPos = []
    for jnt in [headJnt, nAddJnt, nOffsJnt, torsoOffsJnt]:
        vPos.append( cmds.xform(jnt, q=True, t=True, ws=True))
      
    curveName = cmds.curve (d=3, p=vPos, n=pfx+'Ik_crv' )       # curve  
    cmds.skinCluster (  headJnt, nAddJnt, nOffsJnt, torsoOffsJnt, curveName, dr=10, tsb=True)  
      
    madeBridge = True  if not cmds.window ("neckRigOptionWin", exists=True ) else cmds.checkBoxGrp('bridgCHB' , q=True, v1=True) 
    
    
    if madeBridge: 
        madeBridge=True
        subAx =  12 
        jntNum = 6
        twSettings=[ (headJnt, 'z', 'z'), (torsoOffsJnt, 'z', 'z')]
        
        if  cmds.window ("bodyRigOptionWin", exists=True ):
            subAx = cmds.intSliderGrp('ISG_rSab', q=True, v=True )
            jntNum = cmds.intSliderGrp('ISG_jNum', q=True, v=True )  
            if not cmds.checkBoxGrp( 'bridgCHB' , q=True, v1=True): madeBridge=False
            
            #jointName, ikHandl, scaleGrp, geo, nonScaleGrp = an_twistSegment ( curveName, pfx,  jntNum = jntNum, stretchable=True,  upAxsis=upAxsis, scaleObj= chn().general[1], geo=True, subAx=subAx)
            
                            # 4  Made brige if it nessesery______________________________________
                    
        twInfo= {'pfx':pfx+'Tw'}
        twInfo['curveName'] = curveName
        twInfo['jntNum'] = jntNum
        twInfo['stretchable']= True
        twInfo['twSettings'] = twSettings
        twInfo['scaleObj'] = chn().general[1]
        twInfo['geo']=True
        twInfo['subAx'] = subAx
        twData =  an_twistSegment( twInfo)
        
        an_connectRigVis(rigGrp, [twData['rigGrp'], curveName, nAddJnt, torsoOffsJnt])       
        an_delSys(rigGrp , [twData['rigGrp'],   ]) # vCurve, ikHandl[0],  geo,   
        
        cmds.parent ( twData['rigGrp'], curveName, rigGrp)
        cmds.setAttr (curveName+".inheritsTransform", 0)
                
        #an_madeInfoConnection (rigGrp, {'ct': [x.name for x in  [neckObj, neckAddObj] ]})  
        
        cmds.addAttr (neckObj.name, ln="squashSwitch", min=0, max=5 , keyable=True)
        cmds.connectAttr(neckObj.name+'.squashSwitch ',  twInfo['rigGrp']+'.sqSwitch')
    
    print "neck ok"


#an_05_neckRig(action = 'rig')


