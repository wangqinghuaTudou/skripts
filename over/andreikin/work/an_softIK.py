from  anProcedures import  *
import maya.cmds as cmds 
from CharacterNames import CharacterNames as chn



def an_softIK (ikHand,  lock=True, length=True ):
    
    #ikHand = 'ikHandle1'
     
    v_objects = cmds.ikHandle  (ikHand, q=True, sj=True)
    suffixes = chn('tt').suffixes
    jnts  = an_childCapture(cmds.ikHandle  (ikHand, q=True, sj=True))
    prefix  = chn(jnts[0]).divideName()[0]+chn(jnts[0]).divideName()[1]
    pVectorCtrl = cmds.poleVectorConstraint ( ikHand, q=True,   wal=True)[0][:-2]
    side = 1 if cmds.getAttr (jnts [2]+".tx")>0 else -1 # get side koofic.
    
    #blend noda miksuushaya stretchabl i non stretchable cepochki____________
    
    mixChainsBled = cmds.createNode ('blendColors', n=prefix+"_mixBendAndNonbendChains")   
        
    upJntTx = abs(cmds.getAttr (jnts [1]+".tx"))  
    dwJntTx = abs(cmds.getAttr (jnts [2]+".tx"))
      
    cmds.setAttr ( mixChainsBled+".color1R", upJntTx)  # non stretchable length 1
    cmds.setAttr ( mixChainsBled+".color1G", dwJntTx)  # non stretchable length 2
    cmds.setAttr ( mixChainsBled+".color2R", upJntTx) # tmp
    cmds.setAttr ( mixChainsBled+".color2G", dwJntTx) # tmp 
    cmds.connectAttr (mixChainsBled+".outputR", jnts[1]+".tx")   
    cmds.connectAttr (mixChainsBled+".outputG", jnts[2]+".tx") 
    
    #stretchabl cepochka_____________________________    
    
    upCoof = (upJntTx+dwJntTx)/ upJntTx
    dwCoof = (upJntTx+dwJntTx)/ dwJntTx
    
    distMine = an_distans (jnts[0], ikHand, act='createSys')   ###, prefix+"_L2_main")
    
    stretchablLenMtDv = cmds.createNode ( 'multiplyDivide', n=prefix+"_stretchablLen"+suffixes[12])
    cmds.setAttr (stretchablLenMtDv+".operation",  2) 
    for d in ['X', 'Y']: cmds.connectAttr (distMine[0], stretchablLenMtDv+".input1"+d) 
    cmds.setAttr (stretchablLenMtDv+".input2X",  upCoof) 
    cmds.setAttr (stretchablLenMtDv+".input2Y",  dwCoof)
    cmds.setAttr (stretchablLenMtDv+".input1Z",  3)
    cmds.setAttr (stretchablLenMtDv+".input2Z",  1)
    for v, c in zip(['X', 'Y'], ['R', 'G']): cmds.connectAttr (stretchablLenMtDv+'.output'+v,   mixChainsBled+'.color2'+c)
    
    # vycheslitel blend nody miksuushiy nonStretchable i stretchable cepochki
    
    mixDriverSolverMdv = cmds.createNode ( 'multiplyDivide', n=prefix+"_mixDriverSolver"+suffixes[12])
    cmds.setAttr (mixDriverSolverMdv+".operation",  2) 
    cmds.connectAttr (distMine[0], mixDriverSolverMdv+".input2X") 
    cmds.setAttr (mixDriverSolverMdv+".input1X",  upJntTx+dwJntTx) 
     
    cmds.setDrivenKeyframe (mixChainsBled+".blender", cd=mixDriverSolverMdv+".outputX", dv=1, v=0) # mack anim curve
    cmds.setDrivenKeyframe (mixChainsBled+".blender", cd=mixDriverSolverMdv+".outputX", dv=1.1, v=0.66)
    cmds.setDrivenKeyframe (mixChainsBled+".blender", cd=mixDriverSolverMdv+".outputX", dv=1.25, v=1)
    cmds.keyTangent(mixChainsBled+".blender", f=(0, 2), itt='flat', ott='flat') 
    cmds.keyTangent(mixChainsBled+".blender", e=True, f= (1.1, 1.1) , inAngle=15, inWeight=1) 
    
    #connect to joint if x negativ add node
    reversDivide=''           										
    if     side ==-1:
        reversDivide = cmds.createNode ('multiplyDivide', n=prefix+"_ReversNode")
        cmds.connectAttr (mixChainsBled+".outputR", reversDivide+".input1X")
        cmds.connectAttr (mixChainsBled+".outputG", reversDivide+".input1Y")
        cmds.setAttr (reversDivide+".input2X", -1)
        cmds.setAttr (reversDivide+".input2Y", -1)    
        cmds.connectAttr (reversDivide+".outputX", jnts[1]+".tx", f=True)
        cmds.connectAttr (reversDivide+".outputY", jnts[2]+".tx", f=True)
    #systema uzhe mozhet rabotat`, dalee dobovlyem raznye fitchy

    #________________________________________________________________________________________________________
     
    # add nonstratchable mod if need
    
    Condition = cmds.createNode ( 'condition', n=prefix+"_stopStretchCND")
      
    cmds.setAttr (Condition+".operation", 2)
    cmds.connectAttr (distMine[0], Condition+".firstTerm")
    cmds.setAttr (Condition+".secondTerm", (upJntTx+dwJntTx))
    cmds.setAttr (Condition+".colorIfTrueR", (upJntTx+dwJntTx))
    cmds.connectAttr (distMine[0], Condition+".colorIfFalseR")
    
    stopStretchBTA = cmds.createNode ( 'blendTwoAttr', n=prefix+"_stopStretchBTA") 
    cmds.connectAttr (Condition+".outColorR", stopStretchBTA+".input[0]")
    cmds.connectAttr (distMine[0], stopStretchBTA+".input[1]")
     
    for d in ['X', 'Y']: cmds.connectAttr (stopStretchBTA+'.output', stretchablLenMtDv+".input1"+d, f=True)
     
    for each in (['stretching', 1, 0, 1], ['lock', 0, 0, 1], ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3],):
        cmds.addAttr (ikHand, longName=each[0], dv=each[1], min=each[2], max=each[3], keyable=True) #add list of attributes
        
    cmds.connectAttr (ikHand+'.stretching', stopStretchBTA+".attributesBlender")  
        
    #________________________________________________________________________________________________________
    
    #add length correction
    
    if length:
    
        MtDv_L1 =cmds.createNode ( 'multiplyDivide', n=prefix+"_Ishodnik"+suffixes[12])    # seurse length of limbs joints
        cmds.setAttr (MtDv_L1+".input1X",  upJntTx) 
        cmds.setAttr (MtDv_L1+".input1Y",  dwJntTx)
                                              # del warning 
        cmds.connectAttr (ikHand+".upLength", MtDv_L1+".input2X")   
        cmds.connectAttr (ikHand+".dwLength", MtDv_L1+".input2Y")  
        
        cmds.connectAttr (MtDv_L1+".outputX", mixChainsBled+".color1R")
        cmds.connectAttr (MtDv_L1+".outputY", mixChainsBled+".color1G")
        
        PMA_L2 = cmds.createNode ( 'plusMinusAverage', n=prefix+"_lengthSum"+suffixes[14]) # sum of the joints lengths
        cmds.connectAttr (MtDv_L1+".outputX", PMA_L2+".input1D[0]")
        cmds.connectAttr (MtDv_L1+".outputY", PMA_L2+".input1D[1]")
        
        for attr in [Condition+".secondTerm",  Condition+".colorIfTrueR",  mixDriverSolverMdv+".input1X"]:
            cmds.connectAttr (PMA_L2+".output1D", attr)
             
        MtDv_L2 = cmds.createNode ( 'multiplyDivide', n=prefix+"Kofficient"+suffixes[12]) # get distans koofficients   
        cmds.setAttr (MtDv_L2+".operation", 2) 
        cmds.connectAttr (PMA_L2+".output1D", MtDv_L2+".input1X")
        cmds.connectAttr (PMA_L2+".output1D", MtDv_L2+".input1Y")
        cmds.connectAttr (MtDv_L1+".outputX", MtDv_L2+".input2X")  
        cmds.connectAttr (MtDv_L1+".outputY", MtDv_L2+".input2Y") 
        
        cmds.connectAttr (MtDv_L2+".outputX", stretchablLenMtDv+".input2X")  
        cmds.connectAttr (MtDv_L2+".outputY", stretchablLenMtDv+".input2Y")
        
        an_startPosVal (MtDv_L1, jnts[0])    
    
    #add lock to polVector CT
    if lock: 
        DistUp = an_distans (jnts[0], pVectorCtrl, act='createSys')#, prefix+"Up")
        DistDw = an_distans (ikHand, pVectorCtrl, act='createSys')#, prefix+"Dw")
        
        elbLock = cmds.createNode ('blendColors', n=prefix+"_ElbLock")   # lock/unlock stretching
        cmds.connectAttr (DistUp[0], elbLock+".color1R")
        cmds.connectAttr (DistDw[0], elbLock+".color1G")
        cmds.connectAttr (ikHand+".lock", elbLock+".blender")
        
        inpAttr = mixChainsBled+".output"   if side==1 else  reversDivide+".outputX"
        cmds.connectAttr (inpAttr, elbLock+".color2")
        cmds.connectAttr (elbLock+".outputR", jnts[1]+".tx", f=True)   
        cmds.connectAttr (elbLock+".outputG", jnts[2]+".tx", f=True)
    

 

