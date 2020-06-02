#!/usr/bin/env python
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mm
"""
        an_skinProcedures
        
    -getSkin() 
    -setSkin ()
    -copySkin ()
    -swapSkin()
    -copySkinToSelVertex()
    -selectMissingRightSideJnt()
    -editSelectedJntWeights():  - run paint skin tools an lock unselected jnts weights -
    -copyAndMirrowWeights()
    
"""
def buildSkin():
    geo = 'body_cage'
    copySkin ('legs_skin', geo) #копируем скин на кейдж обьект
    swapSkin( 'waist_skin',  geo) # перекидываем через hips01_bind кость. Тем самым заменяем hips01_bind на hips02_bind
    swapSkin( 'arms_skin',  geo) # перекидываем через bodyTw0_jnt кость. Тем самым заменяем bodyTw0_jnt на spine04_bind
    
    tw_data =['l_upArm_jnt', 'l_armBendUpTw_geo'], ['l_foreArm_jnt', 'l_armBendDwTw_geo'], ['r_upArm_jnt', 'r_armBendUpTw_geo'], ['r_foreArm_jnt', 'r_armBendDwTw_geo'], ['neck_bind', 'neckTwTw_geo']
    
    #for jnt, twGeo in tw_data:
        #cmds.select(jnt, twGeo)
        #mm.eval("AddInfluence")
        #cmds.select(cl=True)
        
    for jnt, twGeo in tw_data:
        weight = swapSkin( twGeo, geo )
 

 

def getSkin (geo):
    skinCluster = cmds.ls (cmds.listHistory (geo), type='skinCluster' )[0]
    jnts = cmds.ls (cmds.listHistory (skinCluster, levels=1), type='transform')  ###   jnt  
    jnts = [ jnt for jnt in  jnts if  not cmds.connectionInfo(jnt+'.worldInverseMatrix[0]', isSource=True) ]
    weight = {}                           
    jointIndex, skinClusterIndex, skinClusterConnect, skinClusterConnectPart = [], '', '', ''  # get jnt index and weight
    sizeArray = cmds.getAttr (geo + ".cp", size=True )
    for i in xrange(len(jnts)):   
        skinClusterConnect = cmds.listConnections (jnts[i] + ".worldMatrix", type='skinCluster', plugs=True )
        flag = 0
        for skinClusterIndex  in xrange(len(skinClusterConnect)):    
            skinClusterConnectPart =  skinClusterConnect[skinClusterIndex].split("[")    
            if skinCluster + ".matrix" == skinClusterConnectPart[0] :
    			flag = 1
    			break
        jointIndex = skinClusterConnectPart[1][:-1]
        weight[jnts[i]] = cmds.getAttr (skinCluster + ".weightList[0:" + str(sizeArray - 1) + "].w[" + jointIndex + "]")
    return weight


def setSkin (geo, weight):  
    if cmds.ls (cmds.listHistory (geo), type='skinCluster' ):  #unbind skin Cluster if it exists
        skCluster = cmds.ls (cmds.listHistory (geo), type='skinCluster' )[0]
        cmds.skinCluster(skCluster,   e=True, unbind=True)  
    jnt = [x for x in  weight.keys() if  cmds.objectType(x)=='joint'] + [x for x in  weight.keys() if not cmds.objectType(x)=='joint'] # sort	jnt forvard
    skCluster = cmds.skinCluster(jnt[0], geo, tsb=True, normalizeWeights=True)[0]  #skinning
    useGeoFlag = True if  [ x for x in jnt if not cmds.objectType(x)== 'joint']  else False # influense geo test
    if useGeoFlag:  cmds.setAttr (skCluster+".useComponents", 1)
    cmds.skinCluster(skCluster,   e=True, useGeometry=useGeoFlag, addInfluence=jnt[1:], wt=0.0) # add influenses
    pointsList = range(len(weight[jnt[0]]))# point number list
    jntAndPos=[] # joint and pos in claster list 
    for jn in  jnt[1:]:  
        jntAndPos.append([jn, [ x for x in cmds.connectionInfo(jn +'.worldMatrix[0]', dfs=True) if skCluster in x][0].split(']')[0].split ('[')[1]]) #get position in clasters jnt list
    for jn, pos in  jntAndPos: #go through all the joints except the first one and it positions in skin claster
        for i in pointsList: #go through all points for carrent joint 
            if weight[jn][i]>0: # if point weight larger than 0
                oldWeight = cmds.getAttr (skCluster + ".weightList[" +str(i)+ "].w[0]" )  # get point weight for first joint 
                cmds.setAttr (skCluster + ".weightList[" +str(i)+ "].w[0]", oldWeight - weight[jn][i]) # correct and set point weight for first joint 
                cmds.setAttr (skCluster + ".weightList[" +str(i)+ "].w[" + pos + "]", weight[jn][i] ) #  set point weight for carrent joint 
    return skCluster


