# 03.04.2019   add mirowSolvVal()
# 09.03.2019   ui 
# 01.02.2019   add madeControlSimple() - edit 
# 15.01.2019   add madeControlSimple() - hide fraim shape in control from sel grp 
# 9.01.2019    create proc createFingersSys()      
# 9.01.2019    add return function to mirrorJCSystem()

from  anProcedures import  *
from an_classControllers import AnControllers as ctrl
from CharacterNames import CharacterNames as chn

'''
selbend, selUp = cmds.ls(sl=1)
dirJntList={'Y':('y', '-y'), }
self = JntCorrectiveSys().createBlok('l_earDw', selbend, selUp, dirJntList, 0.1  )
if mirror: self.mirrorJCSystem()
'''


'''
JntCorrectiveSys()
    Attributes:
        - pfx              
        - gScale                         #object for global scale
        - ct                             #locator
        - baseObj                        #object for solver parenting
        - baseUpObj                      #object for up joint grp parenting
        - baseEndObj                     #object for connecting skin systems  
        - sysGrp
        - upGrp
        - bendGrp
        - slvGrp
        - directionsList                 # list of oll directions in sistem
        - jointList                      # list of oll joints in sistem
                            
    Metods:
        
    ---- Criate correction sys:______________________
        -JCSystem ()                     # criating correct systems 
        -addDraftDir() 
        -createDir()
        -simpleDir () 
        -delDir()
        -addJnt()
        -createBlok()                    # criate JCS and set of dirrectionc and joint
        -createBlokAndLoadSettings
        -createBipedalSys()
        -createFingersSys():             # JntCorrectiveSys().createFingersSys(jnts='', gScale = 0.1, mirror=True) 
        #-createQadroSys()
        
    ---- Save/load JCS settings:______________________
        -getDirSettings()
        -getJntSettings()
        -setDirSettings()
        -setJntSettings()     
        -saveSysSettings()
        #-loadJcsSetings()   
        
    ---- Mirror correction sys: ______________________
        -mirrorObg()                     # aksillary proc for mirror 
        -mirrorJCSystem()                # need joint name list correction in r side !!!!!!!!!!!!!!!!!!!!!!!!!!
        -mirrorDir ()
        -existTest()                     #test for existing jnt and direktion
        -mirrorJnt() 
        #-mirrorSettings ()
        -getDataFromGrp  ()              # get attributes from 'rigGrp.data' attribut 
        #-JCSystemFromUi ()
        
    ----Additional metods:______________________
        -madeControlSimple()             #hide fraim shape in control from sel grp    JntCorrectiveSys().madeControlSimple()
        -mirowSolvVal()                  # mirow solvers val  JntCorrectiveSys().mirowSolvVal()
        #-reconnectJCS()
        -connectJCStoScaleCT()
        -getDataFromGrp ()
        -printAttr ()
        -JCS_ui ()                       #JntCorrectiveSys().JCS_ui()
'''

