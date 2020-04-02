import maya.cmds as mc
import maya.OpenMaya as om


def pvDuplicateAttributes(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be two objects.')
        return
    if len(args) != 2:
        om.MGlobal.displayWarning('Must be specified only two objects.')
        return

    source, dest = args

    attributesList = mc.listAttr(source, keyable=True)
    if attributesList:
        for attr in attributesList:
            attrType = mc.attributeQuery(attr, node=source, attributeType=True)
            if not mc.objExists('%s.%s'%(dest, attr)):
                if attrType != 'compound':
                    mc.addAttr(dest, longName=attr, attributeType=attrType, keyable=True)
                    try:
                        value = mc.getAttr('%s.%s'%(source, attr))
                        mc.setAttr('%s.%s'%(dest, attr), value)
                        mc.connectAttr('%s.%s'%(dest, attr), '%s.%s'%(source, attr), force=True)
                    except RuntimeError:
                        om.MGlobal.displayInfo('"%s.%s" is already connected to "%s.%s".'%(dest, attr, dest, attr))
                else:
                    pass
                    #mc.addAttr(dest, longName=attr, attributeType=attrType, keyable=True)

# pvDuplicateAttributes()
