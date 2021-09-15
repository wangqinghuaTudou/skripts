# 15.09.2021 new skin_assembling function
# 16.07.2019 insert -copySkinToSelectionsVertex()
# 01.03.2019 new skin order
# 06.02.2019 insert Skin Geo proc
# 10.01.2019 Add cod for fingers dkin

from anProcedures import an_saveLoadData
import maya.cmds as cmds

'''
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


def insertSkinGeo(mutual_joint=""):
    sers, targ = cmds.ls(sl=True)
    self = AnSkinSys(targ)
    self.getSkinWeights()
    if not mutual_joint:
        mutual_joint = AnSkinSys('').getMutualJoint(self.skinGeo, sers)[0]
    self.insertJointsToWeightList(sers, mutual_joint)
    self.setSkinWeights()


def skin_assembling():
    """
    All pieces of skining are add to the place of "mutual_joint" from "body_proxy",
    only Hand_Proxy is added to the place of "hand_mutual_joint". After this,
    mirrow the weights to the right side.
    """

    body_proxy = "body_proxy"
    legs_proxy = "legs_proxy"
    arm_proxy = "arm_proxy"  # shoulder included
    head_proxy = "head_proxy"  # neck and head
    torso_proxy = "torso_proxy"
    hand_proxy = "hand_proxy"

    mutual_joint = "hips02_bind"
    hand_mutual_joint = "l_hand_bind"

    data = {'l_upArm_jnt': 'l_armBendUpTw_geo',
            'l_foreArm_jnt': 'l_armBendDwTw_geo',
            'l_upLeg_jnt': 'l_legBendUpTw_geo',
            'l_lowLeg_jnt': 'l_legBendDwTw_geo',
            'neck_bind': 'neckTwTw_geo'}

    self = AnSkinSys(body_proxy)
    self.copySkin(legs_proxy, body_proxy)
    self.getSkinWeights()

    self.insertJointsToWeightList(arm_proxy, mutual_joint)
    self.insertJointsToWeightList(head_proxy, mutual_joint)
    self.insertJointsToWeightList(torso_proxy, mutual_joint)
    self.insertJointsToWeightList(hand_proxy, hand_mutual_joint)

    for jnt in data.keys():
        self.insertJointsToWeightList(data[jnt], jnt)

    self.setSkinWeights()
    self.addRightSide()


class AnSkinSys():
    def __init__(self, skinGeo, rootGeo=''):
        self.skinGeo = skinGeo  # final skin geo
        self.rootGeo = rootGeo  # general geo in hierarhy
        self.skinHierarhy = [self.rootGeo]
        self.weightList = []
        # if cmds.objExists(self.skinGeo+'.data'): self.getDataFromAttr (grp=self.skinGeo)
        # else: an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo)

    '''--------------------------------------------skin hierarhy metods:-------------------------------------------'''

    def getDataFromAttr(self, grp):
        self.skinHierarhy = an_saveLoadData(obgect=grp)[0]

    def delDataAttr(self):
        cmds.deleteAttr(self.skinGeo + '.data')

    def printHi(self):
        print 'Final geo: ', self.skinGeo
        print "------------------"
        for x in self.skinHierarhy: print x.replace('*_', '   ')

    def addPart(self):
        childGeo, parentGeo = cmds.ls(sl=True)
        for i in range(len(self.skinHierarhy)):
            if parentGeo == self.skinHierarhy[i].split('*_')[-1]:
                lev = len(self.skinHierarhy[i].split('*_'))
                self.skinHierarhy.insert(i + 1, "*_" * lev + childGeo)
        an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo)

    def removePart(self):
        geo = cmds.ls(sl=True)[0]
        for i in range(len(self.skinHierarhy)):
            if geo == self.skinHierarhy[i].split('*_')[-1]:
                self.skinHierarhy.pop(i)
        an_saveLoadData(data=[self.skinHierarhy], obgect=self.skinGeo)

    def getParent(self, geo):
        geoList = [x.split('*_')[-1] for x in self.skinHierarhy]
        id = [x[0] for x in enumerate(geoList) if x[1] == geo][0]  # geo id in list
        pNumber = len(self.skinHierarhy[id].split('*_')) - 1  # namber of stars
        if pNumber == 0: return None
        i = id - 1
        while len(self.skinHierarhy[i].split('*_')) - 1 >= pNumber:  i = i - 1  # find parent
        return geoList[i]

    def addRightSide(self):
        skinClusterName = cmds.ls(cmds.listHistory(self.skinGeo, pdo=1), type='skinCluster')[0]  ### if claster sel
        history = cmds.listHistory(self.skinGeo)
        clustersName = cmds.ls(history, type='skinCluster')
        skinClusterSetName = cmds.listConnections(skinClusterName, type='objectSet')
        jointName = cmds.ls(cmds.listHistory(skinClusterName, levels=1), type='transform')  ###   jnt
        rSidJnt = self.selectMissingRightSideJnt(objectName=self.skinGeo, select=False)
        cmds.skinCluster(skinClusterName, e=True, addInfluence=rSidJnt, wt=0.0)
        cmds.copySkinWeights(ss=skinClusterName, ds=skinClusterName, mirrorMode='YZ', surfaceAssociation='closestPoint',
                             influenceAssociation='closestJoint')

    def getMutualJoint(self, geo1, geo):  # return joint list which use in both skin klasters ( geo1, geo )
        mutualJoints = list(set(AnSkinSys(geo1).getSkinWeights().keys()) & set(AnSkinSys(geo).getSkinWeights().keys()))
        return mutualJoints

    def updateSkin(self):

        if cmds.ls(cmds.listHistory(self.skinGeo), type='skinCluster'):  # unbind skin Cluster if it exists
            skCluster = cmds.ls(cmds.listHistory(self.skinGeo), type='skinCluster')[0]
            cmds.skinCluster(skCluster, e=True, unbind=True)

        self.weightList = AnSkinSys(self.rootGeo).getSkinWeights()

        for geo in [x.split('*_')[-1] for x in self.skinHierarhy[1:]]:
            geoWeightList = AnSkinSys(geo).getSkinWeights()
            getTargetJnt = list(set(self.weightList.keys()) & set(geoWeightList.keys()))[0]
            self.insertJointsToWeightList(geo, getTargetJnt)
            print geo.replace('*_', '   ')
        self.setSkinWeights()
        # self.addRightSide()

        ''' -------------------------weight list metods:-------------------------------------------'''

    def insertJointsToWeightList(self, pastedSkin, taegetInfluence):
        """
        Insert joints to weight list
        taegetInfluence - influence joint or geometry
        """
        tmpGeo = cmds.duplicate(self.skinGeo)[0]  # copy skin to  skinGeo duplicate
        AnSkinSys('').copySkin(pastedSkin, tmpGeo)
        pastedWeightList = AnSkinSys(tmpGeo).getSkinWeights()  # get pasted weight List
        cmds.delete(tmpGeo)
        taegetInfWeightList = self.weightList.pop(
            taegetInfluence)  # delete taeget Influence in self.weightList and get it val
        for jnt in pastedWeightList.keys():
            self.weightList[jnt] = [pastedWeightList[jnt][i] * taegetInfWeightList[i] for i in
                                    range(len(taegetInfWeightList))]
        return self.weightList

    def getSkinWeights(self):
        """
        get  skin weights
        """
        skinClusterName = cmds.ls(cmds.listHistory(self.skinGeo), type='skinCluster')[0]
        jointName = cmds.ls(cmds.listHistory(skinClusterName, levels=1), type='transform')  ###   jnt
        jointName = [jnt for jnt in jointName if not cmds.connectionInfo(jnt + '.worldInverseMatrix[0]', isSource=True)]
        weightList = {}
        jointIndex, skinClusterIndex, skinClusterConnect, skinClusterConnectPart = [], '', '', ''  # get jnt index and weight
        sizeArray = cmds.getAttr(self.skinGeo + ".cp", size=True)
        for i in xrange(len(jointName)):
            skinClusterConnect = cmds.listConnections(jointName[i] + ".worldMatrix", type='skinCluster', plugs=True)
            flag = 0
            for skinClusterIndex in xrange(len(skinClusterConnect)):
                skinClusterConnectPart = skinClusterConnect[skinClusterIndex].split("[")
                if skinClusterName + ".matrix" == skinClusterConnectPart[0]:
                    flag = 1
                    break
            jointIndex = skinClusterConnectPart[1][:-1]
            weightList[jointName[i]] = cmds.getAttr(
                skinClusterName + ".weightList[0:" + str(sizeArray - 1) + "].w[" + jointIndex + "]")
        self.weightList = weightList
        return weightList

    def setSkinWeights(self):
        """
        set  skin weights
        """
        if cmds.ls(cmds.listHistory(self.skinGeo), type='skinCluster'):  # unbind skin Cluster if it exists
            skCluster = cmds.ls(cmds.listHistory(self.skinGeo), type='skinCluster')[0]
            cmds.skinCluster(skCluster, e=True, unbind=True)

        jnt = [x for x in self.weightList.keys() if cmds.objectType(x) == 'joint'] + [x for x in self.weightList.keys()
                                                                                      if not cmds.objectType(
                x) == 'joint']  # sort	jnt forvard
        skCluster = cmds.skinCluster(jnt[0], self.skinGeo, tsb=True, normalizeWeights=True)[0]  # skinning
        cmds.setAttr(skCluster + ".useComponents", 1)
        useGeoFlag = True if [x for x in jnt if not cmds.objectType(x) == 'joint'] else False  # influense geo test
        cmds.skinCluster(skCluster, e=True, useGeometry=useGeoFlag, addInfluence=jnt[1:], wt=0.0)  # add influenses

        pointsList = range(len(self.weightList[jnt[0]]))  # point number list
        jntAndPos = []  # joint and pos in claster list
        for jn in jnt[1:]:  jntAndPos.append([jn, [x for x in cmds.connectionInfo(jn + '.worldMatrix[0]', dfs=True) if
                                                   skCluster in x][0].split(']')[0].split('[')[
            1]])  # get position in clasters jnt list

        for jn, pos in jntAndPos:  # go through all the joints except the first one and it positions in skin claster
            for i in pointsList:  # go through all points for carrent joint
                if self.weightList[jn][i] > 0:  # if point weight larger than 0
                    oldWeight = cmds.getAttr(
                        skCluster + ".weightList[" + str(i) + "].w[0]")  # get point weight for first joint
                    cmds.setAttr(skCluster + ".weightList[" + str(i) + "].w[0]",
                                 oldWeight - self.weightList[jn][i])  # correct and set point weight for first joint
                    cmds.setAttr(skCluster + ".weightList[" + str(i) + "].w[" + pos + "]",
                                 self.weightList[jn][i])  # set point weight for carrent joint

    def copySkin(self, sourceObj, destObj):
        sourceSkin = cmds.ls(cmds.listHistory(sourceObj, pruneDagObjects=True), type='skinCluster')[0]
        influences = cmds.skinCluster(sourceSkin, query=True, influence=True)
        joints = cmds.ls(influences, type='joint')  # getting joints list on source skinCluster
        nurbs = list(set(influences) - set(joints))  # getting nurbs list on source skinCluster
        useComp = cmds.getAttr(
            sourceSkin + '.useComponents')  # getting state of "useComponents" attribute on source skinCluster

        hist = cmds.listHistory(destObj, pruneDagObjects=True)  # try to find history on the destination object
        destObjSkin = cmds.ls(hist, type='skinCluster')[0] if cmds.ls(hist,
                                                                      type='skinCluster') else None  # try to find skinCluster on the destination object
        if destObjSkin: cmds.skinCluster(destObjSkin, e=True, unbind=True)  # unbind skinCluster with deleting history
        tempJoint = None  # create new skinCluster on destination object with joints influences
        if not joints:
            cmds.select(clear=True)
            tempJoint = cmds.joint()
            joints = tempJoint

        destSkin = \
            cmds.skinCluster(destObj, joints, toSelectedBones=True, useGeometry=True, dropoffRate=4,
                             polySmoothness=False,
                             nurbsSamples=25, rui=False, mi=5, omi=False, normalizeWeights=True)[0]
        if nurbs:  # add nurbs influences in new skinCluster
            cmds.skinCluster(destSkin, edit=True, useGeometry=True, dropoffRate=4, polySmoothness=False,
                             nurbsSamples=25, lockWeights=False, weight=0, addInfluence=nurbs)
        cmds.setAttr((destSkin + '.useComponents'), useComp)  # set state for useComponets attribute
        # copy skin weights from source object to destination
        cmds.copySkinWeights(sourceSkin=sourceSkin, destinationSkin=destSkin, noMirror=True,
                             surfaceAssociation='closestPoint', influenceAssociation='oneToOne', normalize=True)
        if tempJoint: cmds.delete(tempJoint)  # clear template joints

        if cmds.getAttr('%s.deformUserNormals' % destSkin):  # setting up userNormals
            cmds.setAttr('%s.deformUserNormals' % destSkin, 0)
        cmds.select(destObj, r=True)  # selecting destination object

    def replaceJntInList(self, newJnt, oldJnt):  # replaces one list of joint with another in weight list dictionary
        weightList[newJnt] = weightList.pop(oldJnt)
        return weightList

    def copySkinToSelectionsVertex(self, sourceObj, destVert):
        """ copy Skin Weights from object to list of vertex on over object """
        destObj = destVert[0].split('.')[0]
        sourceSkin = cmds.ls(cmds.listHistory(sourceObj, pruneDagObjects=True), type='skinCluster')[0]
        influences = cmds.skinCluster(sourceSkin, query=True, influence=True)
        joints = cmds.ls(influences, type='joint')  # getting joints list on source skinCluster
        nurbs = list(set(influences) - set(joints))  # getting nurbs list on source skinCluster
        useComp = cmds.getAttr(
            sourceSkin + '.useComponents')  # getting state of "useComponents" attribute on source skinCluster

        destObjSkin = cmds.ls(cmds.listHistory(destObj, pruneDagObjects=True), type='skinCluster')[
            0]  # find skinCluster on the destination object
        destInfluences = cmds.skinCluster(destObjSkin, query=True, influence=True)

        for inf in influences:
            if cmds.nodeType(inf) == 'joint' and not inf in destInfluences:
                cmds.skinCluster(destObjSkin, edit=True, lockWeights=False, weight=0, addInfluence=inf)

        cmds.select(sourceObj, destVert)
        cmds.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='oneToOne',
                             normalize=True)
        cmds.select(cl=True)

    @staticmethod
    def selectMissingRightSideJnt(objectName="", select=True):
        if not objectName:
            objectName = cmds.ls(sl=True)[0]
        skinClusterName = cmds.ls(cmds.listHistory(objectName, pdo=1), type='skinCluster')[0]
        history = cmds.listHistory(objectName)
        clustersName = cmds.ls(history, type='skinCluster')
        skinClusterSetName = cmds.listConnections(skinClusterName, type='objectSet')
        jointName = cmds.ls(cmds.listHistory(skinClusterName, levels=1), type='transform')
        rSidJnt = ['r_' + x[2:] for x in jointName if 'l_' == x[:2]]
        missingJnt = []
        for jnt in rSidJnt:
            if not jnt in jointName:
                missingJnt.append(jnt)
        if select:
            cmds.select(missingJnt)
        return missingJnt
