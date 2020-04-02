import maya.cmds as cmds
from  anProcedures import  * 


"""______________an_skinProcedures_______________"""



""" get  skin weight """
def getSkinJntAndWeight( objectName):
    skinClusterName = cmds.ls (cmds.listHistory (objectName), type='skinCluster' )[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt  
    weightList = {}                           
    jointIndex, skinClusterIndex, skinClusterConnect, skinClusterConnectPart = [], '', '', ''  # get jnt index and weight
    sizeArray = cmds.getAttr (objectName + ".cp", size=True )
    
    for i in xrange(len(jointName)):   
        skinClusterConnect = cmds.listConnections (jointName[i] + ".worldMatrix", type='skinCluster', plugs=True )
        flag = 0
        for skinClusterIndex  in xrange(len(skinClusterConnect)):    
            skinClusterConnectPart =  skinClusterConnect[skinClusterIndex].split("[")    
            if skinClusterName + ".matrix" == skinClusterConnectPart[0] :
    			flag = 1
    			break
        jointIndex = skinClusterConnectPart[1][:-1]
        weightList[jointName[i]] = cmds.getAttr (skinClusterName + ".weightList[0:" + str(sizeArray - 1) + "].w[" + jointIndex + "]")
    return weightList


""" set  skin weight """  
def setSkinAndWeight ( objectName,  weightList):
    jnt=[]
    for x in  weightList.keys( ):  jnt.insert(0, x) if  cmds.objectType(x)== 'joint'  else  jnt.append( x) # sort	jnt forvard
    newSkinClusterName = cmds.skinCluster(jnt[0], objectName, tsb=True, normalizeWeights=True)[0]  #skinning
    cmds.setAttr (newSkinClusterName+".useComponents", 1)
    useGeoFlag = True if  [ x for x in jnt if not cmds.objectType(x)== 'joint']  else False # influense geo test
    cmds.skinCluster(newSkinClusterName,   e=True, useGeometry=useGeoFlag, addInfluence=jnt[1:], wt=0.0) # add influenses
    for j in  range(len(jnt))[1:]:
            addJntAndItsWeight(jnt[j], weightList[jnt[j]], jnt[0], objectName)


""" add one jnt weight to over skin claster   """  
def addJntAndItsWeight(impJnt, weightList, targetJnt, targetGeo):
    skinClusterName = cmds.ls (cmds.listHistory (targetGeo), type='skinCluster' )[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt  
    if not impJnt in jointName: 
        cmds.skinCluster(skinClusterName,   e=True, addInfluence=impJnt, wt=0.0) # add influenses
    print skinClusterName    
    #get position in clasters jnt list  
    impJntWPos = [ x for x in cmds.connectionInfo(impJnt +'.worldMatrix[0]',destinationFromSource=True) if skinClusterName in x][0].split(']')[0].split ('[')[1]
    targetJntWPos = [ x for x in cmds.connectionInfo(targetJnt +'.worldMatrix[0]',destinationFromSource=True) if skinClusterName in x][0].split(']')[0].split ('[')[1]
    
    for i in range(len(weightList)):
            if weightList[i] :    
                oldWeight = cmds.getAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + targetJntWPos + "]" ) 
                if oldWeight>0:
                    if  (oldWeight - weightList[i]) >0 :  
                        cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + targetJntWPos + "]", oldWeight - weightList[i] )
                        cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + impJntWPos + "]", weightList[i] )
                    else :
                        cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + targetJntWPos + "]", 0.0 )
                        cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + impJntWPos + "]", oldWeight )
    cmds.setAttr (skinClusterName+".maintainMaxInfluences", 0)


""" insert several jnts and its weight to one jnt """  
def insertJntAndWeight():
    sl1, sl2 = cmds.ls(sl=True)
    copyGeo= cmds.duplicate (sl2)[0]
    an_copySkin( sl1, copyGeo)
    
    serseGeo, targetGeo = copyGeo, sl2
    
    #serseGeo, targetGeo = cmds.ls(sl=True)
    serseGeoWeight = getSkinJntAndWeight( serseGeo)
    targetGeoWeight = getSkinJntAndWeight( targetGeo)

    targetJnt =[]
    for jnt in targetGeoWeight.keys(): 
        if jnt in serseGeoWeight.keys(): targetJnt.append(jnt)
  
    for jnt in serseGeoWeight.keys():
        if not jnt==targetJnt[0]:
            addJntAndItsWeight(jnt, serseGeoWeight[jnt], targetJnt[0], targetGeo)
    cmds.delete (copyGeo)

"""
def doInsert():
    serseGeo, targetGeo = cmds.ls(sl=True)
    copyGeo= cmds.duplicate (targetGeo)[0]
    an_copySkin( serseGeo, copyGeo)
    cmds.select (copyGeo, targetGeo)
    insertJntAndWeight()
    cmds.delete (copyGeo)

 
def insertJntAndWeight():
    serseGeo, targetGeo = cmds.ls(sl=True)
    serseGeoWeight = getSkinJntAndWeight( serseGeo)
    targetGeoWeight = getSkinJntAndWeight( targetGeo)

    targetJnt =[]
    for jnt in targetGeoWeight.keys(): 
        if jnt in serseGeoWeight.keys(): targetJnt.append(jnt)
  
    for jnt in serseGeoWeight.keys():
        if not jnt==targetJnt[0]:
            addJntAndItsWeight(jnt, serseGeoWeight[jnt], targetJnt[0], targetGeo)

"""