def copySkin(geo, dest_geo ):
    sourceSkin = cmds.ls(cmds.listHistory(geo, pruneDagObjects=True) , type='skinCluster')[0]
    influences = cmds.skinCluster(sourceSkin, query=True, influence=True)
    joints = cmds.ls(influences, type='joint') # getting joints list on source skinCluster
    nurbs = list(set(influences) - set(joints)) # getting nurbs list on source skinCluster
    useComp = cmds.getAttr(sourceSkin + '.useComponents') # getting state of "useComponents" attribute on source skinCluster
    hist = cmds.listHistory(dest_geo, pruneDagObjects=True) # try to find history on the destination object
    dest_geoSkin = cmds.ls(hist, type='skinCluster')[0]  if cmds.ls(hist, type='skinCluster') else None# try to find skinCluster on the destination object
    if dest_geoSkin: cmds.skinCluster(dest_geoSkin, e=True, unbind=True) # unbind skinCluster with deleting history
    tempJoint = None   # create new skinCluster on destination object with joints influences
    if not joints: 
        cmds.select(clear=True)
        tempJoint = cmds.joint()
        joints = tempJoint
    destSkin = cmds.skinCluster(dest_geo, joints, toSelectedBones=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, rui=False, mi=5, omi =False, normalizeWeights=True)[0]                            
    if nurbs:   # add nurbs influences in new skinCluster
        cmds.skinCluster(destSkin, edit=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, lockWeights=False, weight=0, addInfluence=nurbs) 
    cmds.setAttr((destSkin + '.useComponents'), useComp) # set state for useComponets attribute
    # copy skin weights from source object to destination
    cmds.copySkinWeights(sourceSkin=sourceSkin, destinationSkin=destSkin, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='oneToOne', normalize=True)
    if tempJoint: cmds.delete(tempJoint) # clear template joints
          
    if  cmds.getAttr('%s.deformUserNormals'%destSkin): # setting up userNormals
        cmds.setAttr('%s.deformUserNormals'%destSkin, 0)
  


def swapSkin( s_geo='', t_geo='', setSkinWeights=True ): #source_geo, target_geo
    if not s_geo:
        s_geo, t_geo = cmds.ls(sl=True)
    s_geo_weight = getSkin(s_geo)
    t_geo_weight = getSkin(t_geo)
    base_jnt = [x for x in s_geo_weight.keys() if sum(s_geo_weight[x])==0][0]
    mutualJoints = list(set(s_geo_weight.keys())  &  set(t_geo_weight.keys())) 
    
    if len(mutualJoints)==1: #insert
        copySkin(s_geo, t_geo)
        pasted_weight = getSkin(t_geo)
        base_jnt_weight = t_geo_weight.pop(base_jnt)     
        for jnt in pasted_weight.keys(): 
                t_geo_weight[jnt]= [pasted_weight[jnt][i]*base_jnt_weight[i] for i in  range( len(base_jnt_weight))] 
        if setSkinWeights:
            setSkin(t_geo, t_geo_weight)
            cmds.select(s_geo, t_geo) 
        return t_geo_weight
    else:                    #extract
        jnts = [x for x in s_geo_weight.keys() if not x==base_jnt]
        for v in xrange(len(t_geo_weight[base_jnt])) :
            t_geo_weight[base_jnt][v] = sum([t_geo_weight[jn][v] for jn in jnts ])
        for jn in jnts:
            t_geo_weight.pop(jn) 
        if setSkinWeights:
            setSkin(t_geo, t_geo_weight) 
            cmds.select(s_geo, t_geo)
        return t_geo_weight

 
