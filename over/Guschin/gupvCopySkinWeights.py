# copy skin weight from one object to another's
import maya.cmds as mc
import pvProcedures as pvp
import maya.OpenMaya as om

def gupvCopySkinWeights():
    
    surfAssocList = ['Closest Point on Surface', \
                     'Ray Cast', \
                     'Closest Component', \
                     'UV Space']
    
    inflAssocList = ['Closest Joint', \
                     'Closest Bone', \
                     'One to One', \
                     'Label', \
                     'Name']
    copyMethod = ['one to many','many to one']       #gu many to one
    
    win = 'gupvCopySkinWeightsUI'

    if mc.window(win, exists=True):
        mc.deleteUI(win)

    win = mc.window(win, title='Copy Skin Weights', \
                    width=300, \
                    height=170, \
                    sizeable=True)

    mc.columnLayout ('gupvMainLayoutCopySkin', \
                     width=300, \
                     height=170, \
                     adjustableColumn=True)
    mc.rowColumnLayout('gupvRowLayoutSurfAssoc', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 170]])
    mc.text('gupvTextSurfAssoc', label='Surface Association:', align='right')
    mc.optionMenuGrp('gupvOptMenuGrpSurfAssoc', columnWidth=[1, 80])
    for item in surfAssocList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('gupvOptMenuGrpSurfAssoc', edit=True, select=1)
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('gupvRowLayoutInfluence', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 170]])
    mc.text('gupvTextInflAssoc', label='Influence Association:', align='right')
    mc.optionMenuGrp('gupvOptMenuGrpInflAssoc', columnWidth=[1, 80])
    for item in inflAssocList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('gupvOptMenuGrpInflAssoc', edit=True, select=3)
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('gupvRowLayoutSettings', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 160]])
    mc.text('gupvTextCheckBoxNorm', label='', align='right')
    mc.checkBox('gupvCheckBoxNorm', value=0, label='Normalize', align='right')
    mc.text('gupvTextCheckBoxForce', label='', align='right')
    mc.checkBox('gupvCheckBoxForce', value=1, label='Delete Exists SkinCluster', align='right')
    mc.text('gupvTextCheckBoxRemUi', label='', align='right')
    mc.checkBox('gupvCheckBoxRemUi', value=1, label='Remove Unused Influences', align='right')
    mc.setParent('..')

    mc.separator(height=5, style='in')
    mc.rowColumnLayout('gupvRowLayoutNurbsSamp', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 30]])
    mc.text('gupvTextIntFieldNurbsSamp', label='NURBS Samples:', align='right')
    mc.intField('gupvIntFieldNurbsSamp', value=25, minValue=0, maxValue=100, width=50)
    mc.setParent('..')

    mc.separator(height=5, style='in')                                         #gu many to one
    mc.rowColumnLayout('gupvRowLayoutCopyMethod', numberOfColumns=2, \
                       columnAttach=[1, 'right', 10], \
                       columnWidth=[[1, 120], [2, 170]])                       #gu many to one
    mc.text('guCopyMethod', label='Copy method:', align='right')               #gu many to one
    mc.optionMenuGrp('guOptMenuCopyMethod', columnWidth=[1, 80])               #gu many to one
    for item in copyMethod:                                                    #gu many to one
        mc.menuItem(label=item)                                                #gu many to one
    mc.optionMenuGrp('guOptMenuCopyMethod', edit=True, select=1)               #gu many to one
    mc.setParent('..')
    mc.separator(height=5, style='in') 
    mc.button('gupvButtonRunCopySkin', label='Copy', \
              width=90, \
              command='gupvCopySkinWeightsMain()')

    mc.showWindow(win)


def gupvCopySkinWeightsInterfaceRequest():

    win = 'gupvCopySkinWeightsUI'

    if not mc.window(win, exists=True):
        om.MGlobal.displayInfo('Interface is absent. Assigned default settings.')
        force = 1
        remUi = 1
        nurbsSamp = 25
        surfAssoc = 1
        inflAssoc = 3
        norm = 0
    else:
        force = mc.checkBox('gupvCheckBoxForce', query=True, value=True)
        remUi = mc.checkBox('gupvCheckBoxRemUi', query=True, value=True)
        nurbsSamp = mc.intField('gupvIntFieldNurbsSamp', query=True, value=True)

        # query necessary attributes for copy skin weights
        if mc.optionMenuGrp('gupvOptMenuGrpSurfAssoc', exists=True):
            surfAssoc = mc.optionMenuGrp('gupvOptMenuGrpSurfAssoc', query=True, select=True)
        else:
            surfAssoc = 1
        if mc.optionMenuGrp('gupvOptMenuGrpInflAssoc', exists=True):
            inflAssoc = mc.optionMenuGrp('gupvOptMenuGrpInflAssoc', query=True, select=True)
        else:
            inflAssoc = 3
        if mc.checkBox('gupvCheckBoxNorm', exists=True):
            norm = mc.checkBox('gupvCheckBoxNorm', query=True, value=True)
        else:
            norm = 0
        if mc.optionMenuGrp('guOptMenuCopyMethod', exists=True):
            manyToOne = mc.optionMenuGrp('guOptMenuCopyMethod', query=True, select=True)-1
        else:
            manyToOne = 0

    return force, remUi, nurbsSamp, surfAssoc, inflAssoc, norm , manyToOne

