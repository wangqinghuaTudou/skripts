import maya.cmds as cmds

def an_corectivBshTool():
    win = "an_corrBsh"
    vWidth = 180
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Corrective bsh tool.v01", rtf=True  )
    vCLayout =cmds.columnLayout()

    cmds.frameLayout( label='Step 1:', borderStyle='etchedOut', bgc= [0, 0, 0])
    cmds.text("  Enter the skinned object for which\n you want to make a correction form")
    cmds.columnLayout( )
    cmds.textField("an_baseGeoTF", w=vWidth)
    cmds.button(w=vWidth, l="Add geometry", c= "cmds.textField (\"an_baseGeoTF\", e=True, text= cmds.ls (sl=True)[0])")
    cmds.setParent( vCLayout)
    cmds.separator(height=20, style='none')

    cmds.frameLayout( label='Step 2:', borderStyle='etchedOut', bgc= [0, 0, 0] )
    cmds.columnLayout( )
    cmds.text("  Deform skinned object to the  \n    desired form and generate the\n blank for bsh")
    cmds.button(w=vWidth, l="Generate blank", c="an_makeBlank()" )
    cmds.setParent( vCLayout)
    cmds.separator(height=20, style='none')

    cmds.frameLayout( label='Step 3:', borderStyle='etchedOut' , bgc= [0, 0, 0])
    cmds.columnLayout( )
    cmds.text("  Deform blank to the desired form\n and generate corrective bsh")
    cmds.textField("an_blankGeoTF", w=vWidth)
    cmds.button(w=vWidth, l="Add geometry blank",  c= "cmds.textField (\"an_blankGeoTF\", e=True, text= cmds.ls (sl=True)[0])")
    cmds.separator(height=5, style='none')
    cmds.checkBoxGrp("delBlCBG", columnWidth2=[30, 165], numberOfCheckBoxes=1, label='    ', label1='Delete blank', v1=True)
    cmds.separator(height=5, style='none')
    cmds.button(w=vWidth, l="Generate corrective bsh", c="an_makeCorrectiveBsh()"  )
    cmds.setParent( '..')


    cmds.frameLayout( label='Step 4:', borderStyle='etchedOut', bgc= [0, 0, 0])
    cmds.text("  Enter the bsh node and connect\n  selected geometry  ")
    cmds.columnLayout( )
    cmds.textField("an_bshTF", w=vWidth)
    cmds.button(w=vWidth, l="Add bsh", c= "cmds.textField (\"an_bshTF\", e=True, text= cmds.ls (sl=True)[0])")
    cmds.button(w=vWidth, l="Connect selected to bsh",  c="an_addCorrectiveToBsh()")
    cmds.setParent( vCLayout)
    cmds.showWindow ()

#######################################
def an_addCorrectiveToBsh():
    vBlendShape = cmds.textField ('an_bshTF', q=True, text =True )
    vObj = cmds.textField ('an_baseGeoTF', q=True, text =True )
    cmds.blendShape( vBlendShape, edit=True, t=(vObj, 0, cmds.ls (sl=True)[0], 1.0) )

#######################################
def an_makeCorrectiveBsh():
    vObjBlank = cmds.textField ('an_blankGeoTF', q=True, text =True )
    vObjNegativ = vObjBlank.replace('_blank','_negativ')
    vObj = cmds.textField ('an_baseGeoTF', q=True, text =True )
    vList =  cmds.listHistory (vObj, pdo=True)
    skinClaster =  cmds.ls (vList, type="skinCluster") [0]
    vBlend = cmds.blendShape(vObjNegativ, vObjBlank, vObj, foc=True, tc=True, w=[(0, -1.0), (1, 1.0)])[0]
    cmds.setAttr (skinClaster+".envelope", 0)

    vDup = cmds.duplicate(vObj, name= vObj+'_corrective'  , rr=True )[0]
    for vEach in ['tx', "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]:  cmds.setAttr (vDup+"."+vEach, lock=False )
    cmds.setAttr (skinClaster+".envelope", 1)
    cmds.delete (vBlend)

    vDupShape = cmds.listRelatives(vDup,s=1)
    vXSize = ((cmds.getAttr (vDupShape[0]+".boundingBoxMaxX"))- (cmds.getAttr (vDupShape[0]+".boundingBoxMinX")))*2
    cmds.setAttr (vDup+".tx", vXSize)
    if cmds.checkBoxGrp("delBlCBG",q=True, v1=True):
        cmds.delete (vObjNegativ, vObjBlank)

#######################################
def an_makeBlank():
    vObj = cmds.textField ('an_baseGeoTF', q=True, text =True )
    vDup = cmds.duplicate(vObj, name= vObj+'_blank'  , rr=True )[0]
    for vEach in ['tx', "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]:  cmds.setAttr (vDup+"."+vEach, lock=False )

    vCopy = cmds.duplicate(vDup, name= vObj+'_negativ'  , rr=True ) [0]
    cmds.setAttr (vCopy+".v", 0)

    vDupShape = cmds.listRelatives(vDup,s=1)
    vXSize = (cmds.getAttr (vDupShape[0]+".boundingBoxMaxX"))- (cmds.getAttr (vDupShape[0]+".boundingBoxMinX"))
    cmds.setAttr (vDup+".tx", vXSize)
    cmds.select (vDup)
    cmds.textField ("an_blankGeoTF", e=True, text= cmds.ls (sl=True)[0])