""" run paint skin tools an lock unselected jnts weights """  
def editSelectedJntWeights():  # select jnt then geo
    geo = cmds.ls(sl=True)[-1]
    jnts = cmds.ls(sl=True)[:-1]
    
    skinClusterV = cmds.ls (cmds.listHistory (geo), type='skinCluster' )[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterV, levels=1), type='transform')  ###   jnt  
 
    for jnt in [x for x in jointName if not x in jnts]:  cmds.setAttr (jnt+'.liw', 1)
    for jnt in  jnts:  cmds.setAttr (jnt+'.liw', 0)

    import maya.mel as mm 
    cmds.select(geo)
    mm.eval("ArtPaintSkinWeightsToolOptions;")
    mm.eval('setSmoothSkinInfluence '+jnts[0]+' ;artSkinRevealSelected artAttrSkinPaintCtx;')


""" copy skin weight from one object to another """  
def an_copySkin( sourceObj, destObj ):  
    #sourceObj, destObj = cmds.ls(selection=True)
    sourceSkin = cmds.ls(cmds.listHistory(sourceObj, pruneDagObjects=True) , type='skinCluster')[0]
    influences = cmds.skinCluster(sourceSkin, query=True, influence=True)
    joints = cmds.ls(influences, type='joint') # getting joints list on source skinCluster
    nurbs = list(set(influences) - set(joints)) # getting nurbs list on source skinCluster
    useComp = cmds.getAttr(sourceSkin + '.useComponents') # getting state of "useComponents" attribute on source skinCluster

    hist = cmds.listHistory(destObj, pruneDagObjects=True) # try to find history on the destination object
    destObjSkin = cmds.ls(hist, type='skinCluster')[0]  if cmds.ls(hist, type='skinCluster') else None# try to find skinCluster on the destination object
    if destObjSkin: cmds.skinCluster(destObjSkin, e=True, unbind=True) # unbind skinCluster with deleting history
    tempJoint = None   # create new skinCluster on destination object with joints influences
    if not joints: 
        cmds.select(clear=True)
        tempJoint = cmds.joint()
        joints = tempJoint
        
    destSkin = cmds.skinCluster(destObj, joints, toSelectedBones=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, rui=False, mi=5, omi =False, normalizeWeights=True)[0]                            
    if nurbs:   # add nurbs influences in new skinCluster
        cmds.skinCluster(destSkin, edit=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, lockWeights=False, weight=0, addInfluence=nurbs) 
    cmds.setAttr((destSkin + '.useComponents'), useComp) # set state for useComponets attribute
    # copy skin weights from source object to destination
    cmds.copySkinWeights(sourceSkin=sourceSkin, destinationSkin=destSkin, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='oneToOne', normalize=True)
    
    if tempJoint: cmds.delete(tempJoint) # clear template joints
          
    if  cmds.getAttr('%s.deformUserNormals'%destSkin): # setting up userNormals
        cmds.setAttr('%s.deformUserNormals'%destSkin, 0)
    cmds.select(destObj, r=True) # selecting destination object

 
def combineSkinParts():     # connect parts of skin to one  
    geo = 'body____skin'
    corpus,  arm, leg, hand = 'corpus____skin',  'arm____skin', 'leg____skin', 'hand____skin' 
    
    an_copySkin( corpus, geo) 
    
    cmds.select(arm, geo)
    insertJntAndWeight()
    
    cmds.select(leg, geo)
    insertJntAndWeight()
    
    cmds.select(hand, geo)
    insertJntAndWeight()

    cmds.select(geo)              #add right joints
    selectMissingRightSideJnt ()
    r_jnts = cmds.ls(sl=True)
    skinClusterName = cmds.ls (cmds.listHistory (geo), type='skinCluster' )[0]
    cmds.skinCluster(skinClusterName,   e=True, addInfluence=r_jnts, wt=0.0)

    cmds.copySkinWeights (ss=skinClusterName, ds=skinClusterName, mirrorMode='YZ', surfaceAssociation='closestPoint', influenceAssociation='closestJoint')


def selectMissingRightSideJnt ():
    objectName = cmds.ls(sl=True)[0]
    skinClusterName =  cmds.ls (cmds.listHistory (objectName, pdo=1), type='skinCluster')[0]    ### if claster sel
    history = cmds.listHistory (objectName)
    clustersName = cmds.ls (history, type='skinCluster' )
    skinClusterSetName = cmds.listConnections (skinClusterName, type='objectSet' )
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt
    rSidJnt = ['r_'+x[2:] for x in jointName if 'l_'==x[:2]]
    missingJnt = []
    for jnt in  rSidJnt:
        if not jnt in jointName:
             missingJnt.append(jnt)
    cmds.select(missingJnt)
    
    