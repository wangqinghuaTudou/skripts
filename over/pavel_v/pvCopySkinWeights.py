# copy skin weight from one object to another's
import maya.cmds as mc
import pvProcedures as pvp
import maya.OpenMaya as om

def pvCopySkinWeights():
    
    surfAssocList = ['Closest Point on Surface', \
                     'Ray Cast', \
                     'Closest Component', \
                     'UV Space']
    
    inflAssocList = ['Closest Joint', \
                     'Closest Bone', \
                     'One to One', \
                     'Label', \
                     'Name']

    win = 'pvCopySkinWeightsUI'

    if mc.window(win, exists=True):
        mc.deleteUI(win)

    win = mc.window(win, title='Copy Skin Weights', \
                    width=300, \
                    height=170, \
                    sizeable=True)

    mc.columnLayout ('pvMainLayoutCopySkin', \
                     width=300, \
                     height=170, \
                     adjustableColumn=True)
    mc.rowColumnLayout('pvRowLayoutSurfAssoc', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 170]])
    mc.text('pvTextSurfAssoc', label='Surface Association:', align='right')
    mc.optionMenuGrp('pvOptMenuGrpSurfAssoc', columnWidth=[1, 80])
    for item in surfAssocList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('pvOptMenuGrpSurfAssoc', edit=True, select=1)
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('pvRowLayoutInfluence', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 170]])
    mc.text('pvTextInflAssoc', label='Influence Association:', align='right')
    mc.optionMenuGrp('pvOptMenuGrpInflAssoc', columnWidth=[1, 80])
    for item in inflAssocList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('pvOptMenuGrpInflAssoc', edit=True, select=3)
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('pvRowLayoutSettings', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 160]])
    mc.text('pvTextCheckBoxNorm', label='', align='right')
    mc.checkBox('pvCheckBoxNorm', value=0, label='Normalize', align='right')
    mc.text('pvTextCheckBoxForce', label='', align='right')
    mc.checkBox('pvCheckBoxForce', value=1, label='Delete Exists SkinCluster', align='right')
    mc.text('pvTextCheckBoxRemUi', label='', align='right')
    mc.checkBox('pvCheckBoxRemUi', value=1, label='Remove Unused Influences', align='right')
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('pvRowLayoutNurbsSamp', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 30]])
    mc.text('pvTextIntFieldNurbsSamp', label='NURBS Samples:', align='right')
    mc.intField('pvIntFieldNurbsSamp', value=25, minValue=0, maxValue=100, width=50)
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.button('pvButtonRunCopySkin', label='Copy', \
              width=90, \
              command='pvCopySkinWeightsMain()')

    mc.showWindow(win)

def pvCopySkinWeightsInterfaceRequest():

    win = 'pvCopySkinWeightsUI'

    if not mc.window(win, exists=True):
        om.MGlobal.displayInfo('Interface is absent. Assigned default settings.')
        force = 1
        remUi = 1
        nurbsSamp = 25
        surfAssoc = 1
        inflAssoc = 3
        norm = 0
    else:
        force = mc.checkBox('pvCheckBoxForce', query=True, value=True)
        remUi = mc.checkBox('pvCheckBoxRemUi', query=True, value=True)
        nurbsSamp = mc.intField('pvIntFieldNurbsSamp', query=True, value=True)

        # query necessary attributes for copy skin weights
        if mc.optionMenuGrp('pvOptMenuGrpSurfAssoc', exists=True):
            surfAssoc = mc.optionMenuGrp('pvOptMenuGrpSurfAssoc', query=True, select=True)
        else:
            surfAssoc = 1
        if mc.optionMenuGrp('pvOptMenuGrpInflAssoc', exists=True):
            inflAssoc = mc.optionMenuGrp('pvOptMenuGrpInflAssoc', query=True, select=True)
        else:
            inflAssoc = 3
        if mc.checkBox('pvCheckBoxNorm', exists=True):
            norm = mc.checkBox('pvCheckBoxNorm', query=True, value=True)
        else:
            norm = 0

    return force, remUi, nurbsSamp, surfAssoc, inflAssoc, norm

