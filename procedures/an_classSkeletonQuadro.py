

#self = AnSkeletonQuadro()
#self.skeletonRig()
#self.getJntStructure()
#self.createSceleton(miror=False)
#self.deleteSkeletonRig()
#self.deleteSkeleton()
#self.printJntStructure()
from an_classSkeleton import AnSkeleton
from an_classNames import  AnNames
#from  anProcedures import  * 
from an_classControllers import  AnControllers  as ctrl

'''
    AnSkeletonQuadro()
    
Class for storage and create  Quadro joint structure and names
	
attributes:
    - structure
    - rootJnts    attib need for getJntStructu re () 
    - mirowJnt    nirow jnts list 
'''

class AnSkeletonQuadro(AnSkeleton):
    def __init__ (self ):
        self.structure=[ [' hips01_bind', [0.0, 6.92, -1.16], [-180.0, -90.0, 0.0]],
                        [u'* hips02_bind', [0.0, 6.92, -1.16], [-180.0, -90.0, 0.0]],
                        [u'** l_hip_jnt', [0.41, 6.92, -1.16], [-90.0, -0.0, -18.44]],
                        [u'*** l_upLeg_jnt', [1.63, 6.51, -1.16], [-90.0, 23.2, -90.0]],
                        [u'**** l_lowLeg_jnt', [1.63, 3.66, -2.38], [-90.0, 59.04, -90.0]],
                        [u'***** l_foot_bind', [1.63, 2.44, -4.42], [-90.0, -12.85, -90.0]],
                        [u'****** l_toe_bind', [1.63, 0.57, -4.01], [-90.0, -67.53, -90.0]],
                        [u'******* l_toe1_jnt', [1.63, 0.33, -3.4], [-90.0, -58.39, -90.0]],
                        [u'******** l_toe2_jnt', [1.63, 0.0, -2.87], [-90.0, -58.39, -90.0]],
                        [u'* spine01_bind', [-0.0, 6.92, 0.38], [-180.0, -90.0, 0.0]],
                        [u'** spine02_bind', [0.0, 6.92, 1.89], [-180.0, -90.0, 0.0]],
                        [u'*** spine03_bind', [0.0, 6.92, 3.44], [-180.0, -90.0, 0.0]],
                        [u'**** spine04_bind', [0.0, 6.92, 4.94], [90.0, -26.57, 90.0]],
                        [u'***** neck_bind', [0.0, 8.14, 5.55], [90.0, -14.04, 90.0]],
                        [u'****** head_bind', [0.0, 11.39, 6.37], [90.0, 0.0, 90.0]],
                        [u'******* head01_jnt', [0.0, 13.02, 6.37], [90.0, -8.14, 90.0]],
                        [u'***** l_shoulder_bind', [0.41, 6.92, 4.94], [-90.0, 0.0, -14.04]],
                        [u'****** l_upArm_jnt', [2.03, 6.51, 4.94], [-90.0, 18.43, -90.0]],
                        [u'******* l_foreArm_jnt', [2.03, 4.07, 4.13], [-90.0, -14.04, -90.0]],
                        [u'******** l_hand_bind', [2.03, 1.63, 4.74], [-90.0, -15.07, -90.0]],
                        [u'********* l_middle1_bind', [2.03, 0.57, 5.02], [-90.0, -66.8, -90.0]],
                        [u'********** l_middle2_bind', [2.03, 0.33, 5.59], [-90.0, -60.26, -90.0]],
                        [u'*********** l_middle3_bind', [2.03, -0.0, 6.16], [-90.0, -60.26, -90.0]],
                        [' l_legRevers1_jnt', [1.22, 0.0, -3.48], [0.0, 0.0, 0.0]],
                        [u'* l_legRevers2_jnt', [2.03, 0.0, -3.48], [0.0, 180.02, 0.0]],
                        [u'** l_legRevers3_jnt', [1.63, 0.0, -3.81], [0.0, 269.16, 0.0]],
                        [u'*** l_legRevers4_jnt', [1.63, 0.0, -3.4], [0.0, 269.16, 0.0]],
                        [u'**** l_legRevers5_jnt', [1.63, 0.0, -2.87], [-1.54, 88.2, -1.55]],
                        [u'***** l_legRevers6_jnt', [1.63, 0.33, -3.4], [90.0, 67.53, 90.0]],
                        [u'****** l_legRevers7_jnt', [1.63, 0.57, -4.01], [90.0, 12.85, 90.0]],
                        [u'******* l_legRevers8_jnt', [1.63, 2.44, -4.42], [43.8, 86.18, 43.87]],
                        [' l_armRevers1_jnt', [1.63, 0.0, 5.31], [0.0, 0.0, 0.0]],
                        [u'* l_armRevers2_jnt', [2.44, 0.0, 5.31], [0.0, 180.05, 0.0]],
                        [u'** l_armRevers3_jnt', [2.03, 0.0, 4.98], [0.0, 269.16, 0.0]],
                        [u'*** l_armRevers4_jnt', [2.03, 0.0, 5.39], [0.0, 269.16, 0.0]],
                        [u'**** l_armRevers5_jnt', [2.03, 0.0, 6.16], [-2.21, 88.2, -2.21]],
                        [u'***** l_armRevers6_jnt', [2.03, 0.33, 5.59], [90.0, 66.8, 90.0]],
                        [u'****** l_armRevers7_jnt', [2.03, 0.57, 5.02], [90.0, 15.07, 90.0]],
                        [u'******* l_armRevers8_jnt', [2.03, 1.63, 4.74], [87.99, -11.64, -85.69]]]
                        
        self.rootJnts =  [x for x in self.getJntList() if not self.getParent(x) ]
        self.mirowJnt = 'l_shoulder_bind', 'l_hip_jnt', 'l_legRevers1_jnt', ' l_armRevers1_jnt'


    def getSkeletonPart(self, part, side='l_'): #  
        out=[]
        if part== 'body': 
            out= [0, 1]+range (8,12) 
            return  self.getJntFromIndex(out) 
        if part== 'arm': out=  range (16,22) 
        if part== 'leg': out=  range (2,8) 
        #if part== 'fingers': out= [ range (16,21),  range (21,24), range (24,21), range (16,21), range (16,21)]
        return [side+x[2:] for x in  self.getJntFromIndex(out) if x[:2]=='l_']

    def skeletonRig(self, gScale=1):
        
        if not cmds.objExists(self.rootJnts[0]): self.createSceleton(miror=False)
        else: [cmds.delete (x.replace('l_', 'r_')) for x in self.mirowJnt]
        
        ''' 1) lists of difrent data tapes'''
        
        def getJntFromIndex(iList): #insert jnt insted its indexes
            if type(iList[0])==int: return [ AnSkeletonQuadro().getJntList()[x] for x in iList]
            else: return [[ AnSkeletonQuadro().getJntList()[x] for x in each] for each in iList]
        
        hand, leg = getJntFromIndex([20, 6])                                                        # jnt for placing arm and leg controls
        paretStructureForCt = getJntFromIndex(([1,0],     ))                                        # joint list for parenting and hiding      [haidet, parent]
        nonChildJnt = [x for x in self.getJntList() if not self.getChildren(x)]                     # list of joint which do not have a childrens
        parentJnt = getJntFromIndex([0, 1,] )                                                       # list of joint which parentConstraned to controls
        paretToHandCt = getJntFromIndex( range(19, 23)+range(31, 39) )                              # controls which parent to hand
        paretToLegCt = getJntFromIndex( range(5, 9)+range(23, 31) )                                 # controls which parent to leg:
        #midCtList = getJntFromIndex([[15, 14, 13], [5, 4, 3]])                                     # joint list for point constrant between ferst and end numbers in eacch list element
        helpLineList = getJntFromIndex([range(8,1,-1)+[0]+range(9, 16)    ,  [12]+ range(16, 23) ]) # joint list for help line
        
        ''' 2) Group whive controllers '''
        
        jenCT = ctrl('general_CT') #make general 
        jenCT.makeController('general',  size = gScale*17, offset = [0, 0, gScale/2])
        for attr, val in [ ('ctSize', [10, 0.5]), ('axisVis', [1, 1]), ('ctVis', [1, 1]), ('jntVis', [1, 0])    ]:
            cmds.addAttr(jenCT.name, longName=attr, defaultValue=val[1], minValue=0.0, maxValue=val[0], k=True)
        
        legCT = ctrl('legIk_CT') #make legCT 
        legCT.makeController( 'legIk',  size = gScale*3, offset = [0, 0, 0])
        #legCT.gropeCT()
        legCT.placeCT (leg, 'point')
        cmds.setAttr(legCT.oriGrp + '.ty', 0)
        legCT.addColor (jenCT.name, 'left')
        
        handCT = ctrl('handIk_CT') #make hand CT 
        handCT.makeController( 'legIk',  size = gScale*3, offset = [0, 0, 0])
        #handCT.gropeCT()
        handCT.placeCT (hand, 'point')
        cmds.setAttr(handCT.oriGrp + '.ty', 0)
        cmds.parent (legCT.oriGrp, handCT.oriGrp, jenCT.name )
        handCT.addColor (jenCT.name, 'left')
        
        for jnt in self.getJntList(): # pos controller 
            pfx = chn(jnt).sfxMinus()
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
                cH_CT = chn(child).divideName()[0]+ chn(child).divideName()[1]+'_CT'
                CT = chn(jnt).divideName()[0]+ chn(jnt).divideName()[1]+'_CT'
                cmds.aimConstraint(cH_CT, jnt, upVector=[0,0,1], worldUpVector=[0,0,1], worldUpType="objectrotation", worldUpObject= CT)   

        for chJnr, pJnt in paretStructureForCt: ##################### parent and haid controls
            chCtOri = chn(chJnr).divideName()[0]+ chn(chJnr).divideName()[1]+'_ori'
            pCt = chn(pJnt).divideName()[0]+ chn(pJnt).divideName()[1]+'_CT'
            cmds.parent (chCtOri, pCt)
            cmds.setAttr(chCtOri+'.v', 0)
            
        '''for jnt1, midJnt, jnt2 in midCtList: 
            ct1 = chn(jnt1).divideName()[0]+ chn(jnt1).divideName()[1]+'_CT'
            ct2 = chn(jnt2).divideName()[0]+ chn(jnt2).divideName()[1]+'_CT'
            cmds.pointConstraint( ct1,ct2, chn(midJnt).divideName()[0]+ chn(midJnt).divideName()[1]+'_ori', mo=True )'''
            
        for lst in helpLineList:
            cmds.parent ( an_helpLine(lst, name="line01_crv"), jenCT.name)      
            
            
            
                       