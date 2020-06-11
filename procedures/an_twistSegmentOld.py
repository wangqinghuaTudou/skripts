

#pfx='l_foreArm'
#curveName='l_armBendDwCurv'
#jntNum = 10
#stretchable=True
#twSettings =[('l_armBendCurvSkin02_jnt', 'z', 'z'), ('l_armBendCurvSkin04_jnt', 'y', 'y')] # y axis twJnt to to  obj z axis   ( z orient to y )
#scaleObj= 'general_CT'
#########################################################
#an_twistSegment (curveName, pfx,  jntNum = jntNum, stretchable=True,  twSettings=twSettings, scaleObj=scaleObj, geo=True)

#an_twistSegment (curveName, pfx='',  jntNum = 10, stretchable=True,  twSettings=twSettings, scaleObj=scaleObj, geo=True, subAx=12)


import maya.cmds as cmds
from  anProcedures import an_delSys

def an_twistSegmentOld (curveName, pfx='',  jntNum = 10, stretchable=True,  twSettings=[], scaleObj='', geo=True, subAx=12):   # twSettings = [('l_jnt', 'y', 'z'), ('l_a2_jnt', 'y', 'z')]

    pfx = curveName+'ChSys' if not pfx else pfx

    scaleGrp = cmds.group (em=True, n=pfx+'TwJnt_grp')
    nonScaleGrp = cmds.group (em=True, n=pfx+'NonScale_grp')


    cmds.select (cl=True)

    if stretchable: #If the joints should be stretched.

        curvLength  = cmds.arclen(curveName, constructionHistory = True)

        scaleMDVnod = cmds.createNode ('multiplyDivide', n= pfx+'scaleMDV') # scale solver sys
        cmds.setAttr (scaleMDVnod+".operation", 2)
        cmds.connectAttr (curvLength+'.arcLength',  scaleMDVnod+'.input1X')
        if not cmds.objExists(scaleGrp+'.scaleCompensator'): cmds.addAttr (scaleGrp, ln='scaleCompensator', k=True, dv=1)
        cmds.connectAttr (scaleGrp+'.scaleCompensator',  scaleMDVnod+".input2X")
        if scaleObj: cmds.connectAttr (scaleObj+'.sx',  scaleGrp+'.scaleCompensator')
        blTwoAttr = cmds.createNode ('blendTwoAttr', n= pfx+'_blta')     #sqosh switch
        cmds.connectAttr (scaleMDVnod+'.outputX', blTwoAttr+'.input[1]')
        cmds.setAttr (blTwoAttr+'.input[0]', cmds.arclen(curveName))
        jntPosMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'jPosMDV',  asUtility=True) # solve jnt length (X) and scale kooficient
        cmds.connectAttr (blTwoAttr+'.output',  jntPosMDVnod+'.input1Y')
        cmds.connectAttr (scaleMDVnod+'.outputX',  jntPosMDVnod+'.input1X')
        cmds.setAttr (jntPosMDVnod+".input2X", jntNum)
        cmds.setAttr (jntPosMDVnod+".operation", 2)
        cmds.setAttr (jntPosMDVnod+".input2Y", cmds.arclen(curveName))

    jointName = range(jntNum+1) # create joints
    for index, string in enumerate(range(jntNum+1)):
    		 jointName[index]= cmds.joint (r=True , n=pfx+str(index)+'_jnt', p= [cmds.arclen(curveName)/jntNum, 0, 0])
    		 if stretchable: cmds.connectAttr (jntPosMDVnod+'.outputX',  jointName[index]+'.tx')

    if geo:
        geo = cmds.polyCylinder (r=cmds.arclen(curveName)/jntNum/3, h=cmds.arclen(curveName), sx=subAx, sy=jntNum, sz=0, ax=[1,0,0], rcp=0, cuv=3, ch=1, n= pfx+'Tw_geo' )
        cmds.delete (cmds.pointConstraint (jointName[0], jointName[-1], geo))
        cmds.skinCluster(jointName[:-1],  geo, tsb=True)

    ikHandl = cmds.ikHandle  (n=pfx+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=jointName[0], ee= jointName[-1], c=curveName)

    cmds.parent (jointName[0], scaleGrp)


    if twSettings:           ###################################################################
        def an_axisToVector (axis):
            return {'x':(1.0,0,0), 'y':(0,1.0,0), 'z':(0,0,1.0) ,  '-x':(-1.0,0,0), '-y':(0,-1.0,0), '-z':(0,0,-1.0) }[axis]

        onCurvJnts=[]
        for i in xrange(2):
            cmds.select (cl=True)
            onCurvJnt = cmds.joint( n=pfx+'TwAim'+str(i)+'_jnt')
            WorldUpObj = twSettings[i][0]
            UpAxis =     twSettings[i][1]
            WorldUp =  an_axisToVector (twSettings[i][2])
            inverseUp = True if '-' in UpAxis else False

            motionPath = cmds.pathAnimation( onCurvJnt, c=curveName , wut='objectrotation', f=True, fa='x', ua=UpAxis[-1], wu= WorldUp, wuo = WorldUpObj, iu=inverseUp  )######################
            cmds.cutKey( motionPath, time=(0,20), attribute='uValue', option="keys" )
            cmds.setAttr (motionPath+'.uValue', i )
            cmds.addAttr (scaleGrp, ln="twOffs"+str(i),   keyable=True)
            cmds.connectAttr ( scaleGrp+'.twOffs'+str(i), motionPath + ".frontTwist" )
            cmds.parent (onCurvJnt, nonScaleGrp)
            onCurvJnts.append(onCurvJnt)


        cmds.setAttr (ikHandl[0]+".dTwistControlEnable", 1)
        cmds.setAttr (ikHandl[0]+".dWorldUpType", 4)
        cmds.connectAttr (onCurvJnts[0]+".worldMatrix[0]", ikHandl[0]+".dWorldUpMatrix")
        cmds.connectAttr (onCurvJnts[1]+".worldMatrix[0]", ikHandl[0]+".dWorldUpMatrixEnd")
        cmds.setAttr (ikHandl[0]+".dWorldUpAxis", 3)
        cmds.setAttr (ikHandl[0]+".dWorldUpVector",  0, 0, 1)
        cmds.setAttr (ikHandl[0]+".dWorldUpVectorEnd",  0, 0, 1)
    if geo:                      ##########################################################################
        cmds.addAttr (scaleGrp, ln = 'squashOffset',  dv=cmds.arclen(curveName), keyable= True )
        cmds.connectAttr (scaleGrp+'.squashOffset',  jntPosMDVnod+".input2Y")
        cmds.addAttr (scaleGrp, ln = 'geoRadius',  dv=cmds.arclen(curveName)/5, keyable= True )
        cmds.connectAttr (scaleGrp+'.geoRadius',  geo[1]+'.radius')

    if stretchable:             ##########################################################################

        # add sqash system
        cmds.addAttr (scaleGrp, ln = 'squashSwitch', min = 0, max =30, dv=1, keyable= True )
        cmds.addAttr (scaleGrp, ln = 'sqShapeCurve',  at='double', k=True )
        cmds.connectAttr (scaleGrp+'.squashSwitch',  blTwoAttr+'.attributesBlender')

        # sqrt(curvLength)
        sqrtLen = cmds.createNode ('multiplyDivide', n= pfx+'SqrtCerve_mdv')
        cmds.setAttr (sqrtLen+".operation", 3)
        cmds.connectAttr (jntPosMDVnod+'.outputY',  sqrtLen+'.input1X')
        cmds.setAttr (sqrtLen+".input2X", 0.5)

        # 1/sqrt
        OneDevSqrt = cmds.createNode ('multiplyDivide', n= pfx+'OneDevSqrt_mdv')
        cmds.setAttr (OneDevSqrt+".operation", 2)
        cmds.setAttr (OneDevSqrt+".input1X", 1)
        cmds.connectAttr (  sqrtLen+'.outputX', OneDevSqrt+".input2X")

        # now that we have the objects, we can create the animation curve which will control the attribute
        numControls = len(jointName)
        objAttr = scaleGrp + ".sqShapeCurve"
        cmds.setKeyframe (scaleGrp, at=".sqShapeCurve", t=1, v=0 )
        cmds.setKeyframe (scaleGrp, at=".sqShapeCurve", t=numControls, v=0)

        cmds.keyTangent (scaleGrp, wt = 1, at=".sqShapeCurve")
        cmds.keyTangent (scaleGrp, weightLock = False, at=".sqShapeCurve")
        cmds.keyTangent (objAttr, e = True,   a = True,  t= (1,1) ,  outAngle=50)
        cmds.keyTangent (objAttr, e = True,   a = True,  t=(numControls, numControls),  inAngle=-50)

        # connect to jnt scale
        for x in range(numControls):
            fc = cmds.createNode ('frameCache', n= pfx+'_frameCache'+str(x)+'_fc')
            cmds.connectAttr (objAttr, fc + ".stream")
            cmds.setAttr (fc + ".vt", x+1)

            pow = cmds.createNode ('multiplyDivide', n= pfx+'Pow_mdv')
            cmds.setAttr (pow+".operation", 3)
            cmds.connectAttr (  OneDevSqrt+'.outputX', pow+".input1X")
            cmds.connectAttr (fc + '.v',  pow+'.input2X' )

            cmds.connectAttr (pow+'.outputX', jointName[x]+'.sz')
            cmds.connectAttr (pow+'.outputX', jointName[x]+'.sy')

    #nonScaleGrp = cmds.group (geo[0] , ikHandl[0], n=pfx+'NonScale_grp')
    cmds.parent(geo[0] , ikHandl[0], nonScaleGrp)
    if stretchable: an_delSys(scaleGrp, objList =[ikHandl[0], scaleGrp, jntPosMDVnod, scaleMDVnod, curvLength, blTwoAttr])
    else: an_delSys(ikHandl[0], objList =[scaleGrp, ])
    return jointName, ikHandl, scaleGrp, geo[0], nonScaleGrp



#$scale = curveInfo5.normalizedScale (realLen/seurseLen)
#$sqrt = 1/sqrt($scale)
#pfx0_jnt.scaleY = pow($sqrt,pfx0_jnt.pow)



















