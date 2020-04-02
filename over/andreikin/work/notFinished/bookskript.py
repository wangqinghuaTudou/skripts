v_curve =  cmds.ls(sl=True)[0]
colorSpher (v_curve)



def colorSpher (v_curve):

    pfx = v_curve

    curveInfoNode = cmds.arclen(v_curve, ch=True)
    length = cmds.getAttr ( curveInfoNode+'.arcLength')



    shader = cmds.createNode ( 'surfaceShader', n= pfx+"sShader" )
    v_sphere = cmds.sphere( n=pfx+'Sphere', r=0.1 )
    sphereShape = cmds.listRelatives(v_sphere, s=True)[0]
    cmds.defaultNavigation (source=shader, destination=sphereShape+'.instObjGroups[0]', connectToExisting=True)

    cmds.setDrivenKeyframe( shader+".outColorR", cd=curveInfoNode+'.arcLength', dv= length, v=0 )
    cmds.setDrivenKeyframe( shader+".outColorR", cd=curveInfoNode+'.arcLength', dv= length*0.8, v=1 )
    cmds.setDrivenKeyframe( shader+".outColorR", cd=curveInfoNode+'.arcLength', dv= length*1.2, v=1 )






#############################################################################################################


#cmds.select (CurvEnd)

	from CharacterNames import CharacterNames as chn
	from An_Controllers import An_Controllers  as ctrl



	CurvStart =  cmds.ls(sl=True)[0]
	CurvEnd = 'up'+CurvStart[2:]
	contrl = ['page01_CT', 'page02_CT', 'page03_CT', 'page04_CT', 'page05_CT', 'page06_CT', 'page07_CT', 'page08_CT', 'page09_CT', 'page10_CT',
			'page11_CT', 'page12_CT', 'page13_CT', 'page14_CT', 'page15_CT', 'page16_CT', 'page17_CT', 'page18_CT', 'page19_CT', 'page20_CT'] [int(CurvStart[18:])]


	pfx = CurvStart   #.split('_')[0]
	booksSpine = 'bookSpineMid_jnt'


	for vCurve in [CurvStart, CurvEnd]:                                         #### create curveInfo nodes
		curveInfo = cmds.createNode ( 'curveInfo', n=vCurve+'InfoNod')
		cmds.connectAttr (cmds.listRelatives(vCurve, s=True)[0]+'.worldSpace[0]',  curveInfo+'.inputCurve')


	locRoot = cmds.createNode ( 'transform', n=pfx+"rootLoc" )
	cmds.connectAttr (CurvStart+'InfoNod.controlPoints[0]', locRoot+'.translate')
	cmds.orientConstraint(booksSpine, locRoot)  #for non flipping aim constrants


	rigGrp = cmds.group(locRoot, n=pfx+'Rig')
	cmds.addAttr (rigGrp, longName='rigVis', dv=0.0, min=0.0, max=1.0, keyable=True)

	for i in range(1,5):
		locators, AngLocators, distLocators = [],[],[]
		for vCurve in [CurvStart, CurvEnd]:                                      #### criate locators
			loc= cmds.spaceLocator (p=[0, 0, 0], n=CurvStart+'loc'+str(i))[0]
			cmds.connectAttr (vCurve+'InfoNod.controlPoints['+str(i)+']', loc+'.translate')

			locAngl = cmds.spaceLocator (p=[0, 0, 0], n=vCurve+'locAngl'+str(i))[0]
			locDist = cmds.spaceLocator (p=[0, 0, 0], n=vCurve+'locDist'+str(i))[0]

			locators.append(loc)
			AngLocators.append( locAngl)
			distLocators.append( locDist)

			for l in (loc, locAngl, locDist): cmds.setAttr (l+"Shape.localScale", 0.2, 0.2, 0.2,)
			for vChild, vParent in ([locDist, locAngl],[locAngl, locRoot]): cmds.parent(vChild, vParent)
			cmds.setAttr (locAngl+".t", 0, 0, 0)

			cmds.aimConstraint(loc, locAngl, wut="objectrotation", worldUpObject= booksSpine, u=[0,0,1], wu=[0,0,1], )
			cmds.pointConstraint( loc, locDist, mo=False)


			for obj in (loc, locAngl, locDist):
			   cmds.connectAttr (rigGrp+".rigVis", obj+'.v')




		Obj = ctrl(pfx+str(i)+'_CT')
		Obj.makeController( "sphere",  size=0.5 ) # make Controller
		Obj.gropeCT()
		Obj.placeCT (locRoot , "point")
		cmds.connectAttr (contrl+".ControlsVis", Obj.name+'.v')
		Obj.hideAttr(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
		cmds.parent(Obj.oriGrp, locRoot)

		blendMix = cmds.createNode ( 'blendColors', n=pfx+"_MixNod"+str(i))
		cmds.connectAttr (contrl+".open", blendMix+".blender")
		cmds.connectAttr (AngLocators[0]+".rz", blendMix+".color2R")
		cmds.connectAttr (AngLocators[1]+".rz", blendMix+".color1R")

		cmds.connectAttr (distLocators[0]+".tx", blendMix+".color2G")
		cmds.connectAttr (distLocators[1]+".tx", blendMix+".color1G")

		cmds.connectAttr (  blendMix+".outputR", Obj.oriGrp+".rz" )
		cmds.connectAttr (  blendMix+".outputG", Obj.conGrp+".tx" )

	curveName = cmds.curve (n=pfx+'curve', d=3, p=([0, 0, 0], [1, 0, 0],    [2, 0, 0],  [3, 0, 0],  [4, 0, 0] ))   ### need name !!!!!!!!!!!!!
	for i in range(5): #print i
		cmds.select (cl=True)
		cmds.joint (n=pfx+"_jnt"+str(i), p= [i, 0, 0])
	cmds.skinCluster( [pfx+"_jnt"+str(x) for x in  range(5)], curveName, dr=4.5)
	cmds.parent(pfx+"_jnt"+str(0), locRoot)
	for i in range(1,5):
		cmds.parent(pfx+"_jnt"+str(i), pfx+str(i)+'_CT')
	for i in range(5): cmds.setAttr (pfx+"_jnt"+str(i)+".t", 0, 0, 0)
	[pfx+"_jnt"+str(x) for x in  range(5)]



	for obj in [CurvStart, CurvEnd]:
		cmds.connectAttr (rigGrp+".rigVis", obj+'.v')



	'''
	vPlane = cmds.ls(sl=True)[0]
	poz = 1.0
	for i in range(20):
		print poz

		curvePar = cmds.duplicateCurve ( vPlane+".v[1]", ch=1,  rn=0.1,  local=0, n= vPlane+"_crv"+str(i)  )[1]

		cmds.setAttr (curvePar+".isoparmValue", poz)

		poz = poz - 0.0125

	'''




