
#17 06 2019  add setCylinderWheight() function


import maya.cmds as cmds
from  anProcedures import * 
from an_classSkin import *
#from an_twistSegment import * 
#info={}
#info['pfx']='l_upArm' 
#info['curveName']='l_armBendUp_crv'
#info['jntNum'] = 10
#info['stretchable']=True
#info['twSettings'] =[('l_armBendaxis_tr',  'z'), ('l_foreArm_jnt', 'z')] # define up vector
#info['scaleObj']= 'general_CT'
#info['geo']=True
#info['subAx'] = 12


def setCylinderWheight(geo, rSub=8):
    self = AnSkinSys(geo)
    self.getSkinWeights()
    jnts = self.weightList.keys()
    jnts.sort()
    pNum = len(self.weightList[jnts[0]])

    for i in range(len(jnts)):
        self.weightList[jnts[i]] = [0] * pNum
        for j in range(i * rSub, i * rSub + rSub):
            self.weightList[jnts[i]][j] = 1
    for j in range(pNum - rSub, pNum):
        self.weightList[jnts[-1]][j] = 1
    # set value 1 for second jnt (0-Sub range of points)
    for j in range(rSub):
        self.weightList[jnts[1]][j] = 1
    # remove first jnt from cluster
    del self.weightList[jnts[0]]

    self.setSkinWeights()



