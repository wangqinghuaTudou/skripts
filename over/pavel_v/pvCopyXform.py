import maya.cmds as mc

def pvCopyXform():

    if (mc.window('pvCopyXform_ui', exists=True)):
        mc.deleteUI('pvCopyXform_ui')

    mc.window('pvCopyXform_ui', \
              resizeToFitChildren=True, \
              sizeable=False, \
              title='Copy Xform')

    mc.columnLayout(adjustableColumn=True)
    mc.text('<< Select Two Objects >>', align='center')

    mc.separator (height=5, style='out')
    mc.checkBox('pvCopyTxCheckBox', value=1, label='TranslateX', align='left')
    mc.separator(height=5, style='in')
    mc.checkBox('pvCopyTyCheckBox', value=1, label='TranslateY', align='left')
    mc.separator(height=5, style='in')
    mc.checkBox('pvCopyTzCheckBox', value=1, label='TranslateZ', align='left')
    mc.separator(height=5, style='in')
    mc.checkBox('pvCopyRxCheckBox', value=1, label='RotateX', align='left')
    mc.separator(height=5, style='in')
    mc.checkBox('pvCopyRyCheckBox', value=1, label='RotateY', align='left')
    mc.separator(height=5, style='in')
    mc.checkBox('pvCopyRzCheckBox', value=1, label='RotateZ', align='left')
    mc.button(label='Copy', command='pvCopyXformMain ()')

    mc.showWindow('pvCopyXform_ui')

def pvCopyXformMain ():

    objectList = mc.ls(selection=True)
    if len(objectList) != 2:
        mc.warning ('pvMakeCtrl :: Must be selected two objects.')
        return
    else:
        source, destination = objectList
        translateSource = mc.xform(source, query=True, worldSpace=True, translation=True)
        rotateSource = mc.xform(source, query=True, worldSpace=True, rotation=True)
        translateDestination = mc.xform(destination, query=True, worldSpace=True, translation=True)
        rotateDestination = mc.xform(destination, query=True, worldSpace=True, rotation=True)

        if mc.checkBox('pvCopyTxCheckBox', query=True, value=True):
            tx = translateSource[0]
        else:
            tx = translateDestination[0]
        if mc.checkBox('pvCopyTyCheckBox', query=True, value=True):
            ty = translateSource[1]
        else:
            ty = translateDestination[1]
        if mc.checkBox('pvCopyTzCheckBox', query=True, value=True):
            tz = translateSource[2]
        else:
            tz = translateDestination[2]

        if mc.checkBox('pvCopyRxCheckBox', query=True, value=True):
            rx = rotateSource[0]
        else:
            rx = rotateDestination[0]
        if mc.checkBox('pvCopyRyCheckBox', query=True, value=True):
            ry = rotateSource[1]
        else:
            ry = rotateDestination[1]
        if mc.checkBox('pvCopyRzCheckBox', query=True, value=True):
            rz = rotateSource[2]
        else:
            rz = rotateDestination[2]

        mc.xform(destination, worldSpace=True, translation=[tx, ty, tz])
        mc.xform(destination, worldSpace=True, rotation=[rx, ry, rz])

# pvCopyXform()