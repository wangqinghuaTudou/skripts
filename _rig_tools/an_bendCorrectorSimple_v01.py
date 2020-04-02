import maya.cmds as cmds
from CharacterNames import CharacterNames as chn

def an_bendCorrectorSimple_v01():

    win = "simpleCorrectiveSystem"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Simple corrective system v01", width=392,  height=120, s=False, rtf=True, menuBar=True )
    cmds.columnLayout ( adjustableColumn=True)
    cmds.floatSliderGrp('ISG_offset', label='Joint offset:', field=True, min=0.1, max=10,  v=1 , cw = [(1, 124), (2, 50) ], enable= True )
    cmds.textFieldButtonGrp ('TFBG_B', l="Bend joint :   ",  bl=" Add selected",  cw = [(1, 124), (2, 170)],  bc = 'insertText()' )
    bcA = "cmds.textFieldButtonGrp ('TFBG_A', e=True, tx=  cmds.ls (sl=True)[0])"
    cmds.textFieldButtonGrp ('TFBG_A', l="Up joint :   ",  bl=" Add selected",  cw = [(1, 124), (2, 170)],  bc = bcA )
    cmds.textFieldGrp ( 'TFGpfx', label="Prefix :   ", text="",  cw = [(1, 124), (2, 170)])
    cmds.radioButtonGrp('RBGaxis', label='Driver axis :        ', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3, cw = [(1, 140), (2, 80), (3, 80), (4, 80)], sl=3   )
    cmds.separator  (  style="none", h=5)
    cmds.checkBoxGrp('ChBG' ,columnWidth2=[100, 165], numberOfCheckBoxes=1, label='Mirror joint :   ',   v1=True , cw = [(1, 126), (2, 50) ],)
    cmds.separator  (  style="none", h=5)
    cmds.button(l="Make correctiv joint", c= 'doCorrectSys()')#4
    cmds.showWindow()

def insertText():
    bJnt=  cmds.ls (sl=True)[0]
    uJnt= cmds.listRelatives (bJnt, p=True)[0]
    pfx = chn(uJnt).divideName()[0]+chn(uJnt).divideName()[1]
    cmds.textFieldButtonGrp ('TFBG_B', e=True, tx= bJnt)
    cmds.textFieldButtonGrp ('TFBG_A', e=True, tx= uJnt)
    cmds.textFieldGrp ( 'TFGpfx', e=True, tx= pfx)


def doCorrectSys():
    pfx = cmds.textFieldGrp ( 'TFGpfx', q=True, text=True)
    upBaseJnt = cmds.textFieldButtonGrp ('TFBG_A', q=True, text=True )
    rtBaseJnt = cmds.textFieldButtonGrp ('TFBG_B', q=True, text=True )
    axis = '.r'+{1:'x', 2:'y', 3:'z'}[cmds.radioButtonGrp('RBGaxis', q=True, sl=True)]
    offset = cmds.floatSliderGrp('ISG_offset', q=True,   v= True )
    simpleJointSystem(pfx, rtBaseJnt, upBaseJnt, axis, offset)
    if cmds.checkBoxGrp('ChBG' , q=True,  v1=True ):
        rtGrp = simpleJointSystem(pfx.replace('l_', 'r_'), rtBaseJnt.replace('l_', 'r_'), upBaseJnt.replace('l_', 'r_'), axis, offset)


        for attr in ['rtOffsRt', 'trOffsRt']:    cmds.setAttr(rtGrp+'.'+attr,    cmds.getAttr(rtGrp+'.'+attr)*-1.0 )


def simpleJointSystem (pfx, rtBaseJnt, upBaseJnt, axis, offset ):

    cmds.select (cl=True)
    jntUp = cmds.joint( n=pfx+'Up_jnt')
    cmds.select (cl=True)
    jntRt = cmds.joint(n=pfx+'Rt_jnt')

    aimGrp = cmds.group (jntUp, n=pfx+'Aim_gtp')
    rtGrp = cmds.group (aimGrp, jntRt, n=pfx+'rt_gtp')

    cmds.parentConstraint (rtBaseJnt, rtGrp )
    cmds.aimConstraint (upBaseJnt, aimGrp, aim=[1, 0, 0], u=[0, 0, 1], wu=[0, 0, 1], wut = "objectrotation", wuo=jntRt)

    # add offset attr and connection
    MDVOfset = cmds.createNode ('multiplyDivide', n=pfx+'OffsetMDV')
    PMA = cmds.createNode ('plusMinusAverage', n=pfx+'OffsetPMA')


    for i, attr in  enumerate([ 'rtOffsUp', 'trOffsUp', 'rtOffsRt', 'trOffsRt']):
        cmds.addAttr(rtGrp, longName = attr, k=True, dv = 0.05)
        if attr in (  'trOffsUp',  'trOffsRt'): cmds.setAttr(rtGrp+'.'+attr, offset  )

    for coord in  ['X', 'Y']:  cmds.connectAttr (rtBaseJnt +axis, MDVOfset+'.input2' + coord )
    cmds.connectAttr (rtGrp +'.rtOffsUp', MDVOfset+'.input1X')
    cmds.connectAttr (rtGrp +'.rtOffsRt', MDVOfset+'.input1Y')

    cmds.connectAttr (rtGrp +'.trOffsUp', PMA+'.input2D[0].input2Dx')
    cmds.connectAttr (rtGrp +'.trOffsRt', PMA+'.input2D[0].input2Dy')

    cmds.connectAttr (MDVOfset +'.outputX', PMA+'.input2D[1].input2Dx')
    cmds.connectAttr (MDVOfset +'.outputY', PMA+'.input2D[1].input2Dy')

    cmds.connectAttr (PMA+'.output2D.output2Dx', jntUp+'.tx')
    cmds.connectAttr (PMA+'.output2D.output2Dy', jntRt+'.tx')
    return rtGrp