def pvCopySkinWeightsMain(*args):

    force, remUi, nurbsSamp, surfAssoc, inflAssoc, norm = pvCopySkinWeightsInterfaceRequest()

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return
    if len(args) < 2: # check count of the selected objects
        om.MGlobal.displayInfo('Must be selected more than one object.')
        return

    destList = list(args)
    sourceObj  = destList.pop(0) # getting source object (should selected first)
    sourceSkin = pvp.pvGetSkinCluster(sourceObj)
    if remUi: # getting influences list on source skinCluster
        influences = mc.skinCluster(sourceSkin, query=True, weightedInfluence=True)
    else:
        influences = mc.skinCluster(sourceSkin, query=True, influence=True)
    joints = mc.ls(influences, type='joint') # getting joints list on source skinCluster
    nurbs = list(set(influences) - set(joints)) # getting nurbs list on source skinCluster
    useComp = mc.getAttr(sourceSkin + '.useComponents') # getting state of "useComponents" attribute on source skinCluster
    for destObj in destList: # try to find history on the destination object
        destObjSkin = pvp.pvGetSkinCluster(destObj)
        if not destObjSkin:
            pvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm) # copy skinCluster and skinWeights from source object to destination
            continue
        else:
            if not force: # if skinCluster exists on the destination object, check the "force" attribute and decide delete skinCluster or not
                om.MGlobal.displayInfo('Object %s already have SkinCluster - %s. It was skiped. Need to use "Delete Exists SkinCluster", to delete it.'%(destObj, destObjSkin))
            else:
                mc.skinCluster(destObjSkin, edit=True, unbind=True) # unbind skinCluster with deleting history
                om.MGlobal.displayInfo('SkinCluster %s on object %s was deleted.'%(destObjSkin, destObj))
                pvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm) # copy skinCluster and skinWeights from source object to destination

def pvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm):
    # describe template variables
    tempJoint = None
    UVspace = None

    if surfAssoc == 1:
        surfAssoc = 'closestPoint'
    elif surfAssoc == 2:
        surfAssoc = 'rayCast'
    elif surfAssoc == 3:
        surfAssoc = 'closestComponent'
    elif surfAssoc == 4:
        surfAssoc = 'closestComponent'
        UVspace = True

    if inflAssoc == 1:
        inflAssoc = 'closestJoint'
    elif inflAssoc == 2:
        inflAssoc = 'closestBone'
    elif inflAssoc == 3:
        inflAssoc = 'oneToOne'
    elif inflAssoc == 4:
        inflAssoc = 'label'
    elif inflAssoc == 5:
        inflAssoc = 'name'

    # create new skinCluster on destination object with joints influences
    if joints:
        destSkin = mc.skinCluster(destObj, \
                                  joints, \
                                  toSelectedBones=True, \
                                  useGeometry=True, \
                                  dropoffRate=4, \
                                  polySmoothness=False, \
                                  nurbsSamples=nurbsSamp, \
                                  removeUnusedInfluence=False, \
                                  maximumInfluences=5, \
                                  obeyMaxInfluences=False, \
                                  normalizeWeights=True)[0]
    else:
        mc.select(clear=True)
        tempJoint = mc.joint()
        om.MGlobal.displayInfo('tempJoint: %s'%tempJoint)
        destSkin = mc.skinCluster(destObj, \
                                  tempJoint, \
                                  toSelectedBones=True, \
                                  useGeometry=True, \
                                  dropoffRate=4, \
                                  polySmoothness=False, \
                                  nurbsSamples=nurbsSamp, \
                                  removeUnusedInfluence=False, \
                                  maximumInfluences=5, \
                                  obeyMaxInfluences=False, \
                                  normalizeWeights=True)[0]

    # add nurbs influences in new skinCluster
    if nurbs:
        mc.skinCluster(destSkin, \
                       edit=True, \
                       useGeometry=True, \
                       dropoffRate=4, \
                       polySmoothness=False, \
                       nurbsSamples=nurbsSamp, \
                       lockWeights=False, \
                       weight=0, \
                       addInfluence=nurbs)

    # set state for useComponets attribute
    mc.setAttr((destSkin + '.useComponents'), useComp)

    # copy skin weights from source object to destination
    if UVspace:
        mc.copySkinWeights(sourceSkin=sourceSkin, \
                           destinationSkin=destSkin, \
                           noMirror=True, \
                           surfaceAssociation=surfAssoc, \
                           influenceAssociation=inflAssoc, \
                           normalize=norm, \
                           uvSpace=['map1', 'map1'])
    else:
        mc.copySkinWeights(sourceSkin=sourceSkin, \
                           destinationSkin=destSkin, \
                           noMirror=True, \
                           surfaceAssociation=surfAssoc, \
                           influenceAssociation=inflAssoc, \
                           normalize=norm)

    # remove unused influences
    if remUi:
        pvp.pvRemoveUnusedInfl(destSkin)

    # clear template joints
    if tempJoint:
        mc.delete(tempJoint)

    # setting up userNormals
    if mc.getAttr('%s.deformUserNormals'%destSkin):
        mc.setAttr('%s.deformUserNormals'%destSkin, 0)

    # selecting destination object
    mc.select(destObj, r=True)

# pvCopySkinWeights()