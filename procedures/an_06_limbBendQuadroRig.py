from  anProcedures import  * 
from an_classControllers import AnControllers  as ctrl
from  an_classTwSegment import  AnTwSegment
from an_classNames import AnNames as chn
from an_classSkeletonQuadro import AnSkeletonQuadro



#pfx = 'l_LegBend'
#inJnt = ['l_upLeg_jnt', 'l_lowLeg_jnt', 'l_foot_bind', 'l_toe_bind']

def getInfo(limb): 
    info = {'jntNum':[10, 7, 7]}
    info['generalCt']= chn().general() 
    info['gScale'] = 4
    if limb: 
        info['side'] = chn(limb).divideName()[0]
        
        info['pfx'] =  info['side']+'armBend' if 'Arm' in chn(limb).divideName()[1] else info['side']+'legBend'    #get arm or leg
        info['jnt']= AnSkeletonQuadro().getSkeletonPart( 'arm' if 'arm' in info['pfx'] else 'leg', side= info['side'] )
        limbTape = info['side']+'arm' if  'Arm' in chn(limb).divideName()[1] else info['side']+'leg'
        info['ctList'] = [x+'Bend_CT' for x in       ( chn(info['jnt'][1]).sfxMinus(),  limbTape+'UpKnee',  chn(info['jnt'][2]).sfxMinus(),  limbTape+'DwKnee', chn(info['jnt'][3]).sfxMinus())]
    return info




def an_06_limbBendQuadroRig(action = 'rig', limb=''):    #'delRig', 

    info = getInfo(limb) 

    win = "limbBendOptionWin"
    if action =='rig':          ######### if rig mod       
        bendQuadroRig(limb)
    elif action =='delRig':     ######### if delete mod:                                                                         
        delLimbBendRig(limb)        
    elif action =='option':
        if  cmds.window (win, exists=True ): cmds.deleteUI (win) 
        cmds.window (win, t="Limb Rig Option", width=420,  height=390, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ('bridgLayout', adjustableColumn=True)
        cmds.text ('          Resolution:',h=30, al='left')
        cmds.floatSliderGrp('ISG_radius', label='Radius:', field=True, min=0, max=10,  v=0.5 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_rSab', label='Radius subdivisions:', field=True, min=1, max=30,  v=8 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.canvas( height=10 )
        cmds.intSliderGrp('ISG_Upjnt', label='Up joint number:', field=True, min=3, max=30,  v=info['jntNum'][0] , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_Midjnt', label='Mid joint number:', field=True, min=3, max=30,  v=info['jntNum'][1] , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_Dwjnt', label='Dw joint number:', field=True, min=3, max=30,  v=info['jntNum'][2] , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.showWindow()  

#  an_06_limbBendQuadroRig(action = 'option', limb='')

def addElbowTypeController (pfx,  bendObj, upObj, ctSize): 
    ctObj = ctrl(pfx+'_CT').makeController ( 'circle', size=ctSize,  orient="X",   pos=bendObj,  posType='parent')
    cmds.pointConstraint (bendObj, ctObj.oriGrp)
    constraint = cmds.orientConstraint (bendObj, upObj, ctObj.oriGrp, mo=False)[0]
    cmds.setAttr (constraint+".interpType", 2)
    return ctObj

def bendQuadroRig(limb=''):
    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0]
    info = getInfo(limb)
    
    rigGrp = cmds.group (n=info['pfx']+'Rig_grp', em=True)
    cmds.parent (rigGrp, info['generalCt'][2])
    
    Ct2Obj= addElbowTypeController (chn(info['ctList'][1]).sfxMinus(),    info['jnt'][2], info['jnt'][1],   ctSize=info['gScale'])
    Ct4Obj= addElbowTypeController (chn(info['ctList'][3]).sfxMinus(),    info['jnt'][3], info['jnt'][2],   ctSize=info['gScale'])
    cmds.parent( Ct2Obj.oriGrp, Ct4Obj.oriGrp, rigGrp)
    
    uAx = ['z', 'z']
    scl = info['generalCt'][1]
    
    
    Ct1Obj = AnTwSegment(   chn(info['ctList'][0]).sfxMinus(),      baseObjects = [info['jnt'][1],  Ct2Obj.name],     parentObj=rigGrp )
    Ct1Obj.jntNum, Ct1Obj.upAxis, Ct1Obj.scaleGrp     =    info['jntNum'][0], uAx, scl
    Ct1Obj.makeTwSegment()
    
    
    Ct3Obj = AnTwSegment(   chn(info['ctList'][2]).sfxMinus(),    baseObjects = [Ct2Obj.name, Ct4Obj.name],     parentObj=rigGrp )
    Ct3Obj.jntNum, Ct3Obj.upAxis, Ct3Obj.scaleGrp     =    info['jntNum'][1], uAx, scl
    Ct3Obj.makeTwSegment()
    
    
    Ct5Obj = AnTwSegment(   chn(info['ctList'][4]).sfxMinus(),    baseObjects = [Ct4Obj.name,  info['jnt'][4]],     parentObj=rigGrp )
    Ct5Obj.jntNum, Ct5Obj.upAxis, Ct5Obj.scaleGrp     =    info['jntNum'][2], uAx, scl
    Ct5Obj.makeTwSegment()
    
    for i, ctObj in enumerate([Ct1Obj.ctList[1] ,    Ct2Obj, Ct3Obj.ctList[1], Ct4Obj, Ct5Obj.ctList[1]]): # ctrlObj
        cmds.connectAttr ( info['generalCt'][0]+'.addCtrls', ctObj.name+'.v' ) 
        ctObj.hideAttr(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']) 
        ctObj.addColor ( info['generalCt'][0], "add")
     
    
    for obj in [Ct1Obj, Ct3Obj, Ct5Obj]:  #print obj.endsClasters, obj.curveName 
        an_connectRigVis(rigGrp, [obj.rigGrp,] ) 
            
    
















 

 