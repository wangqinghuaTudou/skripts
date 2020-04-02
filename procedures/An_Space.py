import maya.cmds as cmds
from CharacterNames import CharacterNames as chn
from  anProcedures import  an_delSys

class An_Space():
    
    attrDic = {'parent':'space', 'point':"tSpace", 'orient':"rSpace"}
    
    def __init__ (self, ctrl, object='', targList=[], spaceType = 'parent'):
        self.ctrl  = ctrl
        self.obj  = object
        self.targList  = targList # list [obj, attr],  [obj, attr],
        self.spaceType = spaceType
        self.driverAttr = ctrl+'.'+ self.attrDic[spaceType]                   
    
    def bildSpaceObj(self):         
        cmds.addAttr (self.ctrl, ln = self.attrDic[self.spaceType],  at="enum",  keyable=True, en="none")                                                                       
        enumAttr = setEnumName([x[1]for x in self.targList ])      #______________define Enum attr name
        cmds.addAttr (self.driverAttr, e=True, enumName=enumAttr)# edit  attr             
        for target , attr in  self.targList: 
            targetPosGrp = grpForSpace(self.obj, target, self.spaceType )[0] #______________ made grp For Space and made constrant
            exec( 'constraint = cmds.'+self.spaceType+'Constraint("'+targetPosGrp +'", "'+self.obj+'", mo=True)[0]' ) 
        if self.targList:
            exec( 'constraintAttributes = cmds.'+self.spaceType+'Constraint("'+constraint+'", q=True, wal =True)' ) #get constrant weths
            for index, string in enumerate(self.targList):
                for drVal, val in zip([index-1, index, index+1], [0,1,0]) : #driver Val List and valList
                    cmds.setDrivenKeyframe( constraint+'.'+constraintAttributes[index] , dv=drVal,  v=val,  cd=self.driverAttr )   

    def rebildSpaceObj(self): 
        if cmds.objExists(self.driverAttr):  self.delSpaceObj()
        self.bildSpaceObj()
 
    def delSpaceObj(self):
        aCurv =[x.split('.')[0] for x in cmds.connectionInfo (self.driverAttr, destinationFromSource = True) ]
        if aCurv:
            constraint = cmds.connectionInfo(aCurv[0]+".output", destinationFromSource = True)[0].split('.')[0] 
            targGrpList=[]  
            exec( 'targGrpList = cmds.'+self.spaceType+'Constraint("'+constraint+'", q=True, targetList =True)' )
            cmds.delete (aCurv)  
            cmds.delete (targGrpList) 
        cmds.deleteAttr( self.driverAttr.split('.')[0], at = self.driverAttr.split('.')[1])

    def getSpaceInfo(self, driverAttr): 
        spaceType = {'space':'parent' , "tSpace":'point', "rSpace":'orient'} [driverAttr.split('.')[1]]              #__get type  
        aCurv =[x.split('.')[0] for x in cmds.connectionInfo (driverAttr, destinationFromSource = True) ]  # get anim curves
        if not aCurv: return [], [], spaceType, [],[], []
        constraint = cmds.connectionInfo(aCurv[0]+".output", destinationFromSource = True)[0].split('.')[0]             #__get constraint
        exec( 'targets = cmds.'+spaceType+'Constraint("'+constraint+'", q=True, targetList=True)' )                  #__get targets
        attrs  =  cmds.addAttr (driverAttr, q=True, enumName=True ).split (':')                                      #__get atributes
        targList = zip( [cmds.listRelatives (cmds.listRelatives (x, p=True)[0], p=True)[0] for x in targets] , attrs)#__get targList
        obj  = cmds.connectionInfo(constraint+".constraintParentInverseMatrix", sfd = True).split('.')[0]            #__get obj
        exec( 'constraintAttributes =   cmds.'+spaceType+'Constraint("'+constraint+'", q=True, wal =True)')          #__get constraintAttributes
        return obj, targList, spaceType, constraint, constraintAttributes, aCurv
    
    def PrintInfo (self):
        print '-------------------------------'
        print 'ctrl - ', self.ctrl 
        print 'object - ', self.obj
        print 'class type - ', self.spaceType
        print 'targList - ', self.targList    
        print 'driverAttr - ', self.driverAttr   

def grpForSpace(obj, target, spaceType, q=False):
    tCar = "P" if spaceType=='point' else ""
    posGrp = chn(obj).divideName()[0]+ chn(obj).divideName()[1]+ chn(target).divideName()[0].capitalize()[:-1]+ chn(target).divideName()[1]+ tCar+ chn(obj).suffixes[27] 
    folderGrp  =  chn(target).divideName()[0]+  chn(target).divideName()[1]+"Spaces"+ chn(obj).suffixes[3]
    if not q: 
        if not cmds.objExists(folderGrp):
            folderGrp = cmds.group (n=folderGrp,  em=True)
            cmds.parent (folderGrp, target)
            for attr in [".t",".r"]: cmds.setAttr (folderGrp+attr, 0, 0, 0)
        if not cmds.objExists(posGrp): 
            posGrp = cmds.group (n=posGrp,  em=True)
            cmds.parent (posGrp, folderGrp )
            cmds.delete (cmds.parentConstraint ( obj, posGrp))
    return  posGrp, folderGrp

def setEnumName(attrList):
    if not attrList:return 'none' 
    out = ''
    for index, string in enumerate(attrList):
        out = out + string
        if not index==len(attrList)-1: out = out+':'
    return out



#targList =[]
#targList = (['pSphere1','sphere'], ['pCube1', 'cube'],  ['pPyramid1', 'pyramid', ],  ['pCylinder1', 'cylinder'] )
#ttt = An_Space( 'locator1',  'group1', targList, spaceType = 'orient')
#ttt.bildSpaceObj() 
#ttt.rebildSpaceObj()  
#ttt.PrintInfo()
#ttt.delSpaceObj() 
#ttt.getSpaceInfo('locator1.tSpace')


