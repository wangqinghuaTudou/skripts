from An_Controllers import An_Controllers  as ctrl

def an_bookRig_v01():
    win = "bookRigUI"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Book rig system v0.01", width=420,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout ('columnLayoutName', adjustableColumn=True)
    #step 1
    cmds.frameLayout (label="Step 1", borderStyle="etchedIn", cll=1, w=424, bgc= [0, 0, 0])
    cmds.columnLayout
    cmds.separator  (  style="none")
    cmds.text (l="         Creating a bounding box for book system ", al="left", font= "boldLabelFont")
    cmds.textFieldGrp ('TFG_pfx', l="System preffix:",  cw = [(1, 124), (2, 191)])
    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)])
    cmds.text (l="")
    cmds.button   (l="Make bounding box",   c="an_makeBoundingBox()" )
    cmds.setParent ('columnLayoutName')
    cmds.separator  (  style="none")
    #step 2
    cmds.frameLayout (label="Step 2", borderStyle="etchedIn", cll=1, w=424, bgc= [0, 0, 0])
    cmds.columnLayout
    cmds.separator  (  style="none")
    cmds.text (l="         Setup books size and creation rig", al="left", font= "boldLabelFont")
    cmds.text (l="     - Using a bounding box, specify the size of the book", al="left")
    cmds.text (l="     - Specify the number of pages ", al="left")
    cmds.text (l="     - To making rig system, press \"Make rig\"", al="left")
    cmds.intSliderGrp('ISG_pagesNum', label='Number of pages:', field=True, min=0, max=100,  v=10 , cw = [(1, 124), (2, 50) ], enable= True )
    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)])
    cmds.text (l="")
    cmds.button   (l= "Make book rig", c='Make rig()' )
    cmds.setParent ('columnLayoutName')
    cmds.showWindow (win)



def an_makeBoundingBox():
    pfx = cmds.textFieldGrp ('TFG_pfx', q=True,  text = True)
    cmds.curve (d=1, n=pfx+'BoundingBox',   p=([3, 0.5, -4.5], [3, 0.5, 4.5], [3, -0.5, 4.5], [3, 0.5, 4.5], [-3, 0.5, 4.5],
    [-3, -0.5, 4.5], [-3, 0.5, 4.5], [-3, 0.5, -4.5], [-3, -0.5, -4.5], [-3, 0.5, -4.5], [3, 0.5, -4.5], [3, -0.5, -4.5],
    [3, -0.5, 4.5], [-3, -0.5, 4.5], [-3, -0.5, -4.5], [3, -0.5, -4.5]))

def midPoint(iList = ['2', '11']):
    pos1 = cmds.xform(boundingBox+'.cv['+iList[0]+']', q=True, t=True, ws=True)
    pos2 = cmds.xform(boundingBox+'.cv['+iList[1]+']', q=True, t=True, ws=True)
    return [(pos1[0]+pos2[0])/2, (pos1[1]+pos2[1])/2, (pos1[2]+pos2[2])/2]



def an_makeBookRig():

	pfx = cmds.textFieldGrp ('TFG_pfx', q=True,  text = True)
	boundingBox = pfx+'BoundingBox'



	ctCoord = []   #controller
	for i in ['1', '4', '7', '0', '1']:  ctCoord.append( cmds.xform(boundingBox+'.cv['+i+']', q=True, t=True, ws=True) )
	for i in ctCoord: i[1]=0

	cmds.curve (d=1, n=pfx+'book_CT', p=ctCoord)
	ct=ctrl(pfx+'book_CT')
	ct.addColor()
	ct.gropeCT()

	for attr in ( 'faceOpen', 'bottomOpen'): cmds.addAttr   ( ct.name, ln=attr,  keyable=True)



	cmds.select(cl=True)   #base joints
	jntBase=[]
	for num, i in enumerate((['2', '11'], ['5', '8'], ['4', '7'], ['1', '0'])):
		jntBase.append(pfx+'base'+str(num)+'_jnt')
		cmds.joint (n=jntBase[num],  p=midPoint(i))

	jntGrp=cmds.group(jntBase[0], n=pfx+'joint_grp')
	cmds.parent(jntGrp, ct.name)












