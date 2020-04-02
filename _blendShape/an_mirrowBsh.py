import maya.mel as mm
import maya.cmds as cmds

def an_mirrowBsh():
    win = "an_corrBsh"
    vWidth = 180
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Mirrow BlandShape tool.v01", rtf=True  )
    vCLayout =cmds.columnLayout()
    cmds.separator(height=5, style='none')
    cmds.text("    Select left (right) target, then \n select base object ")
    cmds.separator(height=5, style='none')
    cmds.text("MaxDistance: ")
    cmds.separator(height=5, style='none')
    cmds.textField("an_mDistTF", w=vWidth, text = "0.001")
    cmds.separator(height=13, style='none')
    cmds.checkBoxGrp("delHiCBG", columnWidth2=[30, 165], numberOfCheckBoxes=1, label='  ', label1='Delete history', v1=True)
    cmds.separator(height=10, style='none')
    cmds.button(w=vWidth, l="Mirrow BlandShape", c="an_doMirrowBsh()"  )
    cmds.showWindow ()



####################################################################################################################

def an_doMirrowBsh():

    vHistory = cmds.checkBoxGrp("delHiCBG", q=True, v1=True)
    vMaxDistance = cmds.textField("an_mDistTF", q=True, text=True)
    do_an_MirrowBlandShape(cmds.ls (sl=True)[1], cmds.ls (sl=True)[0], vHistory, vMaxDistance)

####################################################################################################################

def do_an_MirrowBlandShape(vBaseObj, vBlend, vHistory, vMaxDistance):

    vOppositeBlend = cmds.duplicate   (vBaseObj, n='opozit_'+vBlend)
    cmds.setAttr (vOppositeBlend[0]+".scaleX", -1)
    cmds.delete  (cmds.pointConstraint (vBlend, vOppositeBlend))
    vBsh = cmds.blendShape (vBaseObj, vBlend, w=[(0, 1)])
    cmds.select ( vOppositeBlend, r=True )
    cmds.select ( vBlend, add=True )
    wrapTemp = mm.eval("doWrapArgList \"6\" { \"1\",\"0\",\""+str(vMaxDistance)+"\", \"2\", \"0\", \"0\", \"0\" };")
    mm.eval ("setAttr (\""+wrapTemp[0]+".maxDistance\") "+str(vMaxDistance)+";")
    cmds.setAttr (vBsh[0]+"."+vBaseObj, 0)
    cmds.delete (vBsh)

    if (vHistory):
        cmds.delete   (vOppositeBlend,  ch=True)
        cmds.delete   (vBlend+'Base')
        cmds.setAttr (vOppositeBlend[0]+".scaleX", 1)
        vTXval = cmds.getAttr  (vBlend+'.tx')
        cmds.setAttr (vOppositeBlend[0]+".tx", vTXval*-1)
    else:
        vBsh = cmds.blendShape (vOppositeBlend, vBlend, vBaseObj, w=[(0, 1), (1, 1)])
        cmds.setAttr (vOppositeBlend[0] +".v", 0)

