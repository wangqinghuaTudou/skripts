import maya.cmds as mc
import maya.OpenMaya as om


def pvListChildrenExactType(*args):

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    listTransform = mc.listRelatives(parent, allDescendents=True, f=True)
    if chType=='transform':
        listChType = [trans for trans in listTransform if mc.nodeType(trans)=='transform']
        return listChType
    elif chType=='joint':
        listChType = [trans for trans in listTransform if mc.nodeType(trans)=='joint']
        return listChType
    elif chType=='cluster':
        listChType = [trans for trans in listTransform if mc.listRelatives(trans, c=True, shapes=True, type='clusterHandle')]
        return listChType
    elif chType=='group':
        listChType = [trans for trans in listTransform if not mc.listRelatives(trans, c=True, shapes=True)]
        return listChType
    elif chType=='bind':
        listChType = [trans for trans in listTransform if '_bind' in trans]
        return listChType
    elif chType=='jnt':
        listChType = [trans for trans in listTransform if '_jnt' in trans]
        return listChType
    elif chType=='geo':
        listChType = [trans for trans in listTransform if mc.listRelatives(trans, c=True, shapes=True, type='mesh')]
        return listChType
    else:
        listChType = [trans for trans in listTransform if mc.listRelatives(trans, c=True, shapes=True, type=chType)]
        return listChType