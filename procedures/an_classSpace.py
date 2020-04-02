import maya.cmds as cmds
from an_classNames import AnNames as chn
from  anProcedures import  an_delSys

"""
        AnSpace
        
    metods:  
        - bildSpaceObj ()
        - rebildSpaceObj () 
        - delSpaceObj()
        - getSpaceInfo()
        - printInfo ()
       
"""

class AnSpace():
    
    attrDic = {'parent':'space', 'point':"tSpace", 'orient':"rSpace", 'scale':"sSpace"}
    
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
            cmds.delete (constraint) 
            for grp in targGrpList: 
                if len( cmds.connectionInfo(grp+'.parentMatrix[0]', dfs=True)) == 0:
                    cmds.delete (grp) 

        cmds.deleteAttr( self.driverAttr.split('.')[0], at = self.driverAttr.split('.')[1])
    
    def getSpaceInfo(self, driverAttr): 
        spaceType = {'space':'parent' , "tSpace":'point', "rSpace":'orient', 'sSpace':"scale"} [driverAttr.split('.')[1]]              #__get type  
        aCurv =[x.split('.')[0] for x in cmds.connectionInfo (driverAttr, destinationFromSource = True) ]  # get anim curves
        if not aCurv: return [], [], spaceType, [],[], []
        constraint = cmds.connectionInfo(aCurv[0]+".output", destinationFromSource = True)[0].split('.')[0]             #__get constraint
        exec( 'targets = cmds.'+spaceType+'Constraint("'+constraint+'", q=True, targetList=True)' )                  #__get targets
        attrs  =  cmds.addAttr (driverAttr, q=True, enumName=True ).split (':')                                      #__get atributes
        targList = zip( [cmds.listRelatives (cmds.listRelatives (x, p=True)[0], p=True)[0] for x in targets] , attrs)#__get targList
        obj  = cmds.connectionInfo(constraint+".constraintParentInverseMatrix", sfd = True).split('.')[0]            #__get obj
        exec( 'constraintAttributes =   cmds.'+spaceType+'Constraint("'+constraint+'", q=True, wal =True)')          #__get constraintAttributes
        return obj, targList, spaceType, constraint, constraintAttributes, aCurv
    
    def printInfo (self):
        print '                                    '
        print '---- AnSpace instance --------------'
        print 'ctrl - ', self.ctrl 
        print 'object - ', self.obj
        print 'class type - ', self.spaceType
        print 'targList - ', self.targList    
        print 'driverAttr - ', self.driverAttr


def grpForSpace(obj, target, spaceType, q=False):
    tCar = "P" if spaceType=='point' else ""
    posGrp = chn(obj).divideName()[0]+ chn(obj).divideName()[1]+ chn(target).divideName()[0].capitalize()[:-1]+ chn(target).divideName()[1] + tCar + chn(obj).suffixes() [27]
    folderGrp  =  chn(target).divideName()[0]+  chn(target).divideName()[1]+"Spaces"+ chn(obj).suffixes()[3]
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
#self = AnSpace( 'locator1',  'group1', targList, spaceType = 'scale')
#self.bildSpaceObj()
#self.rebildSpaceObj()  
#self.printInfo()
#self.delSpaceObj() 
#self.getSpaceInfo('locator1.sSpace')
    
def addScaleToParentSpace():
    controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True)
    cmds.connectAttr( controller + ".space", controller + ".sSpace") 
    cmds.setAttr ( controller + ".sSpace", k=False)

win = "spaceUi1"
def an_targetUiBlock( target, attr): # ui which  is inserted to global ui for the each target
    cmds.window (win, e=True, height=cmds.window (win, q=True, height=True )+25 )
    cmds.rowColumnLayout(target+'Layout', nc =4 ,  p='spaceTargetColumnLayout'  )
    cmds.text ( '' , al='left',  width= 142  )
    cmds.textField(target+'textField', tx= target)
    cmds.textField(target+'attrField', tx=attr )
    butCom = 'cmds.deleteUI("'+target+'Layout");'+'cmds.window ("'+win+'",e=True, height=cmds.window ("'+win+'",q=True, height=True )-25 )'
    cmds.button(l='delete', c=butCom ,w=62 )
    cmds.setParent( '..')
                                                                     # insert all target and atributes to Ui
