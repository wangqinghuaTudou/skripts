from maya import cmds

def pvColorShape():

    win = 'pvColorShape_ui'

    if cmds.window(win, exists=True):
        cmds.deleteUI(win)

    cmds.window(win, \
              sizeable=False, \
              width=100, \
              height=100, \
              title='Colors Shape')

    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(numberOfColumns=5, \
                       columnAttach=[1, 'right', 0], \
                       columnWidth=[[1, 25], [2, 25], [3, 25], [4, 25], [5, 25]])
    for i in xrange(31):
        index = i + 1
        colRGB = cmds.colorIndex(index, query=True)
        cmds.button(command='pvSetColorCtrlMain(%s)'%index, label='', backgroundColor=[colRGB[0], colRGB[1], colRGB[2]])

    cmds.showWindow(win)

def pvSetColorCtrlMain (index):
    sel = cmds.ls(selection=True)
    for each in sel:
        shapes = cmds.listRelatives(each, shapes=True, fullPath=True)
        if shapes:
            for sh in shapes:
                    cmds.setAttr('%s.overrideEnabled'%sh, 1)
                    cmds.setAttr('%s.overrideRGBColors'%sh, 1)
                    cmds.setAttr('%s.overrideColor'%sh, index)

#pvColorShape()