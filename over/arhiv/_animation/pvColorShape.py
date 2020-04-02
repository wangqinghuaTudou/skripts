import maya.cmds as mc

def pvColorShape():

    win = 'pvColorShape_ui'

    if mc.window(win, exists=True):
        mc.deleteUI(win)

    mc.window(win, \
              sizeable=False, \
              width=100, \
              height=100, \
              title='Colors Shape')

    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=5, \
                       columnAttach=[1, 'right', 0], \
                       columnWidth=[[1, 25], [2, 25], [3, 25], [4, 25], [5, 25]])
    for i in xrange(31):
        index = i + 1
        colRGB = mc.colorIndex(index, query=True)
        mc.button(command='pvSetColorCtrlMain(%s)'%index, label='', backgroundColor=[colRGB[0], colRGB[1], colRGB[2]])

    mc.showWindow(win)

def pvSetColorCtrlMain (index):
    sel = mc.ls(selection=True)
    for each in sel:
        shapes = mc.listRelatives(each, shapes=True, fullPath=True)
        if shapes:
            for sh in shapes:
                    mc.setAttr('%s.overrideEnabled'%sh, 1)
                    mc.setAttr('%s.overrideColor'%sh, index)

#pvColorShape()