def gupvCopySkinWeightsMain(*args):

    force, remUi, nurbsSamp, surfAssoc, inflAssoc, norm , manyToOne = gupvCopySkinWeightsInterfaceRequest()

    if not args:
        args = mc.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return
    if len(args) < 2: # check count of the selected objects
        om.MGlobal.displayInfo('Must be selected more than one object.')
        return
    destList = list(args)
    if manyToOne:
        sourceObj  = destList[:-1] # getting source object (should selected first)           #gu many to one -FIXED 
        destList = [destList[-1]]                                                            #gu many to one -FIXED 
        sourceSkin = [pvp.pvGetSkinCluster(x) for x in sourceObj]                            #gu many to one -FIXED 
        influences = []                                                                      #gu many to one -FIXED 
        if remUi: # getting influences list on source skinCluster
            for i in sourceSkin:                                                             #gu many to one -FIXED 
                influences += mc.skinCluster(i, query=True, weightedInfluence=True)          #gu many to one -FIXED 
        else:                                                                                #gu many to one -FIXED 
            for i in sourceSkin:                                                             #gu many to one -FIXED 
                influences += mc.skinCluster(i, query=True, influence=True)                  #gu many to one -FIXED 
        influences=list(set(influences))                                                     #gu many to one -FIXED 
    else:
        sourceObj  = destList.pop(0) # getting source object (should selected first)         #gu one to many - OLD
        sourceSkin = pvp.pvGetSkinCluster(sourceObj)                                         #gu one to many - OLD
        if remUi: # getting influences list on source skinCluster                            #gu one to many - OLD
            influences = mc.skinCluster(sourceSkin, query=True, weightedInfluence=True)      #gu one to many - OLD
        else:                                                                                #gu one to many - OLD
            influences = mc.skinCluster(sourceSkin, query=True, influence=True)              #gu one to many - OLD
    joints = mc.ls(influences, type='joint') # getting joints list on source skinCluster
    nurbs = list(set(influences) - set(joints)) # getting nurbs list on source skinCluster
    #useComp = mc.getAttr(sourceSkin + '.useComponents') # getting state of "useComponents" attribute on source skinCluster      #gu    -OLD
    if nurbs:                                                                            #gu many to one -FIXED 
        useComp=True                                                                     #gu many to one -FIXED 
    else:                                                                                #gu many to one -FIXED 
        useComp=False                                                                    #gu many to one -FIXED 
    for destObj in destList: # try to find history on the destination object             
        destObjSkin = pvp.pvGetSkinCluster(destObj)
        if not destObjSkin:
            gupvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm, manyToOne) # copy skinCluster and skinWeights from source object to destination
            continue
        else:
            if not force: # if skinCluster exists on the destination object, check the "force" attribute and decide delete skinCluster or not
                om.MGlobal.displayInfo('Object %s already have SkinCluster - %s. It was skiped. Need to use "Delete Exists SkinCluster", to delete it.'%(destObj, destObjSkin))
            else:
                mc.skinCluster(destObjSkin, edit=True, unbind=True) # unbind skinCluster with deleting history
                om.MGlobal.displayInfo('SkinCluster %s on object %s was deleted.'%(destObjSkin, destObj))
                gupvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm, manyToOne,args) # copy skinCluster and skinWeights from source object to destination
  
def gupvCopySkin(destObj, joints, nurbs, sourceSkin, useComp, nurbsSamp, remUi, surfAssoc, inflAssoc, norm, manyToOne, args):
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
    if manyToOne:                                                                                                     #gu many to one -FIXED 
        om.MGlobal.displayInfo('transfer from '+str(args[0:-1])+' to '+str(args[-1]))                                 #gu many to one -FIXED 
        if UVspace:                                                                                                   #gu many to one -FIXED 
            mc.copySkinWeights(args, \
                               noMirror=True, \
                               surfaceAssociation=surfAssoc, \
                               influenceAssociation=inflAssoc, \
                               normalize=norm, \
                               uvSpace=['map1', 'map1'])                                                              #gu many to one -FIXED 
        else:                                                                                                         #gu many to one -FIXED 
            mc.copySkinWeights(args, \
                               surfaceAssociation=surfAssoc, \
                               influenceAssociation=inflAssoc, \
                               normalize=norm)                                                                        #gu many to one -FIXED 
    else:
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

# gupvCopySkinWeights()

