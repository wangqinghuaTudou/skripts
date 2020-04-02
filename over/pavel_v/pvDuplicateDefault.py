import maya.cmds as cmds
import maya.api.OpenMaya as om

def pvDuplicateDefault(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    objects = args
    dupList = []
    attribute_connection_list = {}
    envelope_state_list = {}

    for obj in objects:

        dup_name = 'dup_' + obj
        history = cmds.listHistory(args[0], pruneDagObjects=True)
        if history:
            for hs in history:
                attribute_connection_list[hs] = None
                if cmds.objExists(hs + '.envelope'):
                    state = cmds.getAttr(hs + '.envelope')
                    envelope_state_list[hs] = state
                    attribute_connection = cmds.listConnections(hs + '.envelope', \
                                                                source=True, \
                                                                destination=False, \
                                                                plugs=True, \
                                                                skipConversionNodes=True) 
                    if attribute_connection:
                        attribute_connection_list[hs] = attribute_connection[0]
                        cmds.disconnectAttr(attribute_connection[0], hs + '.envelope')
                    attribute_lock = cmds.setAttr(hs + '.envelope', query=True, lock=False)
                    if attribute_lock:
                        cmds.setAttr(hs + '.envelope', lock=False, keyable=True)
                    cmds.setAttr(hs + '.envelope', 0)
                else:
                    envelope_state_list[hs] = None

        dup = cmds.duplicate(obj, name=dup_name, returnRootsOnly=True)[0]

        for attr in attributes:
            cmds.setAttr('%s.%s' % (dup, attr), lock=False)

        if history:
            for hs in history:
                if cmds.objExists(hs + '.envelope'):
                    state = envelope_state_list[hs]
                    cmds.setAttr(hs + '.envelope', state)
                    attribute_connection = attribute_connection_list[hs]
                    if attribute_connection:
                        cmds.connectAttr(attribute_connection, hs + '.envelope', force=True)
                    attribute_lock = cmds.setAttr(hs + '.envelope', query=True, lock=False)

        shapes = cmds.listRelatives(dup, shapes=True, fullPath=True)
        if shapes:
            for shp in shapes:
                if cmds.getAttr(shp + '.intermediateObject'):
                    cmds.delete(shp)

        constraintsList = cmds.listRelatives(dup, children=True, type='constraint', fullPath=True)
        if constraintsList:
            for const in constraintsList:
                cmds.delete(const)

        dupList.append(dup)

    if dupList:
        cmds.select(dupList, replace=True)

    return dupList

# pvDuplicateDefault()