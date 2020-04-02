"""
Main Procedure:
    an_bshTransfer()

Creation Date:
    February 25, 2014

Authors:
    Belyaev Andrey
    andreikin@mail.ru
    www.3drigging.com

Description:
    The script allows you to copy blendShape deformer from one object to another, if the topology is similar.
    When copying, a program disables all the deformers and clusters, but you can turn them off manually.

Installation:

    1. Copy the [an_bshTransfer] to your local user/scripts folder
		 		example: ..\my documents\maya\scripts\
	2. Start Maya
	4. Type:    import an_bshTransfer
                from an_bshTransfer import *
	   into the Maya Script Editor (Pithon mod), and hit enter.

How to Use:
    1. Select the object from which copy blendsheyp.
    2. Select the object to which a copy blendsheyp
    3. Specify a prefix for the generated blend
    4. If the history of the object is large, it is better to manually turn off the effects of all deformers, except copied blendShape "
    5. Press the 'Transfer blandShape'

Notes:
    **** Both objects must be located at a single point (as in the script used 'wrap' deformer).


Comments or suggestions? E-mail me!!!
Good luck!!!


*************************************************************************************************************************
 version History
*************************************************************************************************************************
	v2.0
	- Add script description.
	- Added ability to specify a prefix blend.
	- Added procedure disables all deformers.

*************************************************************************************************************************
 Modify at your own risk
"""



import maya.cmds as cmds
import maya.mel as mm

def an_bshTransfer():                                                                                  # user interface
    vWin = "an_bshTransferWin"
    if cmds.window (vWin, exists=True): cmds.deleteUI ( vWin, window=True )
    cmds.window  (vWin, t="BlendShape Transfer  v 2.00", menuBar=True, sizeable=False, wh= [432, 136]  )
    cmds.menu (label="Help"  )
    cmds.menuItem( label='About script', c= 'an_bshTransferhelp("open")')
    cmds.columnLayout()
    cmds.frameLayout( label='Additional tools:', borderStyle='etchedOut', lv=False)
    cmds.separator   (  style = "none" )
    cmds.text ("   Select the object with a blendShapes, then object which you want to transfer it.", align= 'left')
    cmds.textFieldGrp("pfxTFG", label='Prefix for blandShape targets:  ', columnWidth2 = [260, 156] )
    cmds.checkBoxGrp("turnHistCBG", numberOfCheckBoxes=1, label='Turn off all deformers manually:  ', label1='  ', columnWidth2 = [260, 100]  )
    cmds.separator   (h=1, style = "none" )
    cmds.setParent( '..' )
    cmds.button( label='Transfer blandShape', command= "an_doTransfer()", w=427 )
    cmds.separator   (h=3, style = "none" )
    cmds.text ("   The script allows you to copy blendShap from one object to another with (similar")
    cmds.text ("   topology). When copying, a program disable all the deformers and clusters, ")
    cmds.text ("   but you can turn them off manually")
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 350), (2, 50)] )
    cmds.text ( "                www.3drigging.com   Belyaev Andrey" )
    cmds.button( label='Close',  w= 50, c= 'an_bshTransferhelp("v_action")' )
    cmds.showWindow(vWin)

def an_bshTransferhelp(v_action):
    vWin = "an_bshTransferWin"                        # procedure shows or hides the description of the script
    if v_action == "open": cmds.window  (vWin,   e=True,   wh= [432, 210])
    else: cmds.window  (vWin,   e=True,   wh= [432, 136])

def an_bshInfo (v_bsh): # Get the Attr name, the presence of the connection, source connection, value
    #v_bshAttr = cmds.blendShape (v_bsh, q=True, t=True)
    v_bshAttr = cmds.aliasAttr (v_bsh, q=True)[::2]
    v_output = []
    if v_bshAttr:
        for v_eachAttr in v_bshAttr:
            v_attrOut  = [v_eachAttr,
                cmds.connectionInfo(v_bsh+"."+v_eachAttr, isDestination=True),
                cmds.connectionInfo(v_bsh+"."+v_eachAttr, sourceFromDestination=True),
                cmds.getAttr (v_bsh+"."+v_eachAttr) ]
            v_output.append(v_attrOut)
    return v_output

def an_defSwicher (v_obj, v_turnOff): #turnOn/turnOff envelope of all deformers
    v_hist = cmds.listHistory (v_obj, pdo=1)
    if v_hist:
        for v_each in v_hist:
            if any (v_type == cmds.nodeType(v_each) for v_type in ['nonLinear', 'skinCluster', 'tweak', 'wrap' ]):
                if v_turnOff: cmds.setAttr (v_each+'.envelope', 0)
                else:         cmds.setAttr (v_each+'.envelope', 1)

def an_doTransfer():
    # 1 Get the Attr name, the presence of the connection, source connection, value
    v_source, v_target  = cmds.ls(sl=True)
    if cmds.checkBoxGrp("turnHistCBG", q=True, v1 = True  ):
        for v_each in [v_source, v_target] : an_defSwicher (v_each, True)
    v_hist = cmds.listHistory (v_source, pdo=1)
    if v_hist:  v_bsSrc = cmds.ls (v_hist, type='blendShape')[0] #bland node
    v_bShData = an_bshInfo (v_bsSrc)
    # 2 Disconnect attribut and set 0 value
    for v_eachAttr in v_bShData:
        if v_eachAttr[1]:
            cmds.disconnectAttr(v_eachAttr[2], v_bsSrc+"."+v_eachAttr[0])
        cmds.setAttr  (v_bsSrc+"."+v_eachAttr[0], 0)
    # 3 Make Wrap Node
    cmds.select (v_target, v_source, r=True )
    wrapTemp = mm.eval("doWrapArgList \"6\" { \"1\",\"0\",\" 0.001\", \"2\", \"0\", \"0\", \"0\" };")
    mm.eval ("setAttr (\""+wrapTemp[0]+".maxDistance\") 0.001 ;")
    # 4 Mace blands copy and new blandShape node
    v_blCopy = []
    v_pfx = cmds.textFieldGrp("pfxTFG", q=True, text = True )+"_" if cmds.textFieldGrp("pfxTFG", q=True, text = True ) else "copy_"
    for v_eachAttr in v_bShData:
        cmds.setAttr (v_bsSrc+"."+v_eachAttr[0], 1)
        cmds.duplicate (v_target, n=v_pfx+v_eachAttr[0])
        v_blCopy.append(v_pfx+v_eachAttr[0])
        cmds.setAttr (v_bsSrc+"."+v_eachAttr[0], 0)
    v_newBsh = cmds.blendShape (v_blCopy, v_target)[0]
    # 5 Delete Wrap node, make connection, set value
    cmds.delete   (v_source+'Base', wrapTemp)

    for v_eachAttr in v_bShData:
        cmds.setAttr  (v_bsSrc+"."+v_eachAttr[0], v_eachAttr[3])
        cmds.setAttr  (v_newBsh+"."+v_pfx+v_eachAttr[0], v_eachAttr[3])
        if v_eachAttr[1]:
            cmds.connectAttr(v_eachAttr[2], v_bsSrc+"."+v_eachAttr[0])
            cmds.connectAttr(v_eachAttr[2], v_newBsh+"."+v_pfx+v_eachAttr[0])

    if cmds.checkBoxGrp("turnHistCBG", q=True, v1 = True  ):
        for v_each in [v_source, v_target] : an_defSwicher (v_each, False)
















































