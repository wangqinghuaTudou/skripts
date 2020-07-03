
from an_classNames import  AnNames
#from  anProcedures import  * 
from an_Procedures.utilities import *  
from an_classControllers import  AnControllers  as ctrl

'''
    an_classSkeleton()
Class for storage and create joint structure and names
	
attributes:
    - structure
    - rootJnts    attib need for getJntStructure () 
    - mirowJnt    nirow jnts list 
metods:
    - deleteSkeletonRig()
    - deleteSkeleton()
    - mirrowStructure()             add right side to structure
    - getJntFromIndex():            insert jnt insted its indexes list
    - skeletonRig ()                skeleton template
    - getJntStructure ()            return skeleton hierarhy, jnt pos 
    - getJntInfo ()                 return  pos, ori, child of joint
    - getJntList ()
    - createSceleton ()
    - saveJntStructure ()
    - loadJntStructure ()
    - getChildren()                 get children of jnt
    - getParent()                   get parent of jnt
    - printJntStructure ()
'''


'''
def setSceletonToStructure (self, miror=True):


for jnt in self.getJntList():
    if self.getParent(jnt): 
        cmds.parent( jnt, world=True )

for jnt, pos, ori in self.structure:
    cmds.select (cl=True)
    joinName = cmds.joint(n= jnt.split(' ')[-1], p = pos ) #create jnt
        
for jnt, pos, ori in self.structure:
    jnt = jnt.split(' ')[-1]
    parentJnt = self.getParent( jnt)
    cmds.setAttr(jnt+'.jointOrient', ori[0], ori[1], ori[2], type="double3" )
    if parentJnt: 
        cmds.parent (jnt, parentJnt) 
if miror:
    [cmds.mirrorJoint (x, myz=True,  mb=True, sr= ["l_", "r_"]) for x in  self.mirowJnt ]
    
    #[ self.rootJnts.append( x.replace('l_', 'r_')) for x in self.rootJnts if 'l_' in x]

'''
        #leg 
#self = AnSkeleton()
#self.skeletonRig()
#self.getJntList()  'r_')
#self.getJntFromIndex(([1,0], [49, 5], [48, 6],  [7, 47],   [53, 15 ]    ))
#self.getJntStructure()
#self.createSceleton()
#self.deleteSkeletonRig()
#self.deleteSkeleton()
#self.mirrowStructure()
#self.printJntStructure()
#AnSkeleton().getSkeletonPart('fingers')
    
