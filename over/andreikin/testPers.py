
from An_Controllers import An_Controllers as ctrl
from  an_rigAdditionalTools import *
from  anProcedures import  *
import maya.cmds as cmds
from CharacterNames import CharacterNames as chn


def persTestingUI():
    zeroVals = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz' ]
    ctList = cmds.ls ("*"+"_CT")
    lay = an_turnBasedUi('', title ='Charakters test',  stepsLabel =['Key test', 'Zero value', 'None unique ct mames', 'Misc'])

    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)], p=lay[0])
    cmds.button(l='Keys  test', c='keyCtTest(cmds.ls ("*_CT"))')
    cmds.button(l='Delete keys', c='keyCtDel()')

    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)], p=lay[1])
    cmds.button(l='Zero value test', c='zeroCtTest(cmds.ls ("*_CT"))')
    cmds.button(l='Zero value set', c='zeroCtSet()')

    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)], p=lay[2])
    cmds.button(l='None unique ct mames test', c='uniqCtTest()')
    cmds.button(l='Select none unique ct', c='zeroCtSet()')

    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)], p=lay[3])

    cmds.button(l='Geo smoothness off', c='geoSmoothnessOf()')
    cmds.button(l='Set ik toleranse', c='setIkToleranse()')
    cmds.button(l='Jnt visibility off', c='jntVisibility()')
    cmds.button(l='Mirrow ct shape', c='mirrowLeftCtToRight()')
    cmds.button(l='Jnt visibility on', c='cmds.setAttr("switch_CT.jntVis", 1)')

    cmds.button(l='Test animatiom', c='doTestAnim()')


#persTestingUI()

def  keyCtDel():   
    ctList = cmds.ls ("*"+"_CT")
    if [x for x in  ctList if cmds.keyframe( x, query=True, keyframeCount=True ) ]:
        print '\nList of key deleted:\n___________________'
    for ct in [x for x in  ctList if cmds.keyframe( x, query=True, keyframeCount=True ) ]:
        print ct, 'deleted keys'
        cmds.cutKey(ct,  cl=True )

def  keyCtTest(ctList):   
    keyCt=[]
    for ct in ctList:
        if cmds.keyframe( ct, query=True, keyframeCount=True ):
            keyCt.append(ct)
    if keyCt:
        print '\nList of key controls:\n___________________'
        for ct in keyCt: print ct
    return keyCt

def  zeroCtTest(ctList):  
    zeroVals = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz' ]
    exceptionCt = ['switch_CT',]
    nonZeroCt={}
    for ct in [x for x in ctList if not x in exceptionCt] :
        if [ x for x in zeroVals if cmds.getAttr(ct+'.'+x)!=0.0 ]:
            nonZeroCt[ct]=[]
            for attr in [ x for x in zeroVals if cmds.getAttr(ct+'.'+x)!=0.0 ]: nonZeroCt[ct].append(attr)
    if nonZeroCt: print '\nNone zero value controls:\n___________________'
    for ct in nonZeroCt: print ct
    return nonZeroCt

def  zeroCtSet():
    exceptionCt =['switch_CT',]
    nonZeroCt = zeroCtTest(cmds.ls ("*"+"_CT"))
    print '\nControls set to 0:\n___________________'
    for ct in nonZeroCt.keys():
        if not ct in exceptionCt:
            for attr in nonZeroCt[ct]:
                cmds.setAttr(ct+'.'+attr, 0)
            print  ct

def uniqCtTest():      
    nonUniqCtList = list(set([x.split('|')[-1] for x  in cmds.ls ("*"+"_CT") if '|' in x]))
    if not nonUniqCtList: print '\nAll controls have unique mames '
    else:
        print '\nList controls whith non unique mames :\n___________________\n'
        for ct in nonUniqCtList: print ct

def selNoneUniqCt():
    nonUniqCtList = list(set([x for x  in cmds.ls ("*"+"_CT") if '|' in x]))
    cmds.select(nonUniqCtList)

def geoSmoothnessOf ():  
    for mesh in cmds.ls (type=['mesh',]):
        cmds.setAttr(mesh+'.dsm', 0)

def setIkToleranse (): 
    cmds.setAttr ("ikSCsolver.tolerance", 0.0000000001)

def jntVisibility(): 
    jntList = []
    for jnt in cmds.ls (type=['joint']):
        try:
            if  cmds.nodeType(cmds.listRelatives (jnt, p=True)[0])  != 'joint': jntList.append(jnt)
        except: jntList.append(jnt)
    switch = 'switch_CT'
    if not cmds.objExists(switch+'.jntVis'):
        cmds.addAttr (switch, ln="jntVis", at="enum", en="off:on", keyable=False)
        revers = cmds.createNode  ("reverse", n='jntVisRevers')
        cmds.connectAttr (switch+'.jntVis', revers+".inputX")
    for each in jntList:
        if cmds.objectType (each, isType="joint" ):
            if not cmds.connectionInfo (each+".overrideEnabled", id=True ):
                cmds.connectAttr ("jntVisRevers.outputX", each+".overrideEnabled")
            if not cmds.connectionInfo (each+".overrideVisibility", id=True ):
                cmds.connectAttr (switch+'.jntVis', each+".overrideVisibility")
    cmds.setAttr('switch_CT.jntVis', 0)




