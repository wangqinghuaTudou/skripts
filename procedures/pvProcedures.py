import maya.cmds as cmds
import maya.api.OpenMaya as om


#### set 
def pvSetDrawingOverride(state):
    if state not in (0, 1):
        om.MGlobal.displayWarning('The argument must be 0 or 1.')
        return
    else:
        for each in cmds.ls(sl=True):
            eachSh = cmds.listRelatives(each, shapes=True)
            if eachSh:
                for e in eachSh:
                    cmds.setAttr('%s.overrideEnabled'%e, state)
            cmds.setAttr('%s.overrideEnabled'%each, state)


#### return namespace if exists 'root' group
def pvGetNameSpaces():
    roots = cmds.ls('*root')
    nsRoots = cmds.ls('*:root')
    if not roots and not nsRoots:
        om.MGlobal.displayInfo('"root" group(s) doesn\'t exists.')
        return
    
    nsList = []
    rootsList = []

    if roots and nsRoots:
        rootsList = roots + nsRoots
    elif roots and not nsRoots:
        rootsList = roots
    elif not roots and nsRoots:
        rootsList = nsRoots

    for each in rootsList:
        if ':' in each:
            nsParts = each.split(':')
            ns = ''
            for i in range(len(nsParts) - 1):
                ns = ns + nsParts[i] + ':'
        elif '_' in each:
            nsParts = each.split('_')
            ns = ''
            for i in range(len(nsParts) - 1):
                ns = ns + nsParts[i] + '_'
        else:
            ns = ''

        nsList.append(ns)

    return nsList


#### list children exact type for any object
def pvListChildrenExactType(parent, chType):

    listTransform = cmds.listRelatives(parent, allDescendents=True, f=True)

    if chType=='transform':
        listChType = [trans for trans in listTransform if cmds.nodeType(trans)=='transform']
        return listChType
    elif chType=='joint':
        listChType = [trans for trans in listTransform if cmds.nodeType(trans)=='joint']
        return listChType
    elif chType=='cluster':
        listChType = [trans for trans in listTransform if cmds.listRelatives(trans, c=True, shapes=True, type='clusterHandle')]
        return listChType
    elif chType=='group':
        listChType = [trans for trans in listTransform if not cmds.listRelatives(trans, c=True, shapes=True)]
        return listChType
    elif chType=='bind':
        listChType = [trans for trans in listTransform if '_bind' in trans]
        return listChType
    elif chType=='jnt':
        listChType = [trans for trans in listTransform if '_jnt' in trans]
        return listChType
    elif chType=='geo':
        listChType = [trans for trans in listTransform if cmds.listRelatives(trans, c=True, shapes=True, type='mesh')]
        return listChType
    else:
        listChType = [trans for trans in listTransform if cmds.listRelatives(trans, c=True, shapes=True, type=chType)]
        return listChType


#### set display override on list of objects by the state argument
def pvDrawOverrideState(objList, state):
    for obj in objList:
        chnl = '%s.overrideEnabled'%obj
        chnlDraw = '%s.drawOverride'%obj
        if pvCheckLockConn(chnl) and pvCheckLockConn(chnlDraw):
            cmds.setAttr(chnl, state)
        shapes = cmds.listRelatives(obj, c=True, shapes=True)
        if shapes:
            for shp in shapes:
                chnl = '%s.overrideEnabled'%shp
                chnlDraw = '%s.drawOverride'%shp
                if pvCheckLockConn(chnl) and pvCheckLockConn(chnlDraw):
                    cmds.setAttr(chnl, state)

#### check channel for lock and conected
def pvCheckLockConn(chnl):
    lock = cmds.getAttr(chnl, l=True)
    conn = cmds.listConnections(chnl, source=True, destination=False)
    if not lock and not conn:
        return True
    else:
        return False

#### select all objects exact type in scene
def pvListAllObjType(objType):
    listTransform = cmds.ls(type='transform')
    if objType=='transform':
        return listTransform
    else:
        listAllType = [trans for trans in listTransform if cmds.listRelatives(trans, c=True, shapes=True, type=objType)]
        return listAllType