def copySkinToSelVertex(sourceObj, destVert):  #copy Skin Weights from object to list of vertex on over object
    destObj = destVert[0].split('.')[0]  
    sourceSkin = cmds.ls(cmds.listHistory(sourceObj, pruneDagObjects=True) , type='skinCluster')[0]
    influences = cmds.skinCluster(sourceSkin, query=True, influence=True)
    joints = cmds.ls(influences, type='joint') # getting joints list on source skinCluster
    nurbs = list(set(influences) - set(joints)) # getting nurbs list on source skinCluster
    useComp = cmds.getAttr(sourceSkin + '.useComponents') # getting state of "useComponents" attribute on source skinCluster
    destObjSkin = cmds.ls(cmds.listHistory(destObj, pruneDagObjects=True), type='skinCluster')[0]   # find skinCluster on the destination object
    destInfluences = cmds.skinCluster(destObjSkin, query=True, influence=True)
    for inf in influences:
        if cmds.nodeType(inf) == 'joint' and not inf in destInfluences :
            cmds.skinCluster(destObjSkin, edit=True, lockWeights=False, weight=0, addInfluence=inf) 
    cmds.select(sourceObj, destVert)
    cmds.copySkinWeights(  noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='oneToOne', normalize=True) 
    cmds.select(cl=True)
        
def selectMissingRightSideJnt():
    objectName = cmds.ls(sl=True)[0]
    skinClusterName =  cmds.ls (cmds.listHistory (objectName, pdo=1), type='skinCluster')[0]    ### if claster sel
    history = cmds.listHistory (objectName)
    clustersName = cmds.ls (history, type='skinCluster' )
    skinClusterSetName = cmds.listConnections (skinClusterName, type='objectSet' )
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  
    rSidJnt = ['r_'+x[2:] for x in jointName if 'l_'==x[:2]]
    missingJnt = []
    for jnt in  rSidJnt:
        if not jnt in jointName:
             missingJnt.append(jnt)
    cmds.select(missingJnt)

 
def editSelectedJntWeights():  
    geo = cmds.ls(sl=True)[-1]
    jnts = cmds.ls(sl=True)[:-1]
    skinClusterV = cmds.ls (cmds.listHistory (geo), type='skinCluster' )[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterV, levels=1), type='transform')   
 
    for jnt in [x for x in jointName if not x in jnts]:  cmds.setAttr (jnt+'.liw', 1)
    for jnt in  jnts:  cmds.setAttr (jnt+'.liw', 0)

    import maya.mel as mm 
    cmds.select(geo)
    mm.eval("ArtPaintSkinWeightsToolOptions;")
    mm.eval('setSmoothSkinInfluence '+jnts[0]+' ;artSkinRevealSelected artAttrSkinPaintCtx;')

 
def copyAndMirrowWeights( s_geo='', t_geo=''):

    if not s_geo:  s_geo, t_geo = cmds.ls(sl=True)        
    if cmds.ls (cmds.listHistory (t_geo), type='skinCluster' ):  #unbind skin Cluster if it exists
        skCluster = cmds.ls (cmds.listHistory (t_geo), type='skinCluster' )[0]
        cmds.skinCluster(skCluster,   e=True, unbind=True)   
    hist = cmds.listHistory(s_geo, pruneDagObjects=True) # try to find history on the destination object
    s_geoSkin = cmds.ls(hist, type='skinCluster')[0]  if cmds.ls(hist, type='skinCluster') else None
    jointName = cmds.ls (cmds.listHistory (s_geoSkin, levels=1), type='transform') 
    rSidJnt = []
    for jnt in jointName:
        if 'l_'==jnt[:2]:rSidJnt.append ('r_'+jnt[2:])
        else:   rSidJnt.append(jnt)
    
    jnt = [x for x in  rSidJnt if  cmds.objectType(x)=='joint']  +  [x for x in  rSidJnt if not cmds.objectType(x)=='joint'] # sort	jnt forvard
    skCluster = cmds.skinCluster(rSidJnt, t_geo, tsb=True, normalizeWeights=True)[0]  #skinning
    cmds.select(s_geo, t_geo) 
    mm.eval( 'MirrorSkinWeights')


 

    