def an_addTargetsToUI(): [an_targetUiBlock( target, chn(target).divideName()[0]+chn(target).divideName()[1]) for  target in cmds.ls(sl=True)]

def an_deleteSpace():
    controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True, )
    spaceType = {1:'parent', 2:"point", 3:"orient", 4:"scale"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    classObj = AnSpace(controller, spaceType = spaceType )
    classObj.delSpaceObj()
    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:  #del targets ui
        cmds.deleteUI (Layout)
        cmds.window (win, e=True, height=cmds.window (win, q=True, height=True )-25 )

def an_insertSpaceToUi( fromTextFild = True):  # fill interface after specifying controller or type
    if fromTextFild :
        controller =  cmds.ls (sl=True)[0]
        cmds.textFieldButtonGrp ('TFBG_control', e=True, tx=controller )
    else: controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True )
    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:
            cmds.deleteUI (Layout)
            cmds.window (win ,e=True, height=cmds.window (win, q=True, height=True )-25 )
    spaceType = {1:'parent', 2:"point", 3:"orient", 4:"scale"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    
    classObj = AnSpace( controller, spaceType = spaceType )
    
    if cmds.objExists(controller+'.'+classObj.attrDic[spaceType]):
        info = classObj.getSpaceInfo( controller+'.'+classObj.attrDic[spaceType])
        cmds.textFieldButtonGrp ('TFBG_object', e=True, tx=info[0] )
        for target in info[1] : an_targetUiBlock( target[0], target[1])

 

def an_spaceUi():
    
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Space maker v4.00", width=440,  height=169, s=False, rtf=True, menuBar=True )
    cmds.window (win, e=True,  height=169 )
    
    cmds.menu (label="Additional" )
    
    cmds.menuItem( label='Add scale to parent space', c='addScaleToParentSpace()')
    
    cmds.columnLayout ('spaceColumnLayoutName'  , adjustableColumn=True)
    cmds.frameLayout( label='Base and control objects:', bgc =[0,0,0] )
    cmds.columnLayout (  adjustableColumn=True)
    cmds.textFieldButtonGrp ('TFBG_control', l="Controler:",  bl="<<Add selected",
            cw = [(1, 124), (2, 210)],  bc = "an_insertSpaceToUi()" )
    cmds.textFieldButtonGrp ('TFBG_object', l="Objects:",  bl="<<Add selected",
            cw = [(1, 124), (2, 210)],  bc = "cmds.textFieldButtonGrp ('TFBG_object', e=True, tx=  cmds.ls (sl=True)[0])" )
    cmds.radioButtonGrp('typeRBG', label='Constraint type:  ',
                        labelArray4=['Parent', 'Point', 'Orient', 'Scale'],
                        numberOfRadioButtons=4,
                        sl=1,
                        cw = [(1, 130), (2, 60), (3, 60), (4, 60) ],
                        cc = "an_insertSpaceToUi(fromTextFild = False)" )
    cmds.setParent( 'spaceColumnLayoutName')

    cmds.frameLayout( label='Targets and attributes:', bgc =[0,0,0] )
    cmds.columnLayout ('spaceTargetColumnLayout'  ,  adjustableColumn=True)
    cmds.rowColumnLayout(nc =4 ,  p='spaceTargetColumnLayout'  )
    cmds.text ( '' , al='left',  width= 142  )
    cmds.text ( '  target:' , al='left', width= 122  )
    cmds.text ( 'attribut:' , al='left' , width= 142 )
    for i in (0,1):  cmds.setParent( '..')

    cmds.rowColumnLayout(nc =3   )
    cmds.button(l='Add selectet targets', c='an_addTargetsToUI()',w=142 )
    cmds.button(l='Delete space', c='an_deleteSpace()',w=142 )
    cmds.button(l='Make / Edit space', c='makeEditSpace()',w=142 )
    cmds.showWindow()

def makeEditSpace():
    controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True)
    object = cmds.textFieldButtonGrp ('TFBG_object', q=True, tx=True)
    spaceType = {1:'parent', 2:"point", 3:"orient", 4:"scale"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    targetList=[]

    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:
        filds = cmds.rowColumnLayout (Layout,  q=True, ca=True)[1:]
        targetList.append([cmds.textField(filds[0], q=True, tx=True), cmds.textField(filds[1], q=True, tx=True)])

    classObj = AnSpace( controller, object, targetList, spaceType=spaceType)
    classObj.rebildSpaceObj()