def mirrowLeftCtToRight(): # mirrow left ct to right
    for ct in cmds.ls ("*"+"_CT"):
        if ct[:2]=='l_':
            ctrl(ct).mirrorShape('r_'+ct[2:])

#ct ='l_foreArm_CT'


def doTestAnim():
    controllers = cmds.ls( sl=True )
    for ct in controllers: testAnim (ct)
    cmds.select (controllers)

def testAnim (ct):
#ct =    cmds.ls( sl=True )[0]

    cmds.select (ct)
    switchCt = chn(object).general[0]
    interval = 30


    l_upArm_CT, l_foreArm_CT, l_hand_CT, l_shoulder_CT = chn(object).getArm('l_')[2:]   #arm
    r_upArm_CT, r_foreArm_CT, r_hand_CT, r_shoulder_CT = chn(object).getArm('r_')[2:]   # r_arm

    l_kneeIk_CT, l_footIk_CT, l_upLeg_CT, l_knee_CT, l_foot_CT, l_hip_CT = chn(object).getLeg('l_') #leg
    r_kneeIk_CT, r_footIk_CT, r_upLeg_CT, r_knee_CT, r_foot_CT, r_hip_CT = chn(object).getLeg('r_') #r_leg


    bodyContols = chn(object).body
    hips_CT = bodyContols.pop(1)
    torso_CT = bodyContols.pop(3)

    anim=''
    if ct in[l_hand_CT, r_hand_CT] :  anim = [ct,  ('rz',  60, -60 ),   ('ry', 90, -90 )]       ##   r
    if ct in [l_foreArm_CT, r_foreArm_CT] :  anim = [ct, ('rz', 135 )  ]                         ##   r
    if ct in [l_upArm_CT, r_upArm_CT] :  anim = [ct,      ('rz',  90, -75 ),   ('ry', 90, -70  )]  ##   r
    if ct in [l_shoulder_CT, r_shoulder_CT] :  anim = [ct,  ('ry',  -45, 35 ),   ('rz', 30, -15 )]  ##   r

    if ct in chn(object).getFingers('l_', oneList=True)[1:]  : anim = [ct, ('rz', 100 )]
    if ct in [chn(object).getFingers('l_', oneList=True)[0], ] : anim = [ct,  ('fist', 90, ), ('rz', 15, -15 ), ('ry', 10, -10 ), ] # l_handClinch_CT
    if ct in chn(object).getFingers('r_', oneList=True)[1:]  : anim = [ct, ('rz', 100 )]
    if ct in [chn(object).getFingers('r_', oneList=True)[0], ] : anim = [ct,  ('fist', 90, ), ('rz', 15, -15 ), ('ry', 10, -10 ), ] # l_handClinch_CT

    if ct in [l_footIk_CT, r_footIk_CT] :  anim = [ct,  ('footRoll',  100, -60 ),]
    if ct in [l_foot_CT, r_foot_CT] :  anim = [ct,  ('rz',  60, -60 ),]

    if ct in [l_knee_CT, r_knee_CT] :  anim = [ct, ('rz', 135 )  ]
    if ct in [l_upLeg_CT, r_upLeg_CT] :  anim = [ct,  ('rz',  90, -120 ),   ('ry', 30, -70  )]

    if ct in [chn(object).head[0]]  :  anim = [ct,  ('rz',  50, -50 ),   ('rx', 50, -50 )]
    if ct in [chn(object).neck[0]]  :  anim = [ct,  ('rz',  30, -30 ),   ('rx', 30, -30 )]

    if ct in bodyContols : anim = [ct,  ('rz',  45, -45 ),   ('rx', 45, -45 )]
    if ct== hips_CT : anim = [hips_CT,  ('rz',  45, -45 ),   ('rx', 45, -45 ),   ('ry', 90, -90 )]
    if ct== torso_CT : anim = [torso_CT,  ('rz',  45, -45 ),   ('rx', 45, -45 ),   ('ry', 90, -90 )]
    #chn(object).neck[:-1] +chn(object).head[0]

    if isKey (anim):
        cmds.currentTime(0)
        data = anim [1:]
        for attr in data:
            dir, valList = attr[0], attr[1:]
            cmds.cutKey( ct, t=(0,9000), attribute=dir, option="keys" )
    else:
        time = 0
        data  = anim [1:]
        for attr in data:
            dir, valList = attr[0], attr[1:]
            for val in  valList:
                setKey (ct, '.'+dir, time, val, interval)
                time=time+interval*2
    cmds.playbackOptions (min=0, max=interval*12)




def setKey (ct, attr, time, val, interval):
    cmds.setKeyframe( ct, attribute=attr, t=time, v=0 )
    cmds.setKeyframe( ct, attribute=attr, t=time+interval, v=val )
    cmds.setKeyframe( ct, attribute=attr, t=time+(interval*2), v=0 )

def isKey (anim):
    ct, data  = anim[0], anim [1:]
    for attr in data:
        dir, valList = attr[0], attr[1:]
        for val in  valList:
            if cmds.keyframe( ct, '.'+dir, query=True, keyframeCount=True ): return True
            else: return False


def testPers():
    persTestingUI()