#### set display Handle attribute is off on the list of objects
def pvHandleOff(objList):
    for obj in objList:
        chnl = '%s.displayHandle'%obj
        if pvCheckLockConn(chnl):
            cmds.setAttr(chnl, 0)

#### return list of deformers on object
def pvListDeformers(obj):
    hist = cmds.listHistory(obj, pruneDagObjects=True)
    if hist:
        skinSrc = cmds.ls(hist, type='skinCluster')
        bsSrc = cmds.ls(hist, type='blendShape')
        clstrSrc = cmds.ls(hist, type='cluster')
        skinList = [deform for deform in skinSrc if skinSrc]
        bsList = [deform for deform in bsSrc if bsSrc]
        clstrList = [deform for deform in clstrSrc if clstrSrc]
        return skinList, bsList, clstrList

#### return two lists of joints and nurbs influences binded to the skin on selected object
def pvListBindedJoints(obj):
    skin = cmds.ls(cmds.listHistory(obj, pruneDagObjects=1), type='skinCluster')[0]
    if skin:
        infls = cmds.skinCluster(skin, query=True, weightedInfluence=True)
        jnts = cmds.ls(infls, type='joint')
        nurbs = list(set(infls).difference(jnts))
        return jnts, nurbs

#### clear reference nodes and namespaces in scene
def pvClearRefNs():
    for each in cmds.ls(type='reference'):
        om.MGlobal.displayInfo('Deleted reference node - %s'%each)
        cmds.lockNode(each, l=0)
        cmds.delete(each)
    for each in cmds.namespaceInfo(lon=True):
        if ('UI' not in each) and ('shared' not in each):
            cmds.namespace(each, mnr=True, rm=True)
            om.MGlobal.displayInfo('Deleted namespace - %s'%each)

#### move curve's pivot point to start CV
def pvMovePivotToStartCV(curveName):
    cvStart = cmds.pointPosition('%s.cp[0]'%curveName, l=True)
    cmds.move(cvStart[0], cvStart[1], cvStart[2], '%s.scalePivot'%curveName, '%s.rotatePivot'%curveName)