class AnSkeleton():
    def __init__ (self ):
        self.structure=[    [' hips01_bind', [0.0, 13.0, 0.0], [90.0, 0.0, 90.0]],   
                            ['* hips02_bind', [0.0, 13.0, 0.0], [90.0, 0.0, 90.0]],     
                            ['** l_hip_jnt', [0.5, 13.0, -0.0], [-90.0, 0.0, -21.8]],   
                            ['*** l_upLeg_jnt', [3.0, 12.0, 0.0], [-90.0, -0.0, -90.0]],   
                            ['**** l_lowLeg_jnt', [3.0, 6.5, 0.0], [-90.0, -0.0, -90.0]],     
                            ['***** l_foot_bind', [3.0, 1.0, -0.0], [-90.0, -71.48, -90.0]],
                            ['****** l_toe_bind', [3.0, 0.33, 2.0], [-90.0, -71.74, -90.0]],
                            ['******* l_toe1_jnt', [3.0, 0.0, 3.0], [-90.0, -71.74, -90.0]],
                            ['* spine01_bind', [0.0, 14.67, 0.0], [90.0, 0.0, 90.0]],
                            ['** spine02_bind', [0.0, 16.33, 0.0], [90.0, 0.0, 90.0]],
                            ['*** spine03_bind', [0.0, 18.0, 0.0], [90.0, 0.0, 90.0]],
                            ['**** spine04_bind', [0.0, 19.0, 0.0], [90.0, 0.0, 90.0]],
                            ['***** l_shoulder_bind', [0.5, 19.0, 1.0], [90.0, 21.8, -0.0]],
                            ['****** l_upArm_jnt', [3.0, 19.0, 0.0], [90.0, 0.0, 0.0]],
                            ['******* l_foreArm_jnt', [7.0, 19.0, 0.0], [90.0, 0.0, 0.0]],
                            ['******** l_hand_bind', [11.0, 19.0, 0.0], [90.0, 0.0, 0.0]],
                            ['********* l_pinky1_bind', [11.25, 19.0, -0.5], [180.0, 17.05, 0.0]],
                            ['********** l_pinky2_bind', [12.0, 19.0, -0.73], [180.0, 14.98, -0.0]],
                            ['*********** l_pinky3_bind', [12.52, 19.0, -0.87], [180.0, 14.98, -0.0]],
                            ['************ l_pinky4_bind', [13.05, 19.0, -1.01], [180.0, 14.98, -0.0]],
                            ['************* l_pinky5_bind', [13.57, 19.0, -1.15], [180.0, 15.72, 0.0]],
                            ['********* l_thumb1_bind', [11.09, 19.0, 0.35], [-180.0, -90.0, 0.0]],
                            ['********** l_thumb2_bind', [11.09, 19.0, 1.05], [-180.0, -90.0, 0.0]],
                            ['*********** l_thumb3_bind', [11.09, 19.0, 1.38], [-180.0, -90.0, 0.0]],
                            ['************ l_thumb4_bind', [11.09, 19.0, 1.71], [-180.0, -90.0, 0.0]],
                            ['********* l_middle1_bind', [11.25, 19.0, 0.16], [-180.0, -5.44, 0.0]],
                            ['********** l_middle2_bind', [12.09, 19.0, 0.24], [-180.0, -5.4, 0.0]],
                            ['*********** l_middle3_bind', [12.58, 19.0, 0.29], [-180.0, -5.4, 0.0]],
                            ['************ l_middle4_bind', [13.08, 19.0, 0.33], [-180.0, -5.4, 0.0]],
                            ['************* l_middle5_bind', [13.57, 19.0, 0.38], [-180.0, -5.44, 0.0]],
                            ['********* l_ring1_bind', [11.25, 19.0, -0.17], [180.0, 5.03, 0.0]],
                            ['********** l_ring2_bind', [12.09, 19.0, -0.24], [180.0, 5.4, 0.0]],
                            ['*********** l_ring3_bind', [12.58, 19.0, -0.29], [180.0, 5.4, 0.0]],
                            ['************ l_ring4_bind', [13.08, 19.0, -0.33], [180.0, 5.4, 0.0]],
                            ['************* l_ring5_bind', [13.57, 19.0, -0.38], [180.0, 5.36, 0.0]],
                            ['********* l_index1_bind', [11.25, 19.0, 0.5], [-180.0, -17.05, 0.0]],
                            ['********** l_index2_bind', [12.0, 19.0, 0.73], [-180.0, -15.32, 0.0]],
                            ['*********** l_index3_bind', [12.52, 19.0, 0.87], [-180.0, -15.32, 0.0]],
                            ['************ l_index4_bind', [13.05, 19.0, 1.02], [-180.0, -15.32, 0.0]],
                            ['************* l_index5_bind', [13.57, 19.0, 1.16], [-180.0, -17.0, 0.0]],
                            ['***** neck_bind', [0.0, 21.0, 0.0], [90.0, 0.0, 90.0]],
                            ['****** head_bind', [0.0, 22.0, 0.0], [90.0, 0.0, 90.0]],
                            ['******* head01_jnt', [0.0, 24.0, 0.0], [90.0, 0.0, 90.0]],
                            [' l_legRevers1_jnt', [2.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
                            ['* l_legRevers2_jnt', [4.0, 0.0, 1.0], [0.0, 180.0, 0.0]],
                            ['** l_legRevers3_jnt', [3.0, 0.0, -1.0], [0.0, -90.0, 0.0]],
                            ['*** l_legRevers4_jnt', [3.0, 0.0, 2.0], [0.0, -90.0, 0.0]],
                            ['**** l_legRevers5_jnt', [3.0, 0.0, 3.0], [0.0, 90.0, 0.0]],
                            ['***** l_legRevers6_jnt', [3.0, 0.33, 2.0], [90.0, 71.48, 90.0]],
                            ['****** l_legRevers7_jnt', [3.0, 1.0, 0.0], [90.0, 71.48, 90.0]],
                            [' l_armRevers1_jnt', [12.0, 18.74, 1.0], [0.0, 90.0, 0.0]],
                            ['* l_armRevers2_jnt', [12.0, 18.74, -1.0], [0.0, -90.0, 0.0]],
                            ['** l_armRevers3_jnt', [12.09, 19.0, 0.0], [0.0, 180.0, 0.0]],
                            ['*** l_armRevers4_jnt', [11.0, 19.0, 0.0], [-90.0, 180.0, -180.0]]]
                            
        self.rootJnts =  [x for x in self.getJntList() if not self.getParent(x) ]
        self.mirowJnt = 'l_hip_jnt', 'l_shoulder_bind',  'l_legRevers1_jnt', ' l_armRevers1_jnt'

#-------------------------------------------- 
    def __getitem__(self, item):
        return self.getJntList()[item]
#--------------------------------------------        
    def getJntFromIndex(self, iList): #insert jnt insted its indexes list
        #if type(iList[0])==int: return [ AnSkeleton().getJntList()[x] for x in iList]
        #else: return [[ AnSkeleton().getJntList()[x] for x in each] for each in iList]
        if type(iList[0])==int: return [ self.getJntList()[x] for x in iList]
        else: return [[ self.getJntList()[x] for x in each] for each in iList]
         
#--------------------------------------------   
    def getSkeletonPart(self, part, side='l_'): #  
        out=[]
        if part== 'body': out= [0, 1]+range (8,12) 
        if part== 'arm': out=  range (12,16) 
        if part== 'leg': out=  range (2,8) 
        #if part== 'fingers': out= [ range (16,21),  range (21,24), range (24,21), range (16,21), range (16,21)]
        return [side+x[2:] for x in  self.getJntFromIndex(out) if x[:2]=='l_']
#--------------------------------------------     
    def mirrowStructure(self):
        rSideJntList={}
        for mJnt in self.mirowJnt: 
            iStart, iEnd =0, 0
            for x in range(len(self.structure)):  # get jnt index in structure
                if mJnt in self.structure[x][0]: 
                    iStart=x
            lev =  len(self.structure[iStart][0].split('*')) # get hierarhy level
            for x in range( iStart+1,  len(self.structure)):   
                if  len(self.structure[x][0].split('*')) > lev:  iEnd = x  # get end jnt index of list
                else:  break
            list = []
            for  name, pos, ori in  self.structure[iStart:iEnd+1]:          #place to correct position and name
                name = name.split(' ')[0]+' r_'+name.split('*')[-1][3:] 
                list.append([str(name), pos, ori])
            rSideJntList[iEnd] = list
        out=[]
        for i in range(len(self.structure)):  # add to out
            if i in rSideJntList.keys():
                out.append(self.structure[i]) 
                for x in rSideJntList[i]:
                    out.append(x)
            else: 
                out.append(self.structure[i])
        self.structure = out 
#-------------------------------------------- 
    def skeletonRig(self, gScale=1):
        
        if not cmds.objExists(self.rootJnts[0]): self.createSceleton(miror=False)
        else: [cmds.delete (x.replace('l_', 'r_')) for x in self.mirowJnt]
        
        ''' 1) lists of difrent data tapes'''
        paretStructureForCt = self.getJntFromIndex(([1,0], [49, 5], [48, 6],  [7, 47],   [53, 15 ]    )) # joint list for parenting and hiding      [haidet, parent]
        nonChildJnt = [x for x in self.getJntList() if not self.getChildren(x)] #list of joint which do not have a childrens
        parentJnt = self.getJntFromIndex([0, 1, 15, 43, 44, 47, 11])  #list of joint which parentConstraned to controls
        hand, leg = self.getJntFromIndex([15, 5]) #jnt for placing arm and leg controls
        paretToHandCt = self.getJntFromIndex( range(15, 40)+range(50, 54) ) #controls which parent to hand
        paretToLegCt = self.getJntFromIndex( range(5, 8)+range(43, 50) ) #controls which parent to leg:
        midCtList = self.getJntFromIndex([[15, 14, 13], [5, 4, 3]]) # joint list for point constrant between ferst and end numbers in eacch list element
        helpLineList = self.getJntFromIndex([ range(7,1,-1)+[1,]+range(8,12,)+range(40,43),    range(11, 21),    range(21, 25),   range(25, 30),  range(30, 35),  range(35, 40),]) # joint list for help line
        
        ''' 2) Group whive controllers '''
        jenCT = ctrl('general_CT') #make general 
        jenCT.makeController('general',  size = gScale*12, offset = [0, 0, gScale])
        for attr, val in [ ('ctSize', [10, 0.5]), ('axisVis', [1, 1]), ('ctVis', [1, 1]), ('jntVis', [1, 0])    ]:
            cmds.addAttr(jenCT.name, longName=attr, defaultValue=val[1], minValue=0.0, maxValue=val[0], k=True)
        
        legCT = ctrl('legIk_CT') #make legCT 
        legCT.makeController( 'legIk',  size = gScale*4.5, offset = [0, -1*gScale, 0])
        #legCT.gropeCT()
        legCT.placeCT (leg, 'point')
        legCT.addColor (jenCT.name, 'left')
        
        handCT = ctrl('handIk_CT') #make hand CT 
        handCT.makeController( 'handIk',  size = gScale*2, orient="X")
        #handCT.gropeCT()
        handCT.placeCT (hand, 'parent')
        cmds.parent (legCT.oriGrp, handCT.oriGrp, jenCT.name )
        handCT.addColor (jenCT.name, 'left')
        
        
        #name=AnNames(AnNames(name).fixNonUniqueName()).divideName() _________________________________________________________________
        
        
            
        for jnt in self.getJntList(): # pos controller 
            #pfx = chn(jnt).divideName()[0]+ chn(jnt).divideName()[1]  
            pfx = AnNames(jnt).divideName()[0]+ AnNames(jnt).divideName()[1]  
            ctObj = ctrl(pfx+'_CT')
            ctObj.makeSpherAndOrientAxis( gScale )
            #ctObj.gropeCT()
            ctObj.placeCT (jnt, 'parent')
            for cord in [ 'x', 'y', 'z']: cmds.connectAttr (jenCT.name+'.ctSize', ctObj.name+'.s'+cord) 
            cmds.connectAttr (jenCT.name+'.axisVis', ctObj.name+'.axisVisibility') 
            cmds.connectAttr (jenCT.name+'.ctVis', ctObj.name+'.sphereVisibility') 
            if jnt in  self.rootJnts :  cmds.connectAttr (jenCT.name+'.jntVis', jnt+'.v') 

            if not jnt in parentJnt:   cmds.pointConstraint(ctObj.name,  jnt)
            else :                     cmds.parentConstraint(ctObj.name,  jnt)
        
            if jnt in paretToHandCt:  cmds.parent ( ctObj.oriGrp,  handCT.name)
            elif jnt in paretToLegCt:  cmds.parent ( ctObj.oriGrp,  legCT.name)
            else:  cmds.parent ( ctObj.oriGrp,  jenCT.name )    
        
        '''3) Connection joint to controls'''
        for jnt in self.getJntList():  # aim constrant from ct to jnt
            if not jnt in nonChildJnt+parentJnt:
                child = cmds.listRelatives(jnt, c=True)[0]
                #ch_CT = chn(child).divideName()[0]+ chn(child).divideName()[1]+'_CT'
                #CT = chn(jnt).divideName()[0]+ chn(jnt).divideName()[1]+'_CT'
                
                ch_CT = AnNames(child).divideName()[0]+ AnNames(child).divideName()[1]+'_CT'
                CT = AnNames(jnt).divideName()[0]+ AnNames(jnt).divideName()[1]+'_CT'

                cmds.aimConstraint(ch_CT, jnt, upVector=[0,0,1], worldUpVector=[0,0,1], worldUpType="objectrotation", worldUpObject= CT)   
            
        for chJnr, pJnt in paretStructureForCt: ##################### parent and haid controls
        
        
            #chCtOri = chn(chJnr).divideName()[0]+ chn(chJnr).divideName()[1]+'_ori'
            #pCt = chn(pJnt).divideName()[0]+ chn(pJnt).divideName()[1]+'_CT'
            
            chCtOri = AnNames(chJnr).divideName()[0]+ AnNames(chJnr).divideName()[1]+'_ori'
            pCt = AnNames(pJnt).divideName()[0]+ AnNames(pJnt).divideName()[1]+'_CT'          
            
            
            cmds.parent (chCtOri, pCt)
            cmds.setAttr(chCtOri+'.v', 0)
            
        for jnt1, midJnt, jnt2 in midCtList: 
            #ct1 = chn(jnt1).divideName()[0]+ chn(jnt1).divideName()[1]+'_CT'
            #ct2 = chn(jnt2).divideName()[0]+ chn(jnt2).divideName()[1]+'_CT'
            
            ct1 = AnNames(jnt1).divideName()[0]+ AnNames(jnt1).divideName()[1]+'_CT'
            ct2 = AnNames(jnt2).divideName()[0]+ AnNames(jnt2).divideName()[1]+'_CT'
            
            
            
            #cmds.pointConstraint( ct1,ct2, chn(midJnt).divideName()[0]+ chn(midJnt).divideName()[1]+'_ori', mo=True )
            cmds.pointConstraint(ct1 ,ct2, AnNames(midJnt).divideName()[0]+ AnNames(midJnt).divideName()[1]+'_ori', mo=True )
            
            
            
            
        for lst in helpLineList:
            cmds.parent ( an_helpLine(lst, name="line01_crv"), jenCT.name)
#--------------------------------------------   
    def getJntStructure (self, ignorRight=True):
        """ return skeleton hierarhy, jnt pos, """
        rootJnt = self.rootJnts
        if cmds.objExists(rootJnt[0]) :
            rPfx=AnNames('').prefixes()[1] # get pfx
            jntStructure = []
            def rekursion (obj, level=0):
                if cmds.nodeType(obj) == 'joint' :
                    jntInfo =[level*'*'+' '+ obj, self.getJntInfo(obj)[0], self.getJntInfo(obj)[1]]
                    jntStructure.append(jntInfo)
                    level = level+1
                    child = cmds.listRelatives (obj, c = True)
                    if child:
                        child =  [x for x in  child if x and not  x[:len(rPfx)]== rPfx ] #r side filter
                    if child: 
                        for x in child: rekursion (x, level) 
            for jnt in rootJnt :  rekursion (jnt, level=0)       
            self.structure = jntStructure
#-------------------------------------------- 
    def getJntInfo(self, jnt):
        roundVal = 2 # znakov okrugleniya posle zapyatoy 
        pos =  [round(x, roundVal) for x in  cmds.xform  (jnt, query=True,  worldSpace=True, translation=True)] # s okrugleniem
        ori = [round(x, roundVal) for x in cmds.xform  (jnt, query=True,  worldSpace=True, rotation=True)]
        child = None
        if cmds.listRelatives (jnt, c = True):
            child = [x for x in  cmds.listRelatives (jnt, c = True) if cmds.nodeType(x) == 'joint'] #non jnt filter
        return  pos, ori, child
#-------------------------------------------- 
    def getJntList(self, side='l_'):
        
        jntList = [x[0].split(' ')[-1] for x in self.structure]
        out =[]
        for each in jntList:
            if 'l_'== each[:2]:    out.append ( each.replace( 'l_', side))  
            else: out.append (each)
        return out
#-------------------------------------------- 
    def createSceleton (self, miror=True):
        if cmds.objExists(self.rootJnts[0].replace('_bind', '_CT') ):
            self.getJntStructure() 
            self.deleteSkeletonRig()
             
        for jnt, pos, ori in self.structure:
            cmds.select (cl=True)
            joinName = cmds.joint(n= jnt.split(' ')[-1], p = pos ) #create jnt    
        for jnt, pos, ori in self.structure:
            jnt = jnt.split(' ')[-1]
            parentJnt = self.getParent( jnt)
            cmds.setAttr(jnt+'.jointOrient', ori[0], ori[1], ori[2], type="double3" )
            if parentJnt: 
                cmds.parent (jnt, parentJnt) 
        if miror:
            [cmds.mirrorJoint (x, myz=True,  mb=True, sr= ["l_", "r_"]) for x in  self.mirowJnt ]
        if cmds.objExists('general_ori'): # del empty grp
            cmds.delete('general_ori')
            
            
#--------------------------------------------   
    def saveJntStructure(self):
        an_saveLoadData(data=self.structure, obgect='', delAttr = False, vDir='')  
#--------------------------------------------  
    def loadJntStructure(self):
        self.structure = an_saveLoadData() 

#-------------------------------------------- 
    def getChildren(self, jnt): 
        id = self.getJntList().index(jnt)       
        lev =  len(self.structure[id][0].split('*')) #stars number
        
        child =[]
        for each in self.structure [id+1:len(self.structure)]:
            if lev == len(each[0].split('*'))-1 : 
                child.append(each[0].split('*')[-1])   
            if lev == len(each[0].split('*')) : break       
        return child  
#-------------------------------------------- 
    def getParent(self, jnt):
        jntList = [x[0].split(' ')[-1] for x in self.structure]
        id = [ x[0] for x in enumerate( jntList ) if x[1]== jnt ][0] # jnt id in list       
        pNumber = len(self.structure[id][0].split(' ')[0]) #namber of stars
        if pNumber == 0: return None 
        i=id-1
        while len(self.structure[i][0].split(' ')[0]) >= pNumber:  i=i-1 # find parent jnt        
        return   jntList[i]  
#--------------------------------------------      
    def deleteSkeleton(self):
        for each in self.rootJnts: 
            if cmds.objExists(each):cmds.delete(each)
#-------------------------------------------- 
    def deleteSkeletonRig(self):
        self.getJntStructure()
        for each in self.rootJnts+['general_CT',]: cmds.delete(each)
#--------------------------------------------        
    def printJntStructure(self): 
        ind=0
        for i in self.structure: 
            print ind, '    ', i
            ind=ind+1
                       
 
























