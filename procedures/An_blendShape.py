import maya.cmds as cmds
class An_blendShape():
    def __init__ (self, name, attrList =[], targList =[]): 
        self.name = name      #name of blend Shape
        self.obj = ''
        self.attrList = attrList
        self.targList = targList
        self.conList = []        

    def an_getInfo (self):
        self.attrList = cmds.aliasAttr (self.name,  q=True)[::2]
        self.targList = cmds.blendShape (self.name, q=True, t=True)
        self.obj = cmds.blendShape (self.name, q=True, geometry=True)[0] 
        self.conList = []
        for attr in self.attrList:
            val = cmds.getAttr (self.name+"."+attr,) 
            if cmds.connectionInfo(self.name+"."+attr, isDestination=True):
                connection = cmds.connectionInfo(self.name+"."+attr, sourceFromDestination=True)
                self.conList.append([connection, attr, val])
            else: self.conList.append(['', attr, val])
        print '_____', self.name, '_____'
        print 'attrList - ', self.obj
        print 'attrList - ', self.attrList
        print 'targList - ', self.targList
        print 'conList - ', self.conList
        #return 

    def an_restoreTargets (self):  
        self.an_getInfo()
        objTrans = cmds.listRelatives (self.obj, p=True)[0]
        
        for index, attr in enumerate(self.attrList):  # disconnect blend shape attr  and set attr to 0
            if  self.conList[index][0] : cmds.disconnectAttr (self.conList[index][0]   , self.name+'.'+ attr )
            cmds.setAttr ( self.name+'.'+ attr, 0)
        for index, attr in enumerate(self.attrList):  # duplicate obj
            cmds.setAttr ( self.name+'.'+ attr, 1)
            targ = cmds.duplicate( objTrans, n = attr )[0]
            cmds.setAttr ( self.name+'.'+ attr, 0)
            self.targList.append(targ)
            print index, targ
        for index, attr in enumerate(self.attrList):  # connect blend shape attr  and set attr to source
            if  self.conList[index][0] : 
                cmds.connectAttr (self.conList[index][0], self.name+'.'+ attr)
            else: cmds.setAttr ( self.name+'.'+ attr, self.conList[index][2])
            targShape = cmds.listRelatives(self.targList[index],  s=True)[0]
            cmds.connectAttr (targShape+'.worldMesh[0]' , self.name+'.inputTarget[0].inputTargetGroup['+ str(index)+'].inputTargetItem[6000].inputGeomTarget') 