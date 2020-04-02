
import maya.cmds as cmds
from CharacterNames import CharacterNames as chn

def an_testAnim():
    controllers = cmds.ls( sl=True )
    for ct in controllers: doTestAnim (ct)
    cmds.select (controllers)

def doTestAnim (ct):
#ct =    cmds.ls( sl=True )[0]

    cmds.select (ct)
    switchCt = chn(object).general[0]
    interval = 30

    upArm_CT, foreArm_CT, l_hand_CT, l_shoulder_CT = chn(object).getArm('l_')[2:]   #arm
    upLeg_CT, knee_CT, foot_CT, hip_CT = chn(object).getLeg('l_')[2:]   #leg

    bodyContols = chn(object).body
    hips_CT = bodyContols.pop(1)
    torso_CT = bodyContols.pop(3)


    anim=''
    if ct == l_hand_CT :  anim = [l_hand_CT,  ('rz',  60, -60 ),   ('ry', 90, -90 )]
    if ct == foreArm_CT :  anim = [foreArm_CT, ('rz', 135 )  ]
    if ct == upArm_CT :  anim = [upArm_CT,      ('rz',  90, -75 ),   ('ry', 90, -70  )]
    if ct == l_shoulder_CT :  anim = [l_shoulder_CT,  ('ry',  -45, 35 ),   ('rz', 30, -15 )]


    if ct in chn(object).getFingers('l_', oneList=True)[1:]  : anim = [ct, ('rz', 100 )]
    if ct in [chn(object).getFingers('l_', oneList=True)[0], ] : anim = [ct,  ('fist', 90, ), ('rz', 15, -15 ), ('ry', 10, -10 ), ] # l_handClinch_CT

    if ct == foot_CT :  anim = [foot_CT,  ('rz',  60, -60 ),]
    if ct == knee_CT :  anim = [knee_CT, ('rz', 135 )  ]
    if ct == upLeg_CT :  anim = [upLeg_CT,      ('rz',  90, -120 ),   ('ry', 30, -70  )]

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

