class JntCorrectiveSys(): # JCS_grp
    def __init__ (self, name=''): 
        self.pfx = name+'CS'          
        self.gScale = 1
        self.ct = ''
        self.baseObj= ''              #object for solver parenting
        self.baseUpObj= ''            #object for up joint grp parenting  
        self.sysGrp= self.pfx+'Rig_grp'
        self.upGrp=self.pfx+'Up_grp'
        self.bendGrp=self.pfx+'Bend_grp'
        self.slvGrp=self.pfx+'Solver_grp'
        self.directionsList = []
        self.jointList = [] 
        self.existTest()

    '''******* criating correct systems     ************************************************************************************************************************************'''
    def JCSystem (self):  ###########################################
        for grp in [self.sysGrp,  self.upGrp, self.bendGrp, self.slvGrp]: cmds.group(em=True, n=grp)
        self.ct = ctrl(self.pfx+'_ctrl')
        self.ct.makeController( "kross", 0.5*self.gScale )
        cmds.parent (self.ct.oriGrp,   self.slvGrp )
        cmds.parent ( self.upGrp, self.bendGrp, self.slvGrp, self.sysGrp)
        for grp in  [self.upGrp, self.bendGrp, self.slvGrp]: cmds.delete (cmds.parentConstraint (self.baseObj, grp, mo=False))
        cmds.delete (cmds.orientConstraint (self.baseUpObj, self.upGrp, mo=False))
        cmds.setAttr (self.ct.name+".translateX", 1*self.gScale)
        cmds.parent ( self.ct.name,   self.sysGrp)
        cmds.delete(self.ct.oriGrp)
        for grp in  [self.upGrp, self.slvGrp]: cmds.parentConstraint (self.baseUpObj, grp, mo=True)
        for grp in  [self.ct.name, self.bendGrp]: cmds.parentConstraint (self.baseObj, grp, mo=True)
        self.ct = self.ct.name
        an_saveLoadData(data=[self.__dict__], obgect=self.sysGrp)

    '''******* criating draft solver'''
    def addDraftDir(self,  axis = 'y'):
        dir = an_unicName (self.pfx, '_dir' , num=True)[0]  
        dirCt = dir[:-4]+'_ctrl'
        cmds.group (em=True, n = dir)
        objCT = ctrl( dirCt).makeController(shapeType='JCSCT', size=2.5*self.gScale) ##-------------------------------------------------------------------------------------------
    
        for attrS, attrT, val in ([ 'orbitPoz', 'tz', 0], ['width', 'sz', 1.25], ['lengthOffset', 'tx', 0], ['lengthSize', 'sx', 1.25]):
            cmds.addAttr   (dirCt, ln=attrS, dv=val,  keyable = True)
            cmds.connectAttr  (dirCt+'.'+attrS,  dirCt+'.'+attrT)
        objCT.hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        cmds.xform (dirCt, os=True, piv=[0, 1*self.gScale, 0])
        
        tmpPlane = cmds.nurbsPlane (p= [0, 1*self.gScale, 0], ax= [0, -1, 0], w=3.14*self.gScale, lr=2, d=3, u=6, v=10, ch=0, n= dir[:-4]+'Template_geo')
        cmds.setAttr (tmpPlane[0]+".template", 1)
        seursePlane = cmds.nurbsPlane (p= [0, 1*self.gScale, 0], ax= [0, -1, 0], w=2.5*self.gScale, lr=1, d=3, u=10, v=10, ch=0, n=dir[:-4]+'dirPlane_geo')
        for attr in [".translate", ".scale"]: cmds.connectAttr  (dirCt+attr,  seursePlane[0]+attr)
        cmds.setAttr ( seursePlane[0] +".rotate", 0, 180, 00)
        cmds.makeIdentity( seursePlane[0], apply=True, rotate=True )
        bendDefA = cmds.nonLinear ( tmpPlane[0] , dirCt, seursePlane, type='bend', highBound=1.57, lowBound=-1.57, curvature=1)
        bendDefA[1] = cmds.rename(bendDefA[1], dir+'BendA_def')
        cmds.setAttr ( bendDefA[1] +".rotate", 0, 0, -90)
        cmds.setAttr ( bendDefA[1] +".scale", 1*self.gScale, 1*self.gScale, 1*self.gScale)
        bendDefB = cmds.nonLinear ( tmpPlane[0], dirCt, seursePlane,  type='bend', highBound=20, lowBound=-20, curvature=1)
        bendDefB[1] = cmds.rename(bendDefB[1], dir+'BendB_def')
        for attr, val in zip (['tx','ty','tz','rx','ry','rz','sx','sy','sz'], [0, 1*self.gScale, 0, -90, 0, -90, 1*self.gScale, 1*self.gScale, 1*self.gScale]):
            cmds.setAttr ( bendDefB[1] +"."+attr,  val)
        for bend in [bendDefA, bendDefB]: cmds.setAttr ( bend[0] +".curvature",  57.3)
        cmds.parent (bendDefB[1], bendDefA[1], tmpPlane[0], seursePlane, dirCt, dir)
        cmds.xform (os=True, piv=[0, 0, 0])
        for obj in [bendDefB[1], bendDefA[1], seursePlane[0]]: cmds.setAttr (obj+".v", 0)
         
        cmds.parent (dir, self.slvGrp)
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']: cmds.setAttr (dir+'.'+attr, 0)
        cmds.setAttr (dirCt+'.orbitPoz', {'y': 0, '-y':3.1415, 'z':1.57, '-z':-1.57 } [axis]*self.gScale )
        cmds.select ( dirCt, r=True) 
        cmds.delete (objCT.oriGrp) 
        cmds.xform (dirCt, ws=True, piv=cmds.xform (self.baseObj, q=True,  ws=True, t=True)) #pivot to jnt
        cmds.xform (seursePlane, ws=True, piv=cmds.xform (self.baseObj, q=True,  ws=True, t=True)) #pivot to jnt
        return  dirCt

    '''******* criating difficult solver'''
    def createDir (self, dirCt=''):
        
        if not dirCt: dirCt = cmds.ls (sl=True)[0]
        pfx = dirCt[:-5]
        tmpPlane, seursePlane, dirName = pfx+'Template_geo', pfx+'dirPlane_geo',  pfx+'_dir'
        for obj in [dirCt, seursePlane, tmpPlane]: cmds.delete(obj, ch=True )# del history
        cmds.delete(tmpPlane)
        ctrl(dirCt).showTransAttrs()
        for attrS, attrT in ([ 'orbitPoz', 'tz'], ['width', 'sz'], ['lengthOffset', 'tx'], ['lengthSize', 'sx']):
                cmds.disconnectAttr  (dirCt+'.'+attrS,  dirCt+'.'+attrT)
        for attr in [".translate", ".scale"]: cmds.disconnectAttr  (dirCt+attr,  seursePlane+attr)
        cmds.connectAttr  (dirCt+".rotate",  seursePlane+".rotate")
        ctrl(dirCt).hideAttr(['orbitPoz', 'width', 'lengthOffset', 'lengthSize','tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        
        for attr in ( 'val',  'multiplier',  'resultVal'  ):
            cmds.addAttr  (dirCt,  ln=attr, dv=10, keyable=True)
        nodes = self.connectDirToLoc( self.ct, seursePlane, dirCt, pfx)
        
        an_delSys(dirName, nodes)
        cmds.select ( dirCt, r=True)
        self.directionsList.append(dirCt)
        self.existTest()
        an_saveLoadData(data=[self.__dict__], obgect=self.sysGrp)
        return dirName
        
    def delDir(self, dirName): 
        an_delSys(dirName)

    '''******* criating simple solver '''
    def simpleDir (self, axis = 'y'):
        dir = an_unicName (self.pfx, '_dir' , num=True)[0] # define name
        dirCt = dir[:-4]+'_ctrl'
        pfx = dirCt[:-5] 
        cmds.group (em=True, n = dir)
        
        objCT = ctrl( dirCt).makeController(shapeType='curvedArrow', size=1*self.gScale, orient="X" )  # made controller
        objCT.rotateCt ([  {'z':0, 'y':-90, '-z':180, '-y':90}[axis]  , 0, 0])               
        for child, paren in ([dirCt, dir], [dir, self.slvGrp]) : cmds.parent (child, paren, s=True, r=True)                          
        cmds.delete(objCT.oriGrp)
        
        nodes = self.connectSimpleDirToLoc(objCT.name, self.baseObj, pfx)
        
        objCT.hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        an_delSys(dir, nodes)
        cmds.select ( dirCt, r=True)
        self.directionsList.append(dirCt)
        self.existTest()
        an_saveLoadData(data=[self.__dict__], obgect=self.sysGrp)
        return dir
    
    '''******* add jnt and connect to solver'''
    def addJnt(self, dirCt='', jntType='bend', axis='y'): 
    
        xOffset = 0.05*self.gScale    # joint offset
       
        if not dirCt: dirCt = cmds.ls (sl=True)[0]
        if jntType == 'bend': parentObj, parentGrp  = self.baseObj, self.bendGrp
        else:                 parentObj  , parentGrp  =  self.baseUpObj, self.upGrp
        
        jntPfx = an_unicName (chn(parentObj).sfxMinus(), '_jnt', num=True)   [0] [:-4]      
        cmds.select (cl=True)
        rtJnt = cmds.joint (n = jntPfx+'Ori_jnt', p=[0,0,0])
        jnt = cmds.joint (n = jntPfx+'_jnt', p=[0,  1*self.gScale, 0])
        cmds.parent (rtJnt, self.bendGrp , relative=True)
        
        if not jntType == 'bend': cmds.setAttr (rtJnt+'.tx',   -1*xOffset)
        else: cmds.setAttr (rtJnt+'.tx',   xOffset)       
        
        cmds.setAttr (rtJnt +".rotateOrder", 5 ) 
        cmds.setAttr (rtJnt+'.rx', {'y': 0, '-y':180, 'z':90, '-z':270} [axis])
        if not jntType == 'bend': 
            cmds.parent (rtJnt, parentGrp)
            cmds.setAttr (rtJnt+'.ry', 180)
        cmds.connectAttr (  dirCt+'.resultVal', jnt+'.tx')
        
        self.jointList.append(rtJnt)
        self.existTest()
        an_saveLoadData(data=[self.__dict__], obgect=self.sysGrp)
        return jnt, rtJnt 
    
        '''******* criate JCS and set of dirrectionc and joint''' 
    def createBlok(self,  name, baseObj, baseUpObj, dirJntList={'Z':('z','-z')}, gScale = 1) : # 'Y' key val- if direction is complicated, 'y'-simple  

        self  = JntCorrectiveSys(name)
        self.baseObj, self.baseUpObj= baseObj, baseUpObj 
        self.gScale=gScale
        self.JCSystem ()  
        
        for dir in dirJntList.keys():
            dirName =''
            if dir in ('Y', '-Y', 'Z', '-Z'): dirName = self.createDir(self.addDraftDir(dir.lower()))
            if dir in ('y', '-y', 'z', '-z'): dirName = self.simpleDir (dir)
            for ax in dirJntList[dir]:
                for typeJnt in ('bend', 'up'):
                    jnt, rtJnt = self.addJnt( dirName.replace('_dir', '_ctrl' ), typeJnt, ax)
                    if not dir.lower()==ax: 
                        cmds.setAttr (rtJnt+'.ry', cmds.getAttr (rtJnt+'.ry')-180)
        return self
        
        
        '''*******         '''

    def createBlokAndLoadSettings(data):
        sysData, dirData, jntData = data
        sys=JntCorrectiveSys(sysData['pfx'][:-2]) # create sys
        for attr in sysData.keys():
            setattr(sys, attr, sysData[attr])
        sys.JCSystem ()
        for i in range(len(sysData['directionsList'])):  
            pass
            draftData = dirData[i]
            dirCt=sys.addDraftDir()
            sys.setDirSettings(dirCt.replace('_ctrl', '_dir'), dirData[i][0])  
                    
    def createBipedalSys(self, gScale = 0.3, mirror=False):
        # hand  
        dirJntList={'Z':('z',),  '-Z':('-z',), 'Y':('y',),  '-Y':('-y',)}
        self = JntCorrectiveSys().createBlok('l_hand', 'l_hand_bind', 'l_armBendDw7_jnt', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        # elbow   
        dirJntList={'Z':('z', '-z'), }
        self = JntCorrectiveSys().createBlok('l_elbow', 'l_armBendDw0_jnt', 'l_armBendUp7_jnt', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        #shoulder  
        dirJntList={'Z':('z',),  '-Z':('-z',), 'Y':('y',),  '-Y':('-y',)}
        self = JntCorrectiveSys().createBlok('l_shoulder', 'l_armBendUp0_jnt', 'l_shoulder_bind', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        #hips 
        dirJntList={'Z':('z',),  '-Z':('-z',), 'Y':('y',),  '-Y':('-y',)}
        self = JntCorrectiveSys().createBlok('l_hip', 'l_legBendUp0_jnt', 'l_hip_jnt', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        # knee  
        dirJntList={'Y':('y', '-y'), }
        self = JntCorrectiveSys().createBlok('l_knee', 'l_legBendDw0_jnt', 'l_legBendUp7_jnt', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        # foot 
        dirJntList={'Y':('y',), '-Y':('-y',) }
        self = JntCorrectiveSys().createBlok('l_foot', 'l_foot_bind',  'l_legBendDw7_jnt',  dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()
        # toe
        dirJntList={'Y':('y',), '-Y':('-y',) }
        self = JntCorrectiveSys().createBlok('l_toe', 'l_toe_bind', 'l_foot_bind', dirJntList, gScale  )
        if mirror: self.mirrorJCSystem()

    def createFingersSys(self, jnts='', gScale = 0.1, mirror=False): # criate JCS and set of dirrectionc and joint
        if not jnts: jnts = cmds.ls (sl=True)
        rigGrp = cmds.group(n='fingersCS_grp', em=True)
        cmds.addAttr  (rigGrp,  ln="l_multiplier", dv=10, keyable=True)
        cmds.addAttr  (rigGrp,  ln="r_multiplier", dv=10, keyable=True)
          
        for jnt in jnts:   
            parentJnt=cmds.listRelatives(jnt, p=True)[0]
            dirJntList={'y':('y', '-y'), }
            self = JntCorrectiveSys().createBlok(chn(jnt).sfxMinus(), jnt, parentJnt, dirJntList, gScale )
            cmds.parent (self.sysGrp, rigGrp)
            controls = self.directionsList[0].replace('_dir', '_ctrl')
            cmds.connectAttr(rigGrp+".l_multiplier",  controls+".multiplier")
            if mirror:
                rRigGrp =  self.mirrorJCSystem()
                cmds.parent (rRigGrp, rigGrp)
                controls = 'r_'+self.directionsList[0].replace('_dir', '_ctrl')[2:]
                cmds.connectAttr(rigGrp+".r_multiplier",  controls+".multiplier")

    '''******* Save/load JCS settings:    ************************************************************************************************************************************'''
    
    def getDirSettings(self, dirIn=''):  # dirIn - dirGrp or controls
    
        if not dirIn: 
            dirIn = cmds.ls (sl=True)[0]            
        pfx = dirIn[:-4]  if '_dir' in  dirIn  else dirIn[:-5]
   
        contr = pfx+'_ctrl'
        dirAttr =  'val', 'multiplier', 'resultVal', 'orbitPoz', 'width', 'lengthOffset',  'lengthSize', 'sx',  'sz', 'sy', 'rx', 'ry', 'rz',
        atrVal = {}
        for attr in dirAttr:    atrVal[attr] = cmds.getAttr(contr+'.'+attr) 
        #get ct shape 
        ctCoord=[]
        sourseShape = cmds.listRelatives(contr, s=True)     # get curve shape
        for i in xrange(len(sourseShape)):
            vPointsNum = cmds.getAttr (sourseShape[i]+'.spans')+cmds.getAttr (sourseShape[i]+'.degree')   # get curve points number
            curvCoord=[]
            for pn in xrange(vPointsNum): 
                pos =cmds.xform(sourseShape[i]+'.controlPoints['+str(pn)+']',  q=True, t=True, ws=True)
                curvCoord.append(pos)
            ctCoord.append(curvCoord)
        #get geo shape
        shape = cmds.listRelatives(pfx+'dirPlane_geo', s=1)[0]
        pCoord=[]
        for upn in xrange(13):
            for vpn in xrange(13):
                pos =cmds.xform(shape+'.cv['+str(upn)+']['+str(vpn)+']',  q=True, t=True, ws=True )
                pCoord.append(pos)
        return atrVal, ctCoord, pCoord
            
    def getJntSettings(self, jntRt=''):
        if not jntRt: jntRt = cmds.ls (sl=True)[0]
        jntEnd = cmds.listRelatives(jntRt, c=True)[0]
        attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'jointOrientX', 'jointOrientY', 'jointOrientZ']
        out = {}
        connection={}
        for jnt in [jntRt, jntEnd]: 
            trDik={}
            for attr in attrList: 
                trDik[attr] = cmds.getAttr( jnt+'.'+attr)
                if cmds.connectionInfo( jnt+'.'+attr, isDestination=True): 
                    connection[jnt+'.'+attr]= cmds.connectionInfo( jnt+'.'+attr, sourceFromDestination=True)     
            out[jnt]= trDik
            out['connection']= connection          
        return out
        
    def setDirSettings(self, dirName, data):  
        #dirName = 'l_shoulderCS03_dir'
        atrVal, ctCoord, pCoord = data 
        pfx = dirName[:-4]
        contr = pfx+'_ctrl'
        #set attr val
        dirAttr = 'multiplier', 'orbitPoz', 'width', 'lengthOffset',  'lengthSize', 'sx',  'sz', 'sy', 'rx', 'ry', 'rz',
        for attr in atrVal:  # set attr
            if cmds.objExists(contr+'.'+attr): 
                attrLoc = False
                if cmds.getAttr(contr+'.'+attr,  l=True ):
                    cmds.setAttr(contr+'.'+attr, l=False)
                    attrLoc = True
                if not cmds.connectionInfo( contr+'.'+attr, isDestination=True):    
                    cmds.setAttr(contr+'.'+attr, atrVal[attr]) 
                    print contr+'.'+attr, '  ', atrVal[attr]
                if attrLoc: cmds.setAttr(contr+'.'+attr, l=True) 
        #set ct shape  
        sourseShape = cmds.listRelatives(contr, s=True)     # get curve shape
        for i in xrange(len(sourseShape)): 
            for pn in xrange(len(data[1][i])): 
                pos = data[1][i][pn]
                cmds.xform(sourseShape[i]+'.controlPoints['+str(pn)+']', t=[pos[0], pos[1], pos[2] ], ws=True )            
        #get geo shape
        i=0
        shape = cmds.listRelatives(pfx+'dirPlane_geo', s=1)[0]
        for upn in xrange(13):
            for vpn in xrange(13):
                pos = data[2][i]
                i+=1
                cmds.xform(shape+'.cv['+str(upn)+']['+str(vpn)+']', t=[pos[0], pos[1], pos[2] ], ws=True )
        
        def setJntSettings(self, data):
            for jnt in data.keys():
                for attr in data[jnt]: 
                    cmds.setAttr( jnt+'.'+attr, data[jnt][attr])
                    print  attr, data[jnt][attr]
            connection = data.pop('connection') 
            for con in connection.keys(): cmds.connectAttr( connection[con], con)
            
    def saveSysSettings(self, sys, toFile=False): 
        obj = JntCorrectiveSys( sys[:-9] )
        sysData = an_saveLoadData(obgect=sys)[0]
        
        dirData, jntData = [], []
        #for derect in obj.directionsList:
        for derect in sysData['directionsList']:
            dirData.append( JntCorrectiveSys().getDirSettings(derect))
            
        #for jnt in obj.jointList: 
        for jnt in sysData['jointList']:
            jntData.append( JntCorrectiveSys().getJntSettings(jnt))
        if toFile: an_saveLoadData(data=[sysData, dirData, jntData], obgect='' )
        else: return  sysData, dirData, jntData

    '''******* mirror System     ************************************************************************************************************************************'''
    def mirrorJCSystem(self): 

        data = an_saveLoadData(obgect=self.sysGrp) [0]   # solve right names
        for attr in self.__dict__.keys():  
            if (type (self.__dict__[attr]) in (unicode, str)) :  
                if self.__dict__[attr][0:2]=='l_':  data[attr] = 'r_'+ self.__dict__[attr][2:]
                
        for grp in [data['sysGrp'], data['upGrp'], data['bendGrp'], data['slvGrp']]: cmds.group(em=True, n=grp )
        r_ct = ctrl(data['ct'])
        r_ct.makeController( "kross", 0.5*self.gScale )
        cmds.parent(data['upGrp'], data['bendGrp'], data['slvGrp'], r_ct.name,  data['sysGrp']) 
        cmds.delete(r_ct.oriGrp)
                
        for obj in ['upGrp','bendGrp', 'slvGrp', 'ct']:     JntCorrectiveSys().mirrorObg( data[obj],  an_saveLoadData(obgect=self.sysGrp)[0][obj])
        for grp in  (data['upGrp'], data['slvGrp']): cmds.parentConstraint (data['baseUpObj'], grp, mo=True)
        for grp in  (data['ct'], data['bendGrp']): cmds.parentConstraint (data['baseObj'], grp, mo=True)   
        
        for dir in self.directionsList:
            self.mirrorDir(dir.replace ('_dir', '_ctrl'))
            
        for jnt in self.jointList:
            self.mirrorJnt(jnt)
        
        return data['sysGrp'] 
        

    def mirrorDir(self, lCtrl=''):
    
        if not lCtrl: lCtrl = cmds.ls (sl=True)[0]   
        lPfx, rPfx = lCtrl[:-5],  lCtrl[:-5].replace ('l_', 'r_')
        
        # if direction is complicated
        if  [True for x in cmds.listRelatives(lCtrl.replace('_ctrl', '_dir'), c=True) if 'dirPlane' in x]:   
            rDir, planeGeo, rCtrl = cmds.duplicate( lCtrl.replace ('_ctrl', '_dir') ,rc=True) # duplicate dir grp
            rDir, planeGeo, rCtrl =[cmds.rename(x, x.replace ('l_', 'r_')[:-1]) for x in [rDir, planeGeo, rCtrl]]
            cmds.parent( rDir , rPfx[:-2]+'Solver_grp')
            for d in ['.t', '.r']: cmds.setAttr(rDir+d, 0, 0, 0)
                # 2  mirrow shape
            ctrl(lCtrl).mirrorShape( rCtrl)
            sourseShape = cmds.listRelatives(lPfx+'dirPlane_geo', s=True)[0]
            targShape = cmds.listRelatives(rPfx+'dirPlane_geo', s=True)[0]
            for upn in xrange(13):
                for vpn in xrange(13):
                    pos =cmds.xform(sourseShape+'.cv['+str(upn)+']['+str(vpn)+']',  q=True, t=True, ws=True )
                    cmds.xform(targShape+'.cv['+str(upn)+']['+str(vpn)+']', t=[pos[0]*-1, pos[1], pos[2] ], ws=True )
            nodes = self.connectDirToLoc( self.ct.replace ('l_', 'r_'), planeGeo, rCtrl, rPfx)
            cmds.deleteAttr (rDir+".delList"  )
            cmds.select ( rCtrl, r=True)
        else:
            rDir = cmds.group (em=True, n = rPfx+'_dir')
            objCT = ctrl( rPfx+'_ctrl' ).makeController(shapeType='curvedArrow' )  # made controller
            
            for child, par in ([objCT.name,  rDir], [rDir, rPfx[:-2]+'Solver_grp']): cmds.parent( child, par) 
            cmds.delete(objCT.oriGrp)
            JntCorrectiveSys().mirrorObg( rDir, lPfx+'_dir')
            ctrl(lCtrl).mirrorShape( objCT.name)
            nodes = self.connectSimpleDirToLoc(objCT.name, self.baseObj.replace ('l_', 'r_'), rPfx)
            cmds.select ( objCT.name, r=True)
            objCT.hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        an_delSys(rDir, nodes)

    def mirrorJnt(self, jnt=''):
              
        if not jnt: jnt = cmds.ls (sl=True)[0] 
        lParentGrp = cmds.listRelatives (jnt, p=True)[0]
        parentGrp = lParentGrp.replace ('l_', 'r_')
        cmds.parent (jnt, w=True)
        rtJnt = cmds.mirrorJoint (jnt, mirrorYZ=True,  mirrorBehavior=True, sr= ['l_', 'r_'])[0]
        endJnt = cmds.listRelatives (rtJnt, c=True)[0]
        
        cmds.parent (jnt, lParentGrp)
        cmds.parent (rtJnt, parentGrp,)
              
        for d in ['.tx', '.ty', '.tz']: 
            if cmds.connectionInfo( endJnt.replace ('r_', 'l_')+d, isDestination=True):
                targAttr = cmds.connectionInfo(endJnt.replace ('r_', 'l_')+d, sourceFromDestination=True).replace ('l_', 'r_')
                cmds.connectAttr  (targAttr,  endJnt+'.tx')
        cmds.setAttr (targAttr.replace ('resultVal', 'multiplier') , -10 ) 

    def connectDirToLoc(self, ct, seursePlane, dirCt, pfx): 
        
        vPointOnSurface = cmds.createNode ("closestPointOnSurface", n=pfx+"PointOnSurface")
        cmds.connectAttr  (ct+'.translate',  vPointOnSurface+".inPosition")
        cmds.connectAttr  (cmds.listRelatives ( seursePlane, s=True )[0]+".worldSpace[0]",  vPointOnSurface+".inputSurface")
        
        setRange = cmds.createNode ("setRange", n=pfx+"SetRange")
        cmds.connectAttr  (vPointOnSurface+".parameterV",  setRange+".valueX")
        cmds.setAttr (setRange+".minX", -1)
        cmds.setAttr (setRange+".maxX", 1)
        cmds.setAttr (setRange+".oldMaxX", 1)
        
        multiplyDivide = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide" )
        cmds.setAttr (multiplyDivide+".operation", 3)
        cmds.setAttr (multiplyDivide+".input2X", 2)
        cmds.connectAttr  (setRange+".outValueX",  multiplyDivide+".input1X")
        
        revers = cmds.createNode ("reverse", n=pfx+"Revers")
        cmds.connectAttr (multiplyDivide+'.outputX', revers+'.inputX')
        multiplyDivide2 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide2" )
        cmds.connectAttr ( revers+'.outputX',  multiplyDivide2+'.input1X')
        cmds.connectAttr ( vPointOnSurface+'.parameterU',  multiplyDivide2+'.input2X')
        cmds.connectAttr (  multiplyDivide2+'.outputX', dirCt+'.val')
        
        multiplyDivide3 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide3" )
        cmds.connectAttr ( multiplyDivide2+'.outputX',  multiplyDivide3+'.input1X')
        cmds.connectAttr ( dirCt+'.multiplier',  multiplyDivide3+'.input2X')
        cmds.connectAttr (  multiplyDivide3+'.outputX', dirCt+'.resultVal')
        return  [ vPointOnSurface, setRange, multiplyDivide, revers, multiplyDivide2, multiplyDivide3]
    
    def connectSimpleDirToLoc(self, dirCt, baseObj, pfx):
        for attr in ( 'inStart',  'inEnd', 'val',  'multiplier',  'resultVal'  ):   # clamp input val to nessesery renge
            cmds.addAttr  (dirCt,  ln=attr, dv=0, keyable=True)
        clamp = cmds.createNode ("clamp", n=pfx+"clamp" )
        cmds.connectAttr  (baseObj+".rz",  clamp+".inputR")
        cmds.connectAttr  (dirCt+".inStart",  clamp+".minR")
        cmds.connectAttr  (dirCt+".inEnd",  clamp+".maxR")
         
        sRange = cmds.createNode ("setRange", n=pfx+"setRange" )      # resolve output to renge from 0 to 1
        cmds.connectAttr  ( clamp+".outputR", sRange+".valueX", )
        cmds.setAttr (sRange+".maxX", 1)
        cmds.connectAttr  (dirCt+".inStart",  sRange+".oldMinX")
        cmds.connectAttr  (dirCt+".inEnd",  sRange+".oldMaxX")
        cmds.connectAttr  ( sRange+".outValueX", dirCt+".val", )
        
        multiplyDivide = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide" ) #add multiplaer
        cmds.connectAttr  (dirCt+".val",  multiplyDivide+".input1X")
        cmds.connectAttr  (dirCt+".multiplier",  multiplyDivide+".input2X")
        cmds.connectAttr  (multiplyDivide+'.outputX',  dirCt+".resultVal",)
        cmds.setAttr (dirCt+".multiplier", 10)
        cmds.setAttr (dirCt+".inEnd", 180)
        return [clamp, multiplyDivide, sRange]  

    #JntCorrectiveSys('').JCS_ui()
    
    ''' ----additional metods   ************************************************************************************************************************************'''
    
    
    def madeControlSimple(self, rSide=True):  #JntCorrectiveSys().madeControlSimple()
        sel = cmds.ls(sl=True)
        for rGrp in sel: 
            if cmds.objExists(rGrp+'.data'):
                dirList = an_saveLoadData(obgect=rGrp) [0] ['directionsList']
                for attr in dirList: 
                    ctCurve = cmds.listRelatives (attr.replace('_dir', '_ctrl'), s=True)[0]
                    cmds.setAttr(ctCurve+'.v', 0)
                    if cmds.objExists(attr.replace('_dir', '_ctrl').replace('l_', 'r_')): 
                        ctCurve = cmds.listRelatives (attr.replace('_dir', '_ctrl').replace('l_', 'r_'), s=True)[0]
                        cmds.setAttr(ctCurve+'.v', 0)
    

    def mirowSolvVal(self): 
        sel = cmds.ls(sl=True)
        for rGrp in sel: 
            if cmds.objExists(rGrp+'.data'):
                dirList = an_saveLoadData(obgect=rGrp) [0] ['directionsList']
                for direct in dirList: 
                    solverVal = cmds.getAttr(direct.replace('_dir', '_ctrl')+'.multiplier' )
                    cmds.setAttr(direct.replace('_dir', '_ctrl').replace('l_', 'r_')+'.multiplier', solverVal*-1)
                    print direct.replace('_dir', '_ctrl').replace('l_', 'r_')+'.multiplier', solverVal

    def mirrorObg(self, obj, srs):
        cmds.select (cl=True)
        jnt = cmds.joint()
        cmds.delete (cmds.parentConstraint (srs, jnt))
        mirJnt = cmds.mirrorJoint (jnt, mirrorYZ=True,  mirrorBehavior=True)[0]
        cmds.delete (cmds.parentConstraint (mirJnt, obj), jnt, mirJnt)
   
    def connectJCStoScaleCT(self, ScaleCT='general_CT'):  #JntCorrectiveSys().connectJCStoScaleCT()
        for sys in cmds.ls (sl=True):
            pfx = sys.replace('CSRig_grp', '')
            for grp in (pfx+'CSUp_grp', pfx+'CSBend_grp'): cmds.connectAttr (  ScaleCT+'.s', grp+'.s')
            
    def printAttr (self):
        self.existTest()
        print '--------------------------------------------------------------------------------------------------'
        attrList = ['pfx', 'gScale', 'ct', 'baseObj', 'baseUpObj', 'sysGrp', 'upGrp', 'bendGrp', 'slvGrp', 'directionsList', 'jointList']
        for attr in  attrList: 
            print attr, ':', self.__dict__[attr]  
    
    def existTest(self):
        if cmds.objExists (self.upGrp):
            self.jointList = [obj for obj in  cmds.listRelatives(self.upGrp, c=True )+cmds.listRelatives(self.bendGrp, c=True) if cmds.nodeType (obj) =='joint']
            self.directionsList = [obj for obj in cmds.listRelatives(self.slvGrp, c=True )  if cmds.nodeType (obj) =='transform']
            self.ct=self.upGrp.replace ('Up_grp', '_ctrl') 
            
            sysData = an_saveLoadData(obgect = self.sysGrp)[0]
            self.baseObj = sysData['baseObj']
            self.baseUpObj = sysData['baseUpObj']
          
            
    def getDataFromGrp (self, grp):
        data = an_saveLoadData(obgect=grp) [0] 
        for attr in self.__dict__.keys(): 
            setattr(self, attr, data[attr])
        self.existTest()
    
    def JCSystemFromUi (self): 
        name = cmds.textFieldGrp ('TFBG_Prefix', q=True, tx=True  )
        self = JntCorrectiveSys(name)
        self.gScale = cmds.floatSliderGrp('ISG_gScaleCSys', q=True, v=True  )
        if not cmds.ls (sl=True): cmds.error('Select joints!')
        self.baseObj, self.baseUpObj = cmds.ls (sl=True)
        self.JCSystem () 
        return self

    def JCS_uiComands (self, act=''): 
        name = cmds.textFieldGrp ('TFBG_Prefix', q=True, tx=True  )
        self = JntCorrectiveSys(name)
        self.gScale = cmds.floatSliderGrp('ISG_gScaleCSys', q=True, v=True  )
        
        if act=='sys': pass

    def JCS_ui (self): 
        #step 1
        layouts=an_turnBasedUi('JCS', title =' Joint correction system v.06',  stepsLabel =['Create system', 'Create "dirrection"', 'Add joints'])   
        cmds.setParent (layouts[0])
        cmds.separator  (  style="none")
        cmds.text (l="         Creating a system for calculating the direction and degree of bend", al="left", font= "boldLabelFont")
        cmds.text (l="     - select joint, then up joint.", al="left")
        cmds.text (l="     - to delete a rig, select the group with the system and press \"Delete\"", al="left")
        cmds.text (l="     - to mirror a system, select the group with the system and press \"Mirror\"", al="left")
        cmds.floatSliderGrp('ISG_gScaleCSys', label='Global scale:', field=True, min=0.1, max=10,  v=1 , cw = [(1, 124), (2, 50) ], enable= True )
        bc = "cmds.textFieldButtonGrp ('TFBG_Prefix', e=True, tx= chn(cmds.ls (sl=True)[0]).sfxMinus()  );"
        cmds.textFieldButtonGrp ('TFBG_Prefix', l='Prefix :',  bl="Assign",  cw = [(1, 124), (2, 245)],  bc = bc )
        cmds.rowColumnLayout (nc=3, cw=[(1, 140), (2, 140), (3, 140)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)])   
        cmds.button   (l="Mirror system",  c='an_mirrorSys()')
        cmds.button   (l="Delete system",c="an_delSys (cmds.ls(sl=True)[0])")
        cmds.button   (l="Add system",   c="JntCorrectiveSys().JCSystemFromUi()" )
        #step 2
        cmds.setParent (layouts[1])
        cmds.separator  (  style="none")
        cmds.text (l='         Creating a "direction" for calculating degree of bend', al="left", font= "boldLabelFont")
        cmds.text (l='     - create template, then input options and press Create "direction".', al="left")
        cmds.text (l="     - to delete a direction, select the controller and press \"Delete\"", al="left")
        cmds.text (l="     - to mirror a direction, select controller and press \"Mirror\"", al="left")
        cmds.textFieldButtonGrp ('TFBG_solver', l='System name :',  bl="Assign",  cw = [(1, 124), (2, 245)],  bc = an_TFBGcomand('TFBG_solver') )
        cmds.radioButtonGrp ('RBG_dirType', l="Dirrection type :     ", nrb=2, la2=["Complicated ", "Simple "],  sl=1 )
        cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210) ], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2) ])
        cmds.button   (l='Delete "direction"',c='an_delSys(cmds.listRelatives (cmds.ls (sl=True)[0], p=True)[0])')
        cmds.button   (l='Create template',   c="an_addTemplateDirection()" )
        cmds.button   (l='Mirror "direction"',  c='an_mirrorDir()')
        cmds.button   (l='Create "direction"',   c="an_addDirection()" )
        #step 3 
        cmds.setParent (layouts[2])        
        cmds.separator  (  style="none")
        cmds.text (l='         Add joint and directional dependence', al="left", font= "boldLabelFont")
        cmds.text (l="     - to add a joint, select direction controller and press \"Add joint\"", al="left")
        cmds.text (l="     - to mirror a joint, select root joint and press \"Mirror\"", al="left")
        cmds.radioButtonGrp ('RBG_orient', l="Parent to  :     ", nrb=2, la2=["Bendable joint","Up joint"],  sl=1 )
        cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)])
        cmds.text ('')
        cmds.button   (l="Add joint",   c="an_addJnt()" )
        cmds.setParent ('..')
        cmds.textFieldButtonGrp ('TFBG_dir', l='Controller name :',  bl="Assign",  cw = [(1, 124), (2, 245)],  bc = an_TFBGcomand('TFBG_dir'))
        cmds.rowColumnLayout (nc=3, cw=[(1, 140), (2, 140), (3, 140)], columnSpacing=[(2,2),(3,2)])
        cmds.button   (l='Mirror joint',c= 'an_mirrorJnt()')
        cmds.button   (l='Delete joint',c= 'cmds.delete(cmds.ls(sl=True))')
        cmds.button   (l="Connect to channel",   c="an_connectChannel()" )


