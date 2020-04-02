import maya.cmds as mc
def guCreateObjectsOnCurve():
	
	win = 'guObjsOnCurve'
	if mc.window(win, exists=True):
	    mc.deleteUI(win)
	win = mc.window(win, title='create objects on curve', \
	                width=300, \
	                height=200, \
	                sizeable=False)
	mc.columnLayout ('guObjsOnCurve', \
	                 width=300, \
	                 height=200, \
	                 adjustableColumn=True)
	mc.frameLayout( label='select curve' )
	mc.columnLayout()
	mc.rowLayout( numberOfColumns=4)
	chekRebuild=mc.checkBox( 'guChekRebuild',label='rebuild curve', align='left', cc='guIntField()')
	mc.intField('guRebuildOptions',value=2,editable=False)
    
	mc.setParent( '..' )
	mc.setParent( '..' )
	
	
	mc.frameLayout( label='object options' )
	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.intFieldGrp('guQualitObj',label='quantity', value1=3)
	mc.rowColumnLayout('guRowLayoutOptObjects', numberOfColumns=2, \
	                   columnAttach=[1, 'right', 10], \
	                   columnWidth=[[1, 100], [2, 150]])
	mc.text('guTextOptionObj', label='set type:', align='right')
	copyMethList = ['joint', \
	                'group', \
	                'lockator']
	mc.optionMenuGrp('guOptMenuGrpEnvironmentObj', columnWidth=[1, 80])
	for item in copyMethList:
		mc.menuItem(label=item)
	mc.setParent( '..' )
	mc.columnLayout()
	mc.rowLayout( numberOfColumns=4)
	chekRebuild=mc.checkBox( 'guChekAim',label='aim Object', align='left', cc='guAimField()')
	mc.textField('guAimOptions',editable=False)
	mc.button('guAimButtn', label='assept' ,bgc=(.26,.26,.26),command='',en=False)
	mc.setParent( '..' )
	mc.setParent( '..' )
	
	bot1=mc.button( label='create' ,bgc=(.0,.270,0.009),command='guCreateObjcts()')
	mc.showWindow(win)

def guAimField():
    if mc.checkBox('guChekAim',q=True,v=True):
    	mc.textField('guAimOptions',editable=True,e=True)
    	mc.button('guAimButtn' ,label='assept' ,bgc=(0.286274509804,0.0392156862745,0.0078431372549),command='guAimAssept()',en=True,e=True)
    else:
        mc.textField('guAimOptions',editable=False,e=True)
        mc.button('guAimButtn' ,label='assept' ,bgc=(.26,.26,.26),command='',en=False,e=True)
def guAimAssept():
    sel=mc.ls(sl=True)[0]
    mc.textField('guAimOptions',tx=sel,editable=True,e=True)
def guIntField():
    rebuildNumb= mc.intField('guRebuildOptions',value=2,editable=mc.checkBox('guChekRebuild',q=True,v=True),e=True)

###################################################################################################################################################
def guCreateObjcts():
    sel=mc.ls(sl=True)
    index=mc.intFieldGrp('guQualitObj', value1=True,q=True)
    poin=float(mc.getAttr(sel[0]+'.mmv.max'))/(index-1)
    start=0
    obj=mc.optionMenuGrp('guOptMenuGrpEnvironmentObj',v=True,q=True)
    aimQer=mc.checkBox('guChekAim',q=True,v=True)
    if mc.checkBox('guChekRebuild',q=True,v=True):
        guRebuildCurve(sel,mc.intField('guRebuildOptions',value=True,q=True))
    for i in xrange(index):
        mc.select(cl=True)
        newObject=guObjQerty(obj,sel[0].replace('_crv','')+str(i))
        mop=guAnimCreate(aimQer,sel[0].replace('_crv','')+str(i))
        mc.setAttr(mop+'.uValue',start)
        start=start+poin
        mc.connectAttr(sel[0]+'.worldSpace',mop+'.geometryPath')
        mc.connectAttr(mop+'.allCoordinates',newObject+'.translate')
        mc.connectAttr(mop+'.rotate',newObject+'.rotate')
def guAnimCreate(aimQer,name):
    if aimQer:
        obj=mc.textField('guAimOptions',tx=True,q=True)
        if not mc.ls(obj):
            mc.error('fail object name for create aim vector')
            mc.warning('press ctrl+z')
        motPath=mc.createNode('motionPath',n=name+'_mop')
        mc.setAttr(motPath+'.worldUpType',1)
        mc.connectAttr(obj+'.worldMatrix[0]',motPath+'.worldUpMatrix')       
    if not aimQer:
        motPath=mc.createNode('motionPath',n=name+'_mop')
    return motPath
            
def guRebuildCurve(sel,sub):
    mc.rebuildCurve(sel, d=3,rt=0,s=sub)
    
    
def guObjQerty(obj,name):
    if obj=='joint':
        new=mc.joint(n=name+'_jnt')
    if obj=='lockator':
        mc.createNode('locator',n=name+'Shape_loc')[0]
        new=mc.rename(mc.listRelatives(name+'Shape_loc',p=True),name+'_loc')
    if obj=='group':
        new=mc.group(n=name+'_grp',em=True,w=True)
    return new
#guCreateObjectsOnCurve()
        