def an_startPosVal (startMDV, rootJoint):
    jnts  = an_childCapture(rootJoint) #joint list   
    startTx1 =  cmds.getAttr (startMDV+".input1X")
    startTx2 =  cmds.getAttr (startMDV+".input1Y")
    realTx1 =  abs(cmds.getAttr (jnts [1]+".tx"))
    realTx2 = abs(cmds.getAttr (jnts [2]+".tx"))
    startLength, realLength, targetLength, = startTx1+startTx2, realTx1+realTx2, cmds.getAttr (startMDV+".input1X")+cmds.getAttr (startMDV+".input1Y")
    add =(startLength-realLength )/1000
    
    for eter in range(10000):
        if realLength<targetLength:
            startTx1, startTx2  =  startTx1+add, startTx2+add
            cmds.setAttr (startMDV+".input1X", startTx1)
            cmds.setAttr (startMDV+".input1Y", startTx2)        
            realLength = abs(cmds.getAttr (jnts [1]+".tx"))+abs(cmds.getAttr (jnts [2]+".tx"))

#######################################
 
def an_2JntIK (rootJoint , pVectorCtrl):
    suffixes = chn('tt').suffixes
    prefix  = chn(rootJoint).divideName()[0]+chn(rootJoint).divideName()[1]
    jnts  = an_childCapture(rootJoint) #joint list
    ikHandl = cmds.ikHandle  (n=prefix+suffixes[11],   sol="ikRPsolver", shf=0, sj=jnts[0], ee=jnts[2]) 
    cmds.poleVectorConstraint (pVectorCtrl, ikHandl[0])
    for each in (['stretching', 1, 0, 1], ['lock', 0, 0, 1], ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3], ['softIKOff', 0, 0, 1], ['softness', 1, 1, 3],   ):
        cmds.addAttr (ikHandl[0], longName=each[0], dv=each[1], min=each[2], max=each[3], keyable=True) #add list of attributes
    rigGroup = cmds.group(ikHandl[0],  n=prefix+"_softIkRig_grp")
    cmds.xform(os=True, piv=[0, 0, 0])
    return [ikHandl[0], rigGroup]