def an_twistSegment (info):

    pfx = info['pfx']
    curveName = info['curveName']
    jntNum = info['jntNum']
    stretchable = info['stretchable']
    twSettings = info['twSettings'] 
    scaleObj = info['scaleObj']
    geo = info['geo']
    subAx = info['subAx']
     
    #grp 
    info['rigGrp'] = rigGrp = cmds.group (em=True, n=pfx+'TwJnt_grp')
    cmds.select (cl=True) 
    
    #jnt 
    jointName = range(jntNum+1)  
    for index, string in enumerate(range(jntNum+1)):   
    		 jointName[index]= cmds.joint (r=True , n=pfx+str(index)+'_jnt', p= [cmds.arclen(curveName)/jntNum, 0, 0])
    info['twJnt'] = jointName
    
    #ik 
    info['ikHandl'] = ikHandl = cmds.ikHandle  (n=pfx+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=jointName[0], ee= jointName[-1], c=curveName)[0]
    cmds.parent(jointName[0], ikHandl, rigGrp)
    
    #if geo:
    geo = cmds.polyCylinder (r=cmds.arclen(curveName)/jntNum*1.2, h=cmds.arclen(curveName), sx=subAx, sy=jntNum, sz=0, ax=[1,0,0], rcp=0, cuv=3, ch=1, n= pfx+'Tw_geo' )[0]
    cmds.delete (cmds.pointConstraint (jointName[0], jointName[-1], geo))
    cmds.delete (cmds.aimConstraint (jointName[0], geo, aim=[-1, 0, 0]))
    cmds.skinCluster(jointName[:-1],  geo, tsb=True, )
    setCylinderWheight( geo, rSub=subAx)
    cmds.parent(geo, rigGrp)    
    cmds.setAttr (geo+".inheritsTransform", 0)
        
    #twSettings
    if twSettings:  
        dir = {'x':(1.0,0,0), 'y':(0,1.0,0), 'z':(0,0,1.0) ,  '-x':(-1.0,0,0), '-y':(0,-1.0,0), '-z':(0,0,-1.0) }
        cmds.setAttr (ikHandl+".dTwistControlEnable", 1)
        cmds.setAttr (ikHandl+".dWorldUpType", 4)      
        cmds.connectAttr (twSettings[0][0]+".worldMatrix[0]", ikHandl+".dWorldUpMatrix")   
        cmds.connectAttr (twSettings[1][0]+".worldMatrix[0]", ikHandl+".dWorldUpMatrixEnd")          
        cmds.setAttr (ikHandl+".dWorldUpAxis", 3)
        stCord, endCord = dir[twSettings[0][1]], dir[twSettings[1][1]]
        cmds.setAttr (ikHandl+".dWorldUpVector", stCord[0], stCord[1], stCord[2] ) 
        cmds.setAttr (ikHandl+".dWorldUpVectorEnd", endCord[0], endCord[1], endCord[2]) 
    
    #stretchable
    if stretchable:
        curvLength  = cmds.arclen(curveName, constructionHistory = True) 
        xScaleMDVnod = cmds.createNode ('multiplyDivide', n= pfx+'xScaleMDV')
        cmds.setAttr (xScaleMDVnod+".operation", 2)
        cmds.addAttr (rigGrp, ln='scaleCompensator', k=True, dv=1)
        cmds.connectAttr (rigGrp+'.scaleCompensator',  xScaleMDVnod+".input2X")
        cmds.connectAttr (curvLength+'.arcLength',  xScaleMDVnod+'.input1X')
        if scaleObj: cmds.connectAttr (scaleObj+'.sx' ,   rigGrp +'.scaleCompensator' )
        
        jntPosMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'jPosMDV',  asUtility=True)
        cmds.setAttr (jntPosMDVnod+".operation", 2)
        cmds.connectAttr (xScaleMDVnod+'.outputX', jntPosMDVnod+'.input1X')
        cmds.setAttr (jntPosMDVnod+".input2X", jntNum)
        for index in range(jntNum+1):   cmds.connectAttr (jntPosMDVnod+'.outputX',  jointName[index]+'.tx')
        
         # normalizedScale 
        normalizedMDVnod = cmds.createNode ('multiplyDivide', n= pfx+'normalizedMDV')
        cmds.setAttr (normalizedMDVnod+".operation", 2)
        cmds.connectAttr (curvLength+'.arcLength',  normalizedMDVnod+'.input1X')
        cmds.setAttr (normalizedMDVnod+".input2X",  cmds.getAttr (normalizedMDVnod+".input1X"))
        
        for attr in ['defLen', 'realLen']: 
            cmds.addAttr (rigGrp, ln = attr,  dv=1,  k=True )
        cmds.connectAttr (curvLength+'.arcLength', rigGrp+'.realLen')
        cmds.connectAttr ( rigGrp+'.defLen', normalizedMDVnod+".input2X" )
        cmds.setAttr (rigGrp+".defLen",  cmds.getAttr (normalizedMDVnod+".input1X"))
        
         # $scale = curveInfo1.normalizedScale/all_anim.globalScale;'''
        scaleMDVnod = cmds.createNode ('multiplyDivide', n= pfx+'scaleMDV')
        cmds.setAttr (scaleMDVnod+".operation", 2)
        cmds.connectAttr (normalizedMDVnod+'.outputX'  ,  scaleMDVnod+'.input1X')
        cmds.connectAttr (rigGrp+'.scaleCompensator',   scaleMDVnod+'.input2X')
        
        #$sqrt = 1/sqrt($scale);'''
        sqrtScale = cmds.createNode ('multiplyDivide', n= pfx+'SqrtScale_mdv') 
        cmds.setAttr (sqrtScale+".operation", 3)
        cmds.connectAttr (scaleMDVnod+'.outputX',  sqrtScale+'.input1X')
        cmds.setAttr (sqrtScale+".input2X", 0.5)
         
        oneDevide = cmds.createNode ('multiplyDivide', n= pfx+'OneDevide_mdv') 
        cmds.setAttr (oneDevide+".operation", 2)
        cmds.setAttr (oneDevide+'.input1X', 1)
        cmds.connectAttr (sqrtScale+'.outputX',  oneDevide+'.input2X')
        
        # now that we have the objects, we can create the animation curve which will control the attribute'''
        cmds.addAttr (rigGrp, ln = 'sqSwitch',  dv=1,  k=True )
        sqSwitch = cmds.createNode ('multiplyDivide', n= pfx+'sqSwitch_mdv') 
        cmds.connectAttr (rigGrp+'.sqSwitch',   sqSwitch+'.input2X')
        
        numControls = len(jointName)    
        objAttr = sqSwitch + ".input1X" 
        cmds.setKeyframe (sqSwitch, at=".input1X", t=1, v=0 )
        cmds.setKeyframe (sqSwitch, at=".input1X", t=numControls, v=0)
        
        cmds.keyTangent (sqSwitch, wt = 1, at=".input1X")
        cmds.keyTangent (sqSwitch, weightLock = False, at=".input1X")
        cmds.keyTangent (objAttr, e = True,   a = True,  t= (1,1) ,  outAngle=50)
        cmds.keyTangent (objAttr, e = True,   a = True,  t=(numControls, numControls),  inAngle=-50)
        #objAttr = sqSwitch + ".outputX" 
        
        delList = [jointName[0], ikHandl, geo, curvLength, xScaleMDVnod, jntPosMDVnod, normalizedMDVnod, scaleMDVnod, sqrtScale,  oneDevide]
        
        animCurve = cmds.connectionInfo(sqSwitch+".input1X", sfd=1)
        
        for x in range(numControls):  
            fc = cmds.createNode ('frameCache', n= pfx+'_frameCache'+str(x)+'_fc')
            cmds.connectAttr (animCurve, fc + ".stream")
            cmds.setAttr (fc + ".vt", x+1)
            
            pow = cmds.createNode ('multiplyDivide', n= pfx+'Pow_mdv') 
            cmds.setAttr (pow+".operation", 3)
            cmds.connectAttr (  oneDevide+'.outputX', pow+".input1X")
            cmds.connectAttr (fc + '.v',  pow+'.input2X' ) 
            
            sqSwitchBTA = cmds.createNode ('blendTwoAttr', n= pfx+'sqSwitch'+str(x)+'_bta') 
            cmds.connectAttr (rigGrp+'.sqSwitch',   sqSwitchBTA+'.attributesBlender')
            cmds.connectAttr (pow+'.outputX',   sqSwitchBTA+'.input[1]')
            cmds.setAttr(sqSwitchBTA+'.input[0]', 1)
            cmds.connectAttr (sqSwitchBTA+'.output', jointName[x]+'.sz')
            cmds.connectAttr (sqSwitchBTA+'.output', jointName[x]+'.sy')
                   
    cmds.delete(sqSwitch)
    info['delList']= delList
    an_delSys(rigGrp, delList)
    return info

