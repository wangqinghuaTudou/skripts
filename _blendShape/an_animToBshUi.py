import maya.mel as mm
import maya.cmds as cmds

SFX='animToBsh'

def anim_to_bsh(geo, start, end, del_blds=True, dbl = True):
    mm.eval("currentTime {} ; ".format(start)) 
    geoDbl = cmds.duplicate(geo)[0] if dbl else geo 
    targs=[]
    for _ in xrange( start, end+1):
        targs.append(cmds.duplicate(geo)[0])
        mm.eval("playButtonStepForward; ") 
    targs.append(geoDbl)
    mm.eval("currentTime {} ; ".format(start)) 
    vBsh = cmds.blendShape (targs[1:],  inBetween=True)
    if del_blds:
        cmds.delete(targs[:-1])

def anim_to_bsh_for_sel():
    start = int(cmds.textFieldGrp(SFX+"f1", q=1, text=1))
    end = int(cmds.textFieldGrp(SFX+"f2", q=1, text=1))
    del_blds = cmds.checkBoxGrp(SFX+"ch1", numberOfCheckBoxes=1, q=1,  v1=1  )
    make_dbl =  cmds.checkBoxGrp(SFX+"ch2", q=1, v1=1  ) 
    for geo in cmds.ls(sl=True): 
        anim_to_bsh(geo, start, end, del_blds, make_dbl)

def an_animToBshUi():
    WIDTH =220
    win = SFX+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t='', width=WIDTH,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout (SFX+"ColumnL", adjustableColumn=True)
    cmds.frameLayout (  label="Convert animation to blandShape"   , cll=0, w=WIDTH , bgc=[0,0,0], borderVisible=True)
    def_mid_val = int(cmds.playbackOptions(q=True,  min=True))
    def_max_val = int(cmds.playbackOptions(q=True,  max=True))
    cmds.textFieldGrp(SFX+"f1", label='Start frame:   ', text=def_mid_val, columnWidth2=[100, 118] )
    cmds.textFieldGrp(SFX+"f2", label='End frame:   ', text=def_max_val, columnWidth2=[100, 118] )
    cmds.checkBoxGrp(SFX+"ch1", numberOfCheckBoxes=1, label='Delete blands     ',  columnWidth2=[110, 108] ,v1=1  )
    cmds.checkBoxGrp(SFX+"ch2", numberOfCheckBoxes=1, label='Duplicate geo     ',  columnWidth2=[110, 108] ,v1=1  )
    cmds.button(  l="Convert", c="anim_to_bsh_for_sel()", w=200  )
    cmds.showWindow (win)

 