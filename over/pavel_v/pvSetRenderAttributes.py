import maya.cmds as cmds
import maya.OpenMaya as om


def pvSetRenderAttributes(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        args = cmds.ls(type='mesh', noIntermediate=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any "mesh" object(s).')
        return False

    om.MGlobal.displayInfo('---------------------------------------------------------')
    om.MGlobal.displayInfo('Info: Start to set "render attributes" on "mesh" objects.')

    renderAttributesList = ['.castsShadows', \
                            '.receiveShadows', \
                            '.motionBlur', \
                            '.primaryVisibility', \
                            '.smoothShading', \
                            '.visibleInReflections', \
                            '.visibleInRefractions', \
                            '.motionBlur']

    for msh in args:
        shapes_list = cmds.listRelatives(msh, shapes=True, noIntermediate=True)
        if shapes_list:
            for shp in shapes_list:
                for rna in renderAttributesList:
                    try:
                        cmds.setAttr(shp + rna, 1)
                    except Exception, err:
                        om.MGlobal.displayWarning(err)
        else:
            for rna in renderAttributesList:
                try:
                    cmds.setAttr(msh + rna, 1)
                except Exception, err:
                    om.MGlobal.displayInfo('Info: %s'%err)

    om.MGlobal.displayInfo('Info: Successfuly setted "render attributes" on "mesh" objects.')
    om.MGlobal.displayInfo('---------------------------------------------------------------')

    return True

# pvSetRenderAttributes()