def an_twistSegmentUi(): 

    layouts = an_turnBasedUi('twSegment', 'Twist segment', stepsLabel =['Curve and controllers', 'Twist rig' ])
    def botCom(cont): return  "cmds.textFieldButtonGrp ('"+cont+"', e=True, tx=  cmds.ls (sl=True)[0]);"
    #step 1
    cmds.setParent(layouts[0])
    cmds.separator( style='none' )
    cmds.textFieldGrp ('TFBG_pfx', l='Prefix :',    cw = [(1, 174), (2, 191)]  )
    cmds.textFieldButtonGrp ('TFBG_sObj', l='Scale object   : ',  bl=" Assign ",  cw = [(1, 174), (2, 191), (3, 40)],  bc = botCom('TFBG_sObj') ) 
    cmds.separator( style='none' )
    #step 2
    cmds.setParent(layouts[1])
    cmds.separator( style='none' )
    cmds.textFieldButtonGrp ('TFBG_curve', l='Curve name :',  bl=" Assign ",  cw = [(1, 174), (2, 191), (3, 40)],  bc = botCom('TFBG_curve') ) 
    cmds.intSliderGrp('ISG_jNum', label='Joint number :', field=True, min=2, max=40,  v=10 , cw = [(1, 174), (2, 50) ], enable= True )
    cmds.checkBoxGrp('CBG_strtch',  numberOfCheckBoxes=1, label='Stretchable :  ', v1=True, cw = [(1, 180), (2, 50) ])
    cmds.text (l="   Joint orient settings :", al="left", font= "boldLabelFont")
    cmds.textFieldButtonGrp ('TFBG_uObj', l='Object rotatin start : ',  bl=" Assign ",  cw = [(1, 174), (2, 191), (3, 40)],  bc = botCom('TFBG_uObj') ) 
    cmds.radioButtonGrp('RBG_startAx', label='Start up axis :   ', labelArray2=['Z', 'Y'], sl =1,  numberOfRadioButtons=2, cw = [(1, 180), (2, 50)] )
    cmds.textFieldButtonGrp ('TFBG_bObj', l='Object rotatin end : ',  bl=" Assign ",  cw = [(1, 174), (2, 191), (3, 40)],  bc = botCom('TFBG_bObj') ) 
    cmds.radioButtonGrp('RBG_endAx', label='End up axis :   ', labelArray2=['Z', 'Y'], sl =1,  numberOfRadioButtons=2, cw = [(1, 180), (2, 50)] )
    cmds.text (l="   Geometry settings :", al="left", font= "boldLabelFont")
    cmds.checkBoxGrp('CBG_geo',  numberOfCheckBoxes=1, label='Made geometry :  ', v1=True, cw = [(1, 180), (2, 50) ])
    cmds.intSliderGrp('ISG_sub', label='Subdivisions axis :', field=True, min=2, max=40,  v=12 , cw = [(1, 174), (2, 50) ], enable= True )
    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210) ], columnSpacing=[(2,2), ] ) 
    cmds.button   (l="Delete selected system",  c='an_delSys(cmds.ls(sl=True)[0])')
    cmds.button   (l="Made twist system",  c='an_doTwistSegment()')

