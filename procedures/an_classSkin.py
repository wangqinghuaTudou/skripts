

#16.07.2019 insert -copySkinToSelectionsVertex()
#01.03.2019 new skin order
#06.02.2019 insert Skin Geo proc
#10.01.2019 Add cod for fingers dkin

from  anProcedures import  an_saveLoadData
import maya.cmds as cmds
    

'''
base structure:
    
cage______geo
    cageHalf______geo # half final skin
    l_root______geo
        l_arm______geo # shoulder
            l_hand______geo # hand
        l_leg______geo # hips02_bind
        body______geo # hips02_bind

skin hierarhy metods:
    -getDataFromAttr()
    -delDataAttr() 
    -printHi()
    -addPart() 
    -removePart()
    -getMutualJoint():# return joint list which use in both skin klasters ( geo1, geo )
    -updateSkin()
    -getParent()
     
weight list metods: 
    -insertJointsToWeightList() # Insert joints to weight list  
    -getSkinWeights()
    -setSkinWeights()
    -copySkin()
    -copySkinToSelectionsVertex()
    
    -addRightSide()
    -replaceJntInList()
    
'''


# mutual_joint = 'l_foreArm_jnt'

def insertSkinGeo(mutual_joint=""):
    sers, targ = cmds.ls(sl=True)  # insert to skin
    self = AnSkinSys(targ)
    self.getSkinWeights()

    if not mutual_joint:
        mutual_joint = AnSkinSys('').getMutualJoint(self.skinGeo, sers)[0]

    self.insertJointsToWeightList(sers, mutual_joint)
    self.setSkinWeights()


#----------------------------------------------------------------------------------------------- 


'''
self = AnSkinSys('bodyArm_skin') 
self.getSkinWeights()
data = {'l_shoulder_bind':   ['l_shoulder01_cp', 'l_shoulder02_cp'],
             'l_upArm_jnt':    [ 'l_upArm01_cp', 'l_upArm02_cp',  'l_armBendUpTw_geo'],
            'l_foreArm_jnt':   [ 'l_foreArm01_cp', 'l_foreArm02_cp', 'l_armBendDwTw_geo' ]  #
            }

for jnt in data.keys():
    for geo in  data[jnt]:
        self.insertJointsToWeightList(geo, jnt) 

self.setSkinWeights ()



'''





