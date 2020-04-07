#!/usr/bin/env python
# -*- coding: utf-8 -*-






"""

        skin
         
    -getSkin 
    -setSkin 
    -copySkin 
    -swapSkin
    -copySkinToSelVertex
    -getSwapJoint
    
    - skinUi
    
"""


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
    cmds.select(dest_geo, r=True) # selecting destination object


 
 





    