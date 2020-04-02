
from anProcedures import *
from CharacterNames import CharacterNames as chn
from an_classControllers import AnControllers  as ctrl

'''
        AnTwSegment()
        
metods:
    -makeTwSegment()
    -makeGrp()
    -delGrp()
    -makeCurve()
    -delCurve()
    -makeControllers()
    -makeJoints()
    -makeJntStretching()
    -makeJntTwist()
    -makeGeo ()
    -printAttr()
    
additionalProcedurs:
    -aimJntTwSegment()     joint whethe aimConstrant
    -upAimConstraint()     joint whethe one axis aimConstrant 
 
self= AnTwSegment( 'l_upKegTw', baseObjects= ['l_upLeg_jnt','l_lowLeg_jnt'], parentObj= 'pivotOffset_CT')

self.makeTwSegment()

self.printAttr()
'''

class AnTwSegment():
    
    def __init__ (self, name, baseObjects, parentObj= ''): 
        
        self.name = name # prefix
        self.baseObjects = baseObjects
        #grp
        self.rigGrp= ''
        self.parentObj= parentObj  # parent rig grp to it
        self.scaleGrp = self.parentObj      # connect scale setting to it
        #curve               
        self.curve= ''
        self.curvePointsNum = 3  
        #controls
        self.startCt = False 
        self.endCt = False 
        self.ctList = [] 
        self.clastersList = []
        #joint 
        self.jntList = [] 
        self.jntNum =  5
        self.stretchable = True
        self.ikHandl = []
        self.stNodes=[]        #stretch nodes
        #twSys
        self.twObj = baseObjects
        self.twAxis = ['z', 'z']   # 'y'  or  'z'  
        #geo
        self.geo=True
        self.subAx = 10
        self.subAy = self.jntNum
        
    def makeTwSegment(self):
        self.makeGrp()
        self.makeCurve()
        self.makeControllers()
        self.makeJoints ()
        self.makeJntStretching()
        self.makeJntTwist()
        self.makeGeo ()
        
    def makeGrp(self):
        self.rigGrp = cmds.group (em=True, n=self.name+'TwJnt_grp')
        if self.parentObj: cmds.parent(self.rigGrp, self.parentObj)
        cmds.parentConstraint(  self.baseObjects[0], self.rigGrp,  mo=False)

    def delGrp(self): cmds.delete (self.rigGrp)
    
    def makeCurve(self):
        distans= an_distans (self.baseObjects[0], self.baseObjects[1])/(self.curvePointsNum-1)
        pos = [ [x*distans, 0,0]  for x in range(self.curvePointsNum)  ]
        self.curve = cmds.curve(n=self.name+'_crv' , d=2, p=pos)
        cmds.parent(self.curve, self.rigGrp)  
        cmds.setAttr (self.curve+".inheritsTransform", 0)
        cmds.delete  ( cmds.pointConstraint(self.baseObjects[0], self.curve ,  mo=False ))  
        cmds.delete  ( cmds.aimConstraint(self.baseObjects[1], self.curve , aim=[1,0,0],  mo=False )) 
        cmds.makeIdentity (apply=True, t=1, r=1, s=1, n=0, pn=1)
        an_connectRigVis (self.rigGrp, [self.curve,])
          
    def delCurve(self): cmds.delete (self.curve)

    def makeControllers(self):
        for i in range(self.curvePointsNum):
            clast=cmds.cluster ( self.curve + '.cv['+str(i)+']', n = self.name+str(i)+'_clst' )[1] 
            self.clastersList.append (clast) 
            ctObj = ctrl(self.name+str(i)+'_CT').makeController ( 'circle', size=2,  orient="X",   pos=clast, posType='point')
            self.ctList.append (ctObj)
            cmds.parent(ctObj.oriGrp, self.rigGrp)
            cmds.setAttr (ctObj.oriGrp+".r", 0,0,0)
            cmds.parent(clast, ctObj.name)
            if not i==0: 
                weight = 1.0/(self.curvePointsNum-1)*i                
                constr = cmds.pointConstraint(  self.baseObjects[0], self.baseObjects[1], self.ctList[i].oriGrp,  mo=False)[0]
                cmds.setAttr (constr+ "."+ self.baseObjects[0]+ "W0",  1-weight)
                cmds.setAttr (constr+ "."+ self.baseObjects[1]+ "W1",  weight) 
        for i, ctState in zip ([0, -1],  [self.startCt,  self.endCt]  ): # for ens controllers
            if not ctState: 
                cmds.parent(self.clastersList[i], self.ctList[i].conGrp)
                cmds.delete (self.ctList[i].name)       
        an_connectRigVis (self.rigGrp,  self.clastersList )
                        
    def makeJoints (self):  
        cmds.select (cl=True)   
        xPos  = cmds.arclen(self.curve, constructionHistory = False) / self.jntNum   
        for i in  range(self.jntNum+1): 
            jnt = cmds.joint (r=1, n=self.name+'Tw0'+str(i)+'_jnt', p= [xPos , 0, 0])
            self.jntList.append(jnt)
        self.ikHandl  =  cmds.ikHandle  (n=self.name+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=self.jntList[0], ee= self.jntList[-1], c=self.curve)[0]
        cmds.parent(self.jntList[0], self.ikHandl,   self.rigGrp) 
        an_connectRigVis (self.rigGrp,  [self.ikHandl,] )       

    def makeJntStretching(self):
        curvLength  = cmds.arclen(self.curve, constructionHistory = True) 
        xScaleMDVnod = cmds.createNode ('multiplyDivide', n= self.name+'ScaleMDV')
        cmds.connectAttr (curvLength+'.arcLength',  xScaleMDVnod+'.input1X')
        cmds.connectAttr (self.scaleGrp+'.sx',  xScaleMDVnod+".input2X")
        cmds.setAttr (xScaleMDVnod+".operation", 2)
        jntPosMDVnod = cmds.shadingNode ('multiplyDivide', n=self.name+'jPosMDV',  asUtility=True)
        cmds.setAttr (jntPosMDVnod+".operation", 2)
        cmds.connectAttr (xScaleMDVnod+'.outputX', jntPosMDVnod+'.input1X')
        cmds.setAttr (jntPosMDVnod+".input2X", self.jntNum )
        for index in range(self.jntNum +1):   cmds.connectAttr (jntPosMDVnod+'.outputX',  self.jntList[index]+'.tx')
        for x in [xScaleMDVnod, jntPosMDVnod]: self.stNodes.append (x)
        
    def makeGeo (self):  
        geo, madeNod = cmds.polyCylinder (r=cmds.arclen(self.curve)/self.jntNum *0.2, h=cmds.arclen(self.curve), sx=self.subAx, sy=self.jntNum, sz=0, ax=[1,0,0], rcp=0, cuv=3, ch=1, n=self.name+'Tw_geo' ) 
        cmds.delete (cmds.pointConstraint (self.jntList[0], self.jntList[-1], geo))
        cmds.delete (cmds.aimConstraint (self.jntList[0], geo))
        cmds.skinCluster(self.jntList[:-1],  geo, tsb=True, )
        cmds.setAttr (madeNod+ ".radius", cmds.arclen(self.curve)/self.jntNum *1.2)
        cmds.setAttr (geo+".inheritsTransform", 0)
        cmds.parent(geo, self.rigGrp)    
        self.geo=geo
    
    def makeJntTwist(self): 
        upVectSt = {'y':[0,1,0], 'z':[0,0,1]}[self.twAxis[0]]
        cmds.aimConstraint(self.clastersList[1] , self.clastersList[0] , aim=[1,0,0], u=upVectSt, wu=upVectSt, wut='objectrotation', wuo=self.twObj[0])
        upVectEnd = {'y':[0,1,0], 'z':[0,0,1]}[self.twAxis[1]]
        cmds.aimConstraint(self.clastersList[-2] , self.clastersList[-1] , aim=[-1,0,0], u=upVectEnd, wu=upVectEnd, wut='objectrotation', wuo=self.twObj[1])
        cmds.setAttr (self.ikHandl+".dTwistControlEnable", 1)
        cmds.setAttr (self.ikHandl+".dWorldUpType", 4)  
        cmds.connectAttr (self.clastersList[0]+".worldMatrix[0]", self.ikHandl+".dWorldUpMatrix")   
        cmds.connectAttr (self.clastersList[-1]+".worldMatrix[0]", self.ikHandl+".dWorldUpMatrixEnd")          
        cmds.setAttr (self.ikHandl+".dWorldUpAxis", 3)
        cmds.setAttr (self.ikHandl+".dWorldUpVector", 0, 0, 1 ) 
        cmds.setAttr (self.ikHandl+".dWorldUpVectorEnd", 0, 0, 1)  

    def printAttr (self):
        print '--------------------------------------------------------------------------------------------------'
        attrList = ['name', 'baseObjects', 'rigGrp', 'parentObj', 'scaleGrp', 'curve', 'curvePointsNum', 'startCt', 'endCt', 'ctList', 'clastersList', 'jntList', 'jntNum', 'stretchable', 'ikHandl', 'stNodes', 'twObj', 'twAxis', 'geo', 'subAx', 'subAy']
        for attr in  attrList: 
            print attr, ':', self.__dict__[attr]   

