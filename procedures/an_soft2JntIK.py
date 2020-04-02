from  anProcedures import  an_childCapture, an_distans, an_delSys
import maya.cmds as cmds 
from CharacterNames import CharacterNames as chn



def an_soft2JntIK (rootJoint , pVectorCtrl):
    
#rootJoint, pVectorCtrl = 'joint1', 'locator1'

    suffixes = chn('tt').suffixes
    prefix  = chn(rootJoint).divideName()[0]+chn(rootJoint).divideName()[1]
    
    jnts  = an_childCapture(rootJoint) #joint list
    
    side = 1 if cmds.getAttr (jnts [2]+".tx")>0 else -1 # get side koofic.
    ikHandl = cmds.ikHandle  (n=prefix+suffixes[11],   sol="ikRPsolver", shf=0, sj=jnts[0], ee=jnts[2]) 
    cmds.poleVectorConstraint (pVectorCtrl, ikHandl[0])
    
    for each in (['stretching', 1, 0, 1], ['lock', 0, 0, 1], ['upLength', 1, 0, 3], ['dwLength', 1, 0, 3], ['softIKOff', 0, 0, 1], ['softness', 1, 1, 3],   ):
        cmds.addAttr (ikHandl[0], longName=each[0], dv=each[1], min=each[2], max=each[3], keyable=True) #add list of attributes
    
    MtDv_L1 =cmds.createNode ( 'multiplyDivide', n=prefix+"_L1_ishodnik"+suffixes[12])    # seurse length of limbs joints
    cmds.setAttr (MtDv_L1+".input1X",  abs(cmds.getAttr (jnts [1]+".tx"))) 
    cmds.setAttr (MtDv_L1+".input1Y",  abs(cmds.getAttr (jnts [2]+".tx")))
    cmds.setAttr (MtDv_L1+".input1Z", 1)                                         # del warning 
    cmds.connectAttr (ikHandl[0]+".upLength", MtDv_L1+".input2X")   
    cmds.connectAttr (ikHandl[0]+".dwLength", MtDv_L1+".input2Y")  
    
    
    PMA_L2 = cmds.createNode ( 'plusMinusAverage', n=prefix+"_L2_Sum"+suffixes[14]) # sum of the joints lengths
    cmds.connectAttr (MtDv_L1+".outputX", PMA_L2+".input1D[0]")
    cmds.connectAttr (MtDv_L1+".outputY", PMA_L2+".input1D[1]")
    
    MtDv_L2 = cmds.createNode ( 'multiplyDivide', n=prefix+"_L3coff"+suffixes[12]) # get distans koofficients  !!!!!!!!!!!!!!!!!!!!! variable name nide coorection
    cmds.setAttr (MtDv_L2+".operation", 2) 
    cmds.connectAttr (PMA_L2+".output1D", MtDv_L2+".input1X")
    cmds.connectAttr (PMA_L2+".output1D", MtDv_L2+".input1Y")
    cmds.connectAttr (MtDv_L1+".output", MtDv_L2+".input2")
     
    DistMine = an_distans (jnts[0], ikHandl[0], act='createSys')   ###, prefix+"_L2_main")
    
    MtDv_L3strech = cmds.createNode ( 'multiplyDivide', n=prefix+"_L3strech"+suffixes[12]) # define length of strech limbs
    cmds.setAttr (MtDv_L3strech+".operation", 2) 
    for each in [".input1X", ".input1Y"]: cmds.connectAttr (DistMine[0], MtDv_L3strech+each)
    for coord in ["X", "Y"]: cmds.connectAttr (MtDv_L2+".output"+coord, MtDv_L3strech+".input2"+coord)
    
    Condition = cmds.createNode ( 'condition', n=prefix+"_L4_stopStretch")  
    cmds.setAttr (Condition+".operation", 4)
    cmds.connectAttr (DistMine[0], Condition+".firstTerm")
    cmds.connectAttr (PMA_L2+".output1D", Condition+".secondTerm") 
    cmds.connectAttr (MtDv_L1+".output", Condition+".colorIfFalse")
    cmds.connectAttr (MtDv_L3strech+".output", Condition+".colorIfTrue")
    
    strLock = cmds.createNode ( 'blendColors', n=prefix+"_L5_strLock")   # lock/unlock stretching
    cmds.connectAttr (MtDv_L3strech+".output", strLock+".color1")
    cmds.connectAttr (Condition+".outColor", strLock+".color2")
    cmds.connectAttr (ikHandl[0]+'.stretching', strLock+'.blender')
    
    ################################################### construction of the second stream is responsible for mixing
    
    MtDv_L3ratio = cmds.createNode ( 'multiplyDivide', n=prefix+"_L3ratio"+suffixes[12]) # define ratio stretch and non stretch
    cmds.setAttr (MtDv_L3ratio+".operation", 2)
    cmds.connectAttr (PMA_L2+".output1D", MtDv_L3ratio+".input1X")
    cmds.connectAttr   (DistMine[0],  MtDv_L3ratio+".input2X")
    
    setRange = cmds.createNode ( 'setRange', n=prefix+"_L4_setRangeSoftness")   # Softness
    cmds.connectAttr (MtDv_L3ratio+".outputX", setRange+".valueX")
    cmds.setAttr (setRange+".minX", 1)
    cmds.setAttr (setRange+".maxX", 1.25)
    cmds.setAttr (setRange+".oldMinX", 1)
    cmds.connectAttr (ikHandl[0]+".softness", setRange+".oldMaxX")
    
    softOffcBlend = cmds.createNode ( 'blendTwoAttr', n=prefix+"_L5softOff")   # Softness off node
    
    """
    
    curveData =[(1.0, 0.0), (1.009970625, 0.014375), (1.019015, 0.0415), (1.0273318749999998, 0.079875), (1.03512, 0.128), (1.042578125, 0.184375), (1.049905, 0.2475), 
                (1.057299375, 0.315875), (1.06496, 0.388), (1.073085625, 0.462375), (1.081875, 0.5375), (1.091526875, 0.611875), (1.10224, 0.684), (1.114213125, 0.752375), 
                (1.127645, 0.8155), (1.142734375, 0.871875), (1.15968, 0.92), (1.178680625, 0.958375), (1.199935, 0.9855), (1.223641875, 0.999875), (1.25, 1.0)] 
    for coord in  curveData: #                     
        cmds.setDrivenKeyframe (softOffcBlend+'.input[0]', cd=setRange+'.outValueX', dv=coord[0], v=coord[1]) 
    
    """
    
    cmds.setDrivenKeyframe (softOffcBlend+".input[0]", cd=setRange+".outValueX", dv=1, v=0) # mack anim curve
    cmds.setDrivenKeyframe (softOffcBlend+".input[0]", cd=setRange+".outValueX", dv=1.1, v=0.66)
    cmds.setDrivenKeyframe (softOffcBlend+".input[0]", cd=setRange+".outValueX", dv=1.25, v=1)
    cmds.keyTangent(softOffcBlend+".input[0]", f=(0, 2), itt='flat', ott='flat') 
    cmds.keyTangent(softOffcBlend+".input[0]", e=True, f= (1.1, 1.1) , inAngle=15, inWeight=1) 
    cmds.connectAttr (ikHandl[0]+".softIKOff", softOffcBlend+".attributesBlender")
    
    conditionStopSostness = cmds.createNode ( 'condition', n=prefix+"_L5_StopSostness")  # conditionStopSoftness
    cmds.setAttr (conditionStopSostness+".operation", 4)
    cmds.connectAttr (MtDv_L3ratio+'.outputX', conditionStopSostness+".firstTerm")
    cmds.setAttr (conditionStopSostness+".secondTerm", 1)
    cmds.connectAttr (conditionStopSostness+'.outColorR',  softOffcBlend+'.input[1]')
    
    mix = cmds.createNode ( 'blendColors', n=prefix+"_L6_mix")   #  mix stretch and not stretch
    cmds.connectAttr (MtDv_L1+'.output', mix+".color1")
    cmds.connectAttr (strLock+'.output', mix+".color2")
    cmds.connectAttr (softOffcBlend+'.output', mix+".blender")
    
    DistUp = an_distans (jnts[0], pVectorCtrl, act='createSys')#, prefix+"Up")
    DistDw = an_distans (ikHandl[0], pVectorCtrl, act='createSys')#, prefix+"Dw")
    
    elbLock = cmds.createNode ('blendColors', n=prefix+"_L7elbLock")   # lock/unlock stretching
    
    cmds.connectAttr (DistUp[0], elbLock+".color1R")
    cmds.connectAttr (DistDw[0], elbLock+".color1G")
    cmds.connectAttr (mix+".output", elbLock+".color2")
    cmds.connectAttr (ikHandl[0]+".lock", elbLock+".blender")
    
    
    reversDivide=''           										#connect to joint if x negativ add node
    if     side ==1:
        cmds.connectAttr (elbLock+".outputR", jnts[1]+".tx")
        cmds.connectAttr (elbLock+".outputG", jnts[2]+".tx")    
    else:
        reversDivide = cmds.createNode ('multiplyDivide', n=prefix+"_L8reversNode")
        cmds.connectAttr (elbLock+".outputR", reversDivide+".input1X")
        cmds.connectAttr (elbLock+".outputG", reversDivide+".input1Y")
        cmds.setAttr (reversDivide+".input2X", -1)
        cmds.setAttr (reversDivide+".input2Y", -1)    
    
        cmds.connectAttr (reversDivide+".outputX", jnts[1]+".tx")
        cmds.connectAttr (reversDivide+".outputY", jnts[2]+".tx") 
        
    an_startPosVal (MtDv_L1, rootJoint)
    
    rigGroup = cmds.group(ikHandl[0], DistMine[1], DistUp[1], DistDw[1], n=prefix+"_softIkRig_grp")
    cmds.xform(os=True, piv=[0, 0, 0])
    
    an_delSys(rigGroup,  [MtDv_L1, PMA_L2, MtDv_L2, DistMine[1], MtDv_L3strech, Condition, strLock, MtDv_L3ratio, setRange, softOffcBlend, conditionStopSostness, mix, DistUp[1], DistDw[1], elbLock, reversDivide] )
    
    return [ikHandl[0], rigGroup]

###############################################################



#rootJoint, startMDV = 'joint1', 'joint1_L1_ishodnik_mdv'

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
 

#ish = len(cmds.ls())


#an_delSys('joint1_softIkRig_grp')

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