#### getting skinCluster name on selected object
def pvGetSkinCluster(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object.')
        return
    if len(args) > 1: # check the count of selected objects
        om.MGlobal.displayWarning('Must be specified only one object.')
        return
    hist = cmds.listHistory(args[0], pruneDagObjects=True) # try to find history on the destination object
    if not hist: 
        om.MGlobal.displayWarning('Object "%s" has no history.'%args)
        return
    skinCl = cmds.ls(hist, type='skinCluster') # try to find skinCluster on the destination object
    if not skinCl:
        om.MGlobal.displayWarning('Object "%s" has no "skinCluster".'%args)
        return
    om.MGlobal.displayInfo('Object: "%s" has skinCluster: %s'%(args[0], skinCl[0]))
    return skinCl[0]

#### remove unused influences in skinCluster
def pvRemoveUnusedInfl(*args):
    if not args:
        sel = cmds.ls(selection=True)
        args = pvGetSkinCluster(sel)
    if not args:
        om.MGlobal.displayWarning('Must be specified any "skinCluster".')
        return
    if len(args) != 1: # check the count of selected objects
        om.MGlobal.displayWarning('Must be specified only one "skinCluster".')
        return

    destSkin = args[0]
    influences = cmds.skinCluster(destSkin, query=True, influence=True) # getting full list of influences
    weightedInfl = cmds.skinCluster(destSkin, query=True, weightedInfluence=True) # getting only weighted influences list
    removeInfl = list(set(influences) - set(weightedInfl)) # getting list with zero weights
    if removeInfl:
        cmds.skinCluster(destSkin, edit=True, removeInfluence=removeInfl) # remove influences with zero weights from destination skinCluster
        om.MGlobal.displayInfo('Removed unused influences: %s'%removeInfl)
    else:
        om.MGlobal.displayInfo('SkinCluster has no unused influences.')

def pvMatchInfluences(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified two objects.')
        return
    if len(args) != 2: # check the count of selected objects
        om.MGlobal.displayWarning('Must be specified only two objects.')
        return

    source, dest = args
    sourceSkin = pvGetSkinCluster(source)
    destSkin = pvGetSkinCluster(dest)
    sourceInfl = cmds.skinCluster(sourceSkin, query=True, influence=True)
    destInfl = cmds.skinCluster(destSkin, query=True, influence=True)
    sourceDif = list(set(destInfl) - set(sourceInfl))
    destDif = list(set(sourceInfl) - set(destInfl))
    matchInfl = sourceInfl + sourceDif

    if sourceDif:
        cmds.skinCluster(sourceSkin, \
                       edit=True, \
                       useGeometry=True, \
                       dropoffRate=4, \
                       polySmoothness=False, \
                       nurbsSamples=25, \
                       lockWeights=True, \
                       weight=0, \
                       addInfluence=sourceDif)

    if destDif:
        cmds.skinCluster(destSkin, \
                       edit=True, \
                       useGeometry=True, \
                       dropoffRate=4, \
                       polySmoothness=False, \
                       nurbsSamples=25, \
                       lockWeights=True, \
                       weight=0, \
                       addInfluence=destDif)

    om.MGlobal.displayInfo('Added influences to both skinClusters: \n%s'%matchInfl)
    return matchInfl

def pvGetSkinInfluences(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object.')
        return
    if len(args) != 1: # check the count of selected objects
        om.MGlobal.displayWarning('Must be specified only one object.')
        return

    skin = pvGetSkinCluster(args)
    skinInfl = cmds.skinCluster(skin, query=True, influence=True)
    om.MGlobal.displayInfo('Matched influences list: \n%s'%skinInfl)
    return skinInfl

def pvSwitchAllInfluences(lock=True, *args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    for each in args:
            infls = pvGetSkinInfluences(each)
            for inf in infls:
                cmds.setAttr('%s.liw'%inf, lock)

def pvRotateToJointOrient(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    for each in args:
        cmds.setAttr('%s.jointOrient'%each, *list(cmds.getAttr('%s.rotate'%each)[0]), type='double3')
        cmds.setAttr('%s.rotate'%each, 0, 0, 0, type='double3')

def pvIsChannelSettable(channel):
    isLocked = cmds.getAttr(channel, lock=True)
    isConnected = cmds.listConnections(channel, source=True, destination=False)
    if cmds.objectType(isConnected) != 'anicmds.rve':
        isConnected = True
    else:
        isConnected = False
    if not isLocked and not isConnected:
        return True
    else:
        return False


#
def pvSnapPivot():
    sel = cmds.ls(selection=True)
    if len(sel) != 2:
        om.MGlobal.displayInfo('Must be selected two objects.')
        return
    source = sel[0]
    dest = sel[1]
    worldPos = cmds.xform(source, query=True, worldSpace=True, translation=True)
    cmds.move(worldPos[0], worldPos[1], worldPos[2], dest + '.scalePivot', dest + '.rotatePivot', worldSpace=True)


# 
def pvUnlockAllAttributes(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    for obj in args:
        for attr in attributes:
            cmds.setAttr(obj + '.' + attr, lock=False, keyable=True)


# 
def pvCreateUpperCTGroups():

    obj = cmds.ls(selection=True)[0]
    ori = obj.replace('_CT', 'CT_ori')
    con = obj.replace('_CT', 'CT_con')
    dup = cmds.duplicate(obj, returnRootsOnly=True, parentOnly=True)[0]

    attributes = cmds.listAttr(dup, userDefined=True)
    if attributes:
        for attr in attributes:
            cmds.deleteAttr(dup, attribute=attr)

    pvUnlockAllAttributes(dup)

    cmds.rename(dup, con)
    dup = cmds.duplicate(con, returnRootsOnly=True)
    cmds.rename(dup, ori)

    cmds.parent(obj, con)
    cmds.parent(con, ori)

    cmds.select(obj, replace=True)

def pvCreateMiddleJoint(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    for jnt in args:
        if '_bind' in jnt:
            dupName = jnt.replace('_bind', 'Middle_bind')
            multName = jnt.replace('_bind', 'RotMult_mdv')
        elif '_jnt' in jnt:
            dupName = jnt.replace('_jnt', 'Middle_bind')
            multName = jnt.replace('_jnt', 'RotMult_mdv')
        else:
            dupName = jnt + 'Middle_bind'
            multName = jnt + 'RotMult_mdv'
        cmds.duplicate(jnt, returnRootsOnly=True, name=dupName)
        dupChildren = cmds.listRelatives(dupName, children=True, fullPath=True)
        if dupChildren:
            cmds.delete(dupChildren)
        cmds.parent(dupName, jnt)
        cmds.createNode('multiplyDivide', name=multName)
        cmds.connectAttr(jnt + '.rotate', multName + '.input1', force=True)
        cmds.setAttr(multName + '.input2X', -0.5)
        cmds.setAttr(multName + '.input2Y', -0.5)
        cmds.setAttr(multName + '.input2Z', -0.5)
        cmds.connectAttr(multName + '.output', dupName + '.rotate', force=True)

    cmds.select(dupName, replace=True)

def pvMirrorObjects(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return
    objects = args
    if objects:
        for obj in objects:
            parent = cmds.listRelatives(obj, parent=True)
            groupName = cmds.group(obj, world=True)
            cmds.xform(groupName, objectSpace=True, pivots=[0, 0, 0])
            cmds.setAttr(groupName + '.sx', -1)
            cmds.makeIdentity(groupName, apply=True, translate=True, rotate=True, scale=True, jointOrient=False)
            if parent:
                cmds.parent(obj, parent[0])
            else:
                cmds.parent(obj, world=True)
            cmds.delete(groupName)

def pvRenameToOpposite(*args):
    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return
    objects = args

    oppositeList = []
    for obj in objects:
        if 'l_' in obj:
            opp = obj.replace('l_','r_')
            oppositeList.append(opp)
        elif 'r_' in obj:
            obj.replace('r_','l_')
            oppositeList.append(opp)
    return oppositeList

def pvRenderStatsOn():

    allShapesList = cmds.ls(type=['mesh', 'nurbsSurface'])

    for shape in allShapesList:
        cmds.setAttr(shape + '.castsShadows', 1)
        cmds.setAttr(shape + '.receiveShadows', 1)
        cmds.setAttr(shape + '.motionBlur', 1)
        cmds.setAttr(shape + '.primaryVisibility', 1)
        cmds.setAttr(shape + '.smoothShading', 1)
        cmds.setAttr(shape + '.visibleInReflections', 1)
        cmds.setAttr(shape + '.visibleInRefractions', 1)
        cmds.setAttr(shape + '.doubleSided', 1)

def pvCreateGroupAbove(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    for obj in args:

        parent = cmds.listRelatives(obj, parent=True)

        if '_jnt' in obj:
            oriGroup = obj.replace('_jnt', '_ori')
            conGroup = obj.replace('_jnt', '_con')
        elif '_bind' in obj:
            oriGroup = obj.replace('_bind', '_ori')
            conGroup = obj.replace('_bind', '_con')
        elif '_CT' in obj:
            oriGroup = obj.replace('_CT', '_ori')
            conGroup = obj.replace('_CT', '_con')
        elif '_clstr' in obj:
            oriGroup = obj.replace('_clstr', '_ori')
            conGroup = obj.replace('_clstr', '_con')
        else:
            oriGroup = obj + '_ori'
            conGroup = obj + '_con'

        cmds.group(empty=True, world=True, name=oriGroup)
        cmds.group(empty=True, world=True, name=conGroup)
        cmds.delete(cmds.parentConstraint(obj, oriGroup, maintainOffset=False))
        cmds.delete(cmds.parentConstraint(obj, conGroup, maintainOffset=False))
        if parent:
            cmds.parent(oriGroup, parent)
        cmds.parent(conGroup, oriGroup)
        cmds.parent(obj, conGroup)