############################################################################################################

    def addElbowTypeController (): pass

#ctJnt, endJnt = cmds.ls(sl=True)
def aimJntTwSegment(ctJnt, endJnt): # joint whethe aimConstrant
    pfx=chn(ctJnt).divideName()[0]+chn(ctJnt).divideName()[1]
    upAx = 'Z'
    length = an_distans( ctJnt, endJnt)
    cmds.select(cl =True  )
    twJnt = cmds.joint( n= pfx+'_jnt')
    twJntEnd = cmds.joint( n= pfx+'End_jnt', p=[length,0,0])
    rigGrp=cmds.group( n=pfx+'Rig_ori', em=True)
    cmds.parent(twJnt, rigGrp)
    upVect = {'Z':[0,0,1], 'Y':[0,1,0]}[upAx]
    cmds.pointConstraint(ctJnt, rigGrp, mo=False)
    cmds.aimConstraint(endJnt, twJnt, aim=[1,0,0], u=upVect, wu=upVect, wut='objectrotation', wuo=ctJnt)
    cmds.pointConstraint(endJnt, twJntEnd, mo=False)

#objForSysParent, aimObj = cmds.ls(sl=True)
def upAimConstraint(aimObj, objForSysParent):
    dir = {'x':(1.0,0,0), 'y':(0,1.0,0), 'z':(0,0,1.0) ,  '-x':(-1.0,0,0), '-y':(0,-1.0,0), '-z':(0,0,-1.0) }
    upAx = dir['x']
    aim = dir['z']
    pfx=chn(objForSysParent).divideName()[0]+chn(objForSysParent).divideName()[1]
    aimLoc = cmds.spaceLocator(n=pfx+'Aim_loc')[0]
    cmds.select(cl =True  )
    twJnt = cmds.joint( n= pfx+'1Axis_jnt')
    cmds.parent(aimLoc, twJnt, objForSysParent)
    cmds.setAttr (aimLoc+".translate", 0, 1, 0)
    cmds.setAttr (aimLoc+".localScale", 0.1, 0.1, 0.1)
    cmds.setAttr (aimLoc+".v", 0)
    cmds.setAttr (twJnt+".translate", 0, 0, 0)
    cmds.aimConstraint(aimLoc, twJnt, aim=[0,0,1], u=upAx, wu=upAx, wut='object', wuo=aimObj)
    
            