def an_doTwistSegment ():
    info={}
    info['pfx']= cmds.textFieldGrp ('TFBG_pfx', q=True,    tx =True  )
    info['scaleObj'] = cmds.textFieldButtonGrp ('TFBG_sObj', q=True,    tx =True  )
    info['curveName']=cmds.textFieldButtonGrp ('TFBG_curve', q=True,    tx =True  )
    info['jntNum'] = cmds.intSliderGrp('ISG_jNum', q=True,    v =True  )
    info['stretchable']=cmds.checkBoxGrp('CBG_strtch', q=True,    v1 =True  )
    obj1 =cmds.textFieldButtonGrp ('TFBG_uObj', q=True,    tx =True  )
    ax1  = ['x', 'z', 'y']  [cmds.radioButtonGrp('RBG_startAx', q=True,    sl =True  )]
    obj2 =cmds.textFieldButtonGrp ('TFBG_bObj', q=True,    tx =True  )
    ax2  = ['x', 'z', 'y']  [cmds.radioButtonGrp('RBG_endAx', q=True,    sl =True  )]
    info['twSettings'] =[(obj1,  ax1), (obj2, ax2)] # define up vector
    info['geo']= cmds.checkBoxGrp('CBG_geo',  q=True, v1=True,  )
    info['subAx'] = cmds.intSliderGrp('ISG_sub', q=True,    v =True  )
        
    an_twistSegment (info) 
 
#pfx='r_handUpEx' 
#ctJnt, endJnt = cmds.ls(sl=True)

def aimJntTwSegment(pfx, ctJnt, endJnt): # joint whethe aimConstrant
    upAx = 'Z'
    length = an_distans( ctJnt, endJnt)
    cmds.select(cl =True  )
    twJnt = cmds.joint( n= pfx+'_jnt')
    twJntEnd = cmds.joint( n= pfx+'End_jnt', p=[length,0,0])
    rigGrp=cmds.group( n=pfx+'Rig_ori', em=True)
    cmds.parent(twJnt, rigGrp)
    upVect = {'Z':[0,0,1], 'Y':[0,1,0]}[upAx]
    cmds.pointConstraint(ctJnt, rigGrp, mo=False)
    cmds.aimConstraint(endJnt, twJnt, aim=[1,0,0], u=upVect, wu=upVect, wut='objectrotation', wuo=ctJnt)
    cmds.pointConstraint(endJnt, twJntEnd, mo=False)