class AnSkinSys(): 
    def __init__ (self, skinGeo, rootGeo = ''): 
        self.skinGeo = skinGeo  #final skin geo  
        self.rootGeo = rootGeo  #general geo in hierarhy 
        self.skinHierarhy =[self.rootGeo]
        self.weightList=[]
        #if cmds.objExists(self.skinGeo+'.data'): self.getDataFromAttr (grp=self.skinGeo)
        #else: an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo)    
    '''--------------------------------------------skin hierarhy metods:------------------------------------------------------------''' 

    def getDataFromAttr (self, grp):  self.skinHierarhy =  an_saveLoadData(obgect=grp)[0] 
    
    def delDataAttr (self): cmds.deleteAttr(self.skinGeo+'.data')
         
    def printHi(self):
        print 'Final geo: ', self.skinGeo 
        print "------------------"
        for x in self.skinHierarhy: print x.replace('*_', '   ')
         
    def addPart(self):
        childGeo, parentGeo = cmds.ls(sl=True)
        for i  in range (len(self.skinHierarhy)):
            if parentGeo == self.skinHierarhy[i].split('*_')[-1]  :
                 lev =  len(self.skinHierarhy[i].split('*_'))
                 self.skinHierarhy.insert(i+1, "*_"*lev+childGeo)
        an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo)                

    def removePart(self): 
        geo = cmds.ls(sl=True)[0]
        for i  in range (len(self.skinHierarhy)):
            if geo==self.skinHierarhy[i].split('*_')[-1]:
                self.skinHierarhy.pop(i)
        an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo) 

    def getParent(self, geo):
        geoList = [x.split('*_')[-1] for x in self.skinHierarhy]
        id = [ x[0] for x in enumerate( geoList ) if x[1]== geo ][0] # geo id in list       
        pNumber = len( self.skinHierarhy[id].split('*_'))-1 #namber of stars
        if pNumber == 0: return None 
        i=id-1
        while len(self.skinHierarhy[i].split('*_'))-1 >= pNumber:  i=i-1 # find parent             
        return   geoList[i]  

    def addRightSide(self):
        skinClusterName =  cmds.ls (cmds.listHistory (self.skinGeo, pdo=1), type='skinCluster')[0]    ### if claster sel
        history = cmds.listHistory (self.skinGeo)
        clustersName = cmds.ls (history, type='skinCluster' )
        skinClusterSetName = cmds.listConnections (skinClusterName, type='objectSet' )
        jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt
        rSidJnt = ['r_'+x[2:] for x in jointName if 'l_'==x[:2]]
        
        cmds.skinCluster(skinClusterName,   e=True, addInfluence=rSidJnt, wt=0.0)
        cmds.copySkinWeights (ss=skinClusterName, ds=skinClusterName, mirrorMode='YZ', surfaceAssociation='closestPoint', influenceAssociation='closestJoint')

    def getMutualJoint(self, geo1, geo):# return joint list which use in both skin klasters ( geo1, geo )
        mutualJoints = list(set(AnSkinSys(geo1).getSkinWeights().keys()) & set(AnSkinSys(geo).getSkinWeights().keys()))
        return mutualJoints
   
    def updateSkin(self):

        if cmds.ls (cmds.listHistory (self.skinGeo), type='skinCluster' ):  #unbind skin Cluster if it exists
            skCluster = cmds.ls (cmds.listHistory (self.skinGeo), type='skinCluster' )[0]
            cmds.skinCluster(skCluster,   e=True, unbind=True)  
        
        self.weightList = AnSkinSys(self.rootGeo).getSkinWeights()
       
        for geo in  [x.split('*_')[-1] for x in self.skinHierarhy[1:]]: 
            geoWeightList = AnSkinSys(geo).getSkinWeights()
            getTargetJnt = list (set(self.weightList.keys()) & set(geoWeightList.keys())) [0] 
            self.insertJointsToWeightList(geo, getTargetJnt )
            print geo.replace('*_', '   ') 
        self.setSkinWeights()   
        #self.addRightSide()  
            
        '''                  -------------------------weight list metods:------------------------------------------------------------''' 
        
    '''Insert joints to weight list  '''
    #pastedSkin, taegetInfluence = geo, self.skinGeo
    def insertJointsToWeightList (self, pastedSkin, taegetInfluence ):  #taegetInfluence - influence joint or geometry
        tmpGeo = cmds.duplicate (self.skinGeo )[0] # copy skin to  skinGeo duplicate
        AnSkinSys('').copySkin(pastedSkin, tmpGeo )
        pastedWeightList = AnSkinSys(tmpGeo).getSkinWeights() #get pasted weight List
        cmds.delete(tmpGeo) 
        taegetInfWeightList = self.weightList.pop(taegetInfluence)     # delete taeget Influence in self.weightList and get it val
        for jnt in pastedWeightList.keys(): 
            self.weightList[jnt]= [pastedWeightList[jnt][i]*taegetInfWeightList[i] for i in  range( len(taegetInfWeightList))]                                                     
        return self.weightList
    
    """get  skin weights """   
    def getSkinWeights(self):  # get  skin weight """
        skinClusterName = cmds.ls (cmds.listHistory (self.skinGeo), type='skinCluster' )[0]
        jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')  ###   jnt  
        jointName = [ jnt for jnt in  jointName if  not cmds.connectionInfo(jnt+'.worldInverseMatrix[0]', isSource=True) ]
        weightList = {}                           
        jointIndex, skinClusterIndex, skinClusterConnect, skinClusterConnectPart = [], '', '', ''  # get jnt index and weight
        sizeArray = cmds.getAttr (self.skinGeo + ".cp", size=True )
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
        self.weightList = weightList   
        return weightList
        
    
    """ set  skin weights """  
    def setSkinWeights (self):   # new procedure
    
        if cmds.ls (cmds.listHistory (self.skinGeo), type='skinCluster' ):  #unbind skin Cluster if it exists
            skCluster = cmds.ls (cmds.listHistory (self.skinGeo), type='skinCluster' )[0]
            cmds.skinCluster(skCluster,   e=True, unbind=True)  
        
        jnt = [x for x in  self.weightList.keys() if  cmds.objectType(x)=='joint'] + [x for x in  self.weightList.keys() if not cmds.objectType(x)=='joint'] # sort	jnt forvard
        skCluster = cmds.skinCluster(jnt[0], self.skinGeo, tsb=True, normalizeWeights=True)[0]  #skinning
        cmds.setAttr (skCluster+".useComponents", 1)
        useGeoFlag = True if  [ x for x in jnt if not cmds.objectType(x)== 'joint']  else False # influense geo test
        cmds.skinCluster(skCluster,   e=True, useGeometry=useGeoFlag, addInfluence=jnt[1:], wt=0.0) # add influenses
        
        pointsList = range(len(self.weightList[jnt[0]]))# point number list
        jntAndPos=[] # joint and pos in claster list 
        for jn in  jnt[1:]:  jntAndPos.append([jn, [ x for x in cmds.connectionInfo(jn +'.worldMatrix[0]', dfs=True) if skCluster in x][0].split(']')[0].split ('[')[1]]) #get position in clasters jnt list
        
        for jn, pos in  jntAndPos: #go through all the joints except the first one and it positions in skin claster
            for i in pointsList: #go through all points for carrent joint 
                if self.weightList[jn][i]>0: # if point weight larger than 0
                    oldWeight = cmds.getAttr (skCluster + ".weightList[" +str(i)+ "].w[0]" )  # get point weight for first joint 
                    cmds.setAttr (skCluster + ".weightList[" +str(i)+ "].w[0]", oldWeight - self.weightList[jn][i]) # correct and set point weight for first joint 
                    cmds.setAttr (skCluster + ".weightList[" +str(i)+ "].w[" + pos + "]", self.weightList[jn][i] ) #  set point weight for carrent joint 

    #sourceObj, destObj = pastedSkin, tmpGeo 

                  
    """ copy skin weights """ 
    def copySkin(self, sourceObj, destObj ):
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
       
    def replaceJntInList(self, newJnt, oldJnt ): # replaces one list of joint with another in weight list dictionary
        weightList[newJnt] = weightList.pop(oldJnt) 
        return weightList  
        
        
    '''copy Skin To Selections Vertex'''
    def copySkinToSelectionsVertex (self, sourceObj, destVert):  #copy Skin Weights from object to list of vertex on over object
     
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

        
        
            