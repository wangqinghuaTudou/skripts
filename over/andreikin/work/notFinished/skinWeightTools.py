



#objectName =  cmds.ls(sl=True)[0]     
    

#impJnt='testCSDir01_jnt'
#targetJnt='joint2'            
#targetGeo = 'body_geo'
#weightList = getSkinJntAndWeight( 'tmpCopy')[impJnt]

def addJntAndItsWeight(impJnt, weightList, targetJnt, targetGeo):

    skinClusterName = cmds.ls (cmds.listHistory (targetGeo), type='skinCluster' )[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt  
    if not impJnt in jointName: 
        cmds.skinCluster(skinClusterName,   e=True, addInfluence=impJnt, wt=0.0) # add influenses
    #get position in clasters jnt list  
    impJntWPos = [ x for x in cmds.connectionInfo(impJnt +'.worldMatrix[0]',destinationFromSource=True) if skinClusterName in x][0].split(']')[0].split ('[')[1]
    targetJntWPos = [ x for x in cmds.connectionInfo(targetJnt +'.worldMatrix[0]',destinationFromSource=True) if skinClusterName in x][0].split(']')[0].split ('[')[1]
    
    for i in range(len(weightList)):
            if weightList[i] :    
                oldWeight = cmds.getAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + targetJntWPos + "]" ) 
                cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + targetJntWPos + "]", oldWeight - weightList[i] )
                cmds.setAttr (skinClusterName + ".weightList[" +str(i)+ "].w[" + impJntWPos + "]", weightList[i] )




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
    
    
    
    
def setSkinAndWeight ( objectName,  weightList):
    jnt=[]
    for x in  weightList.keys( ):  jnt.insert(0, x) if  cmds.objectType(x)== 'joint'  else  jnt.append( x) # sort	jnt forvard
    newSkinClusterName = cmds.skinCluster(jnt[0], objectName, tsb=True, normalizeWeights=True)[0]  #skinning
    cmds.setAttr (newSkinClusterName+".useComponents", 1)
    cmds.skinCluster(newSkinClusterName,   e=True, useGeometry=True, addInfluence=jnt[1:]) # add influenses
    sizeArray = cmds.getAttr (objectName + ".cp", size=True ) # get point number
 
 
    for i in  range(len(jnt)):
        for id in range(sizeArray):
                cmds.setAttr (newSkinClusterName + ".weightList[" +str(id)+ "].w[" + str(i)+ "]", weightList[jnt[i]][id]  )

            
#         
            
            
            
            
            
            
            
            
    
    
    