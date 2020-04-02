import maya.cmds as mc

def pvParentShapes ():

    win = 'pvParentShapes_ui'

    if mc.window(win, exists=True):
        mc.deleteUI(win)

    mc.window(win, resizeToFitChildren=True, title='Parent Shapes')
    mc.columnLayout(adjustableColumn=True)

    mc.text('Select Main Shape then Others', align='center')
    mc.separator(height=5, style='out')
    mc.button(label='Parent', command='pvParentShapesMain()')    

    mc.showWindow(win)

def pvParentShapesMain ():

    sel = mc.ls(selection=True)
    parent = sel.pop(0)

    for each in sel:
            mc.makeIdentity(each, apply=True, translate=True, rotate=True, scale=True, normal=False)
            shape = mc.listRelatives(each, fullPath=True, shapes=True)
            mc.parent(shape, parent, relative=True, shape=True)
            mc.delete(each)

    mc.select(clear=True)