import maya.cmds as cmds
from An_Controllers import An_Controllers  as ctrl
from anProcedures import an_childCapture  as an_childCapture
from anProcedures import   an_helpLine  as  an_helpLine
#from An_CharNames import  An_CharNames as chn
from CharacterNames import  CharacterNames as chn


class An_Skeleton():
    def createSkeleton(self, sfx = "", gScale=1):
        dict = self.jntData if not self.jntCurrentData else  self.jntCurrentData
        for jnt in dict.keys():
            cmds.joint( n=jnt+sfx ) #create jnt
            if (cmds.listRelatives (jnt+sfx, p=True)):
                cmds.parent( jnt+sfx , world=True )
            cmds.setAttr(jnt+sfx+'.jointOrient', dict[jnt]['ori'][0], dict[jnt]['ori'][1], dict[jnt]['ori'][2], type="double3" )



            #cmds.xform (jnt+sfx, worldSpace=True, translation = dict[jnt]['pos'] )
            cmds.xform (jnt+sfx, worldSpace=True, translation = [x*gScale for x in dict[jnt]['pos']] )

        for jnt in dict.keys():
            if dict[jnt]['parent'] : cmds.parent (jnt+sfx, dict[jnt]['parent']+sfx )

    def __init__ (self, name="skelet"):
        self.name = name
        self.skelGrp = self.name+'_grp'

        self.rootJnt  = 'hips01_bind'   # body
        self.hipsJnt  = 'hips02_bind'
        self.torsoJnt = 'spine04_bind'
        self.spinJnt  = ['spine01_bind','spine02_bind','spine03_bind']
        self.neckJnt  = 'neck_bind'
        self.headJnt  = ['head_bind', 'head01_jnt']

        self.hipJnt  = 'l_hip_jnt'   #leg
        self.upLegJnt  = 'l_upLeg_jnt'   #leg
        self.lowLegJnt  = 'l_lowLeg_jnt'
        self.footJnt  = 'l_foot_bind'
        self.toeJnt  = ['l_toe_bind', 'l_toe1_jnt']
        self.shoulderJnt  = 'l_shoulder_bind'   #arm
        self.upArmJnt  = 'l_upArm_jnt'
        self.foreArmJnt  = 'l_foreArm_jnt'
        self.handJnt  = 'l_hand_bind'
        self.indexJnt = ['l_index'+str(x)+'_bind' for x in xrange(1,6)]#fingers
        self.middleJnt = ['l_middle'+str(x)+'_bind' for x in xrange(1,6)]
        self.ringJnt = ['l_ring'+str(x)+'_bind' for x in xrange(1,6)]
        self.pinkyJnt = ['l_pinky'+str(x)+'_bind' for x in xrange(1,6)]
        self.thumbJnt = ['l_thumb'+str(x)+'_bind' for x in xrange(1,5)]
        self.legRevers = ['l_legRevers'+str(x)+'_jnt' for x in xrange(1,8)]# Revers
        self.armRevers = ['l_armRevers'+str(x)+'_jnt' for x in xrange(1,5)]

        self.jntCurrentData = {}

        self.jntData =  {
                        self.rootJnt: {  'pos': [0.0, 13.0, 0.0], 'parent': None, 'ori': [90.0, 0.0, 90.0] }, # body
                        self.hipsJnt: {  'pos': [0.0, 13.0, 0.0], 'parent': self.rootJnt, 'ori': [90.0, 0.0, 90.0]},
                        self.spinJnt[0]:{'pos': [0.0, 14.667, 0.0], 'parent': self.rootJnt, 'ori': [90.0, 0.0, 90.0]},     #sp01
                        self.spinJnt[1]:{'pos': [0.0, 16.333, 0.0], 'parent': self.spinJnt[0], 'ori': [90.0, 0.0, 90.0]},    #sp02
                        self.spinJnt[2]:{'pos': [0.0, 18.0, 0.0], 'parent': self.spinJnt[1], 'ori': [90.0, 0.0, 90.0]},   #sp03
                        self.torsoJnt: { 'pos': [0.0, 19.0, 0.0], 'parent': self.spinJnt[2], 'ori': [90.0, 0.0, 90.0]},   #sp04
                        self.neckJnt: {  'pos': [0.0, 21.0, 0.0], 'parent': self.torsoJnt, 'ori': [90.0, 0.0, 90.0]},
                        self.headJnt[0]: { 'pos': [0.0, 22.0, 0.0], 'parent': self.neckJnt, 'ori': [90.0, 0.0, 90.0]},
                        self.headJnt[1]: { 'pos': [0.0, 24.0, 0.0], 'parent': self.headJnt[0], 'ori': [90.0, 0.0, 90.0]},

                        self.hipJnt:   { 'pos': [0.5, 13.0, 0.0], 'parent': self.hipsJnt, 'ori': [-90.0, -0.0, 0.0]}, #leg
                        self.upLegJnt: { 'pos': [3.0, 12.0, 0.0], 'parent': self.hipJnt,  'ori': [-90.0, -0.0, -90.0]},
                        self.lowLegJnt:{ 'pos': [3.0, 6.0, 0.0], 'parent': self.upLegJnt, 'ori': [-90.0, -0.0, -90.0]},
                        self.footJnt: {  'pos': [3.0, 1.0, 0.0], 'parent': self.lowLegJnt, 'ori': [-90.0, -71.56, -90.0]},
                        self.toeJnt[0]: { 'pos': [3, 0.33, 2.0], 'parent': self.footJnt, 'ori': [-90.0, -71.56, -90.0]},
                        self.toeJnt[1]:{ 'pos': [3.0, 0.0, 3.0], 'parent': self.toeJnt[0], 'ori': [-90.0, -71.56, -90.0]},

                        self.legRevers[0]:{'pos': [2.0, 0.0, 1.0], 'parent': None,               'ori': [0.0, -0.0, 0.0]},  #legRevers
                        self.legRevers[1]: {'pos': [4.0, 0.0, 1.0], 'parent': self.legRevers[0], 'ori': [0.0, 180.0, 0.0]},
                        self.legRevers[2]: {'pos': [3.0, 0.0, -1.0], 'parent': self.legRevers[1], 'ori': [0.0, -90.0, 0.0]},
                        self.legRevers[3]: {'pos': [3.0, 0.0, 2.0], 'parent': self.legRevers[2], 'ori': [0.0, -90.0, 0.0]},
                        self.legRevers[4]: {'pos': [3.0, 0.0, 3.0], 'parent': self.legRevers[3], 'ori': [0.0, 90.0, 0.0]},
                        self.legRevers[5]: {'pos': [3, 0.33, 2.0], 'parent': self.legRevers[4], 'ori': [90.0, 71.5, 90.0]},
                        self.legRevers[6]: {'pos': [3.0, 1.0, 0.0], 'parent': self.legRevers[5], 'ori': [90.0, 71.5, 90.0]},

                        self.shoulderJnt:{'pos': [0.5, 19.0, 1.0], 'parent': self.torsoJnt, 'ori': [90.0, 21.8, 0.0] }, #arm
                        self.upArmJnt:{   'pos': [3.00, 19.0, 0.0], 'parent': self.shoulderJnt, 'ori': [90.0, 0.0, 0.0] },
                        self.foreArmJnt:{ 'pos': [7.0, 19.0, 0.0], 'parent': self.upArmJnt, 'ori': [90.0, 0.0, 0.0] },
                        self.handJnt:{    'pos': [11.0, 19.0, 0.0], 'parent': self.foreArmJnt, 'ori': [90.0, 0.0, 0.0] },

                        self.indexJnt[0]:{'pos': [11.25, 19.0, 0.5], 'parent': self.handJnt, 'ori': [-180.0, -17.0, 0.0] }, # index fingers
                        self.indexJnt[1]:{'pos': [12.0, 19.0, 0.73], 'parent': self.indexJnt[0], 'ori': [-180.0, -17.0, 0.0]  },
                        self.indexJnt[2]:{'pos': [12.59, 19.0, 0.87], 'parent': self.indexJnt[1], 'ori': [-180.0, -17.0, 0.0]  },
                        self.indexJnt[3]:{'pos': [13.08, 19.0, 1.01], 'parent': self.indexJnt[2], 'ori': [-180.0, -17.0, 0.0]   },
                        self.indexJnt[4]:{'pos': [13.57, 19.0, 1.16], 'parent': self.indexJnt[3], 'ori': [-180.0, -17.0, 0.0]  },

                        self.middleJnt[0]:{'pos': [11.25, 19.0, 0.16], 'parent': self.handJnt, 'ori': [-180.0, -5.44, 0.0] }, # middle fingers
                        self.middleJnt[1]:{'pos': [12.09, 19.0, 0.24], 'parent': self.middleJnt[0], 'ori': [-180.0, -5.44, 0.0]  },
                        self.middleJnt[2]:{'pos': [12.59, 19.0, 0.29], 'parent': self.middleJnt[1], 'ori': [-180.0, -5.44, 0.0] },
                        self.middleJnt[3]:{'pos': [12.99, 19.0, 0.338], 'parent': self.middleJnt[2], 'ori': [-180.0, -5.44, 0.0] },
                        self.middleJnt[4]:{'pos': [13.57, 19.0, 0.38], 'parent': self.middleJnt[3], 'ori': [-180.0, -5.44, 0.0] },

                        self.ringJnt[0]:{'pos': [11.25, 19.0, -0.166], 'parent': self.handJnt,   'ori': [180.0, 5.36, 0.0] }, # ring fingers
                        self.ringJnt[1]:{'pos': [12.09, 19.0, -0.24], 'parent': self.ringJnt[0], 'ori': [180.0, 5.36, 0.0]  },
                        self.ringJnt[2]:{'pos': [12.59, 19.0, -0.29], 'parent': self.ringJnt[1], 'ori': [180.0, 5.36, 0.0]  },
                        self.ringJnt[3]:{'pos': [13.08, 19.0, -0.338], 'parent': self.ringJnt[2], 'ori': [180.0, 5.36, 0.0]   },
                        self.ringJnt[4]:{'pos': [13.57, 19.0, -0.38], 'parent': self.ringJnt[3], 'ori': [180.0, 5.36, 0.0]  },

                        self.pinkyJnt[0]:{'pos': [11.25, 19.0, -0.5],  'parent': self.handJnt,   'ori': [180.0, 15.72, 0.0]  }, # pinky fingers
                        self.pinkyJnt[1]:{'pos': [12.0, 19.0, -0.73],  'parent': self.pinkyJnt[0], 'ori': [180.0, 15.72, 0.0]   },
                        self.pinkyJnt[2]:{'pos': [12.59, 19.0, -0.87], 'parent': self.pinkyJnt[1], 'ori': [180.0, 15.72, 0.0]   },
                        self.pinkyJnt[3]:{'pos': [13.08, 19.0, -1.01], 'parent': self.pinkyJnt[2], 'ori': [180.0, 15.72, 0.0]    },
                        self.pinkyJnt[4]:{'pos': [13.57, 19.0, -1.15], 'parent': self.pinkyJnt[3], 'ori': [180.0, 15.72, 0.0]   },

                        self.thumbJnt[0]:{'pos': [11.09, 19.0, 0.35], 'parent': self.handJnt, 'ori':  [180, -90, 0.0] }, # thumb fingers
                        self.thumbJnt[1]:{'pos': [11.09, 19.0, 1.05], 'parent': self.thumbJnt[0], 'ori':  [180, -90, 0.0]  },
                        self.thumbJnt[2]:{'pos': [11.09, 19.0, 1.38], 'parent': self.thumbJnt[1], 'ori':  [180, -90, 0.0]  },
                        self.thumbJnt[3]:{'pos': [11.09, 19.0, 1.71], 'parent': self.thumbJnt[2], 'ori':  [180, -90, 0.0]  },

                        self.armRevers[0]: {'pos': [12.0, 18.74, 1.0], 'parent': None,              'ori': [0.0, 90.0, 0.0]},  #armRevers
                        self.armRevers[1]: {'pos': [12.0, 18.74, -1.0],'parent': self.armRevers[0], 'ori': [0.0, -90.0, 0.0]},
                        self.armRevers[2]: {'pos': [12.0, 19.08, 0.0], 'parent': self.armRevers[1], 'ori': [0.0, 180.0, 5.0]},
                        self.armRevers[3]: {'pos': [11.0, 19.0, 0.0],  'parent': self.armRevers[2], 'ori': [0.0, 180.0, 5.0]},
                        }

        self.templateData =  {
                        self.rootJnt:   { 'type':'body',   'sz':6,  'ofsShape': [0,0,0,0,0,90],   'prntCt': 'general_CT',  'xAim':self.spinJnt[0], 'zAim':self.rootJnt },  # body
                        self.hipsJnt:   { 'type':'sphere', 'sz':1.5,  'ofsShape': None,             'prntCt': self.rootJnt,  'xAim':self.hipsJnt, 'zAim':self.hipsJnt },
                        self.spinJnt[0]:{ 'type':'sphere', 'sz':.5, 'ofsShape': None,'prntCt':[(self.rootJnt, .66),(self.spinJnt[2], .33)], 'xAim':self.spinJnt[1], 'zAim':self.rootJnt},
                        self.spinJnt[1]:{ 'type':'sphere', 'sz':.5, 'ofsShape': None,'prntCt':[(self.rootJnt, .33),(self.spinJnt[2], .66)], 'xAim':self.spinJnt[2], 'zAim':self.rootJnt},
                        self.spinJnt[2]:{ 'type':'fkBody', 'sz':5, 'ofsShape': [0,0,0,0,90,90], 'prntCt':'general_CT',      'xAim':self.torsoJnt, 'zAim':self.rootJnt},
                        self.torsoJnt:  { 'type':'sphere', 'sz':1, 'ofsShape': None, 'prntCt': self.spinJnt[2],      'xAim':self.neckJnt, 'zAim':self.rootJnt},
                        self.neckJnt:   { 'type':'fk',     'sz':2, 'ofsShape': [0,0,0,0,0,90],  'prntCt': self.torsoJnt ,    'xAim':self.headJnt[0], 'zAim':self.rootJnt},
                        self.headJnt[0]:{ 'type':'head',   'sz':4, 'ofsShape': [0,0,0,90,90,0], 'prntCt': self.neckJnt,      'xAim':self.headJnt[1], 'zAim':self.rootJnt},
                        self.headJnt[1]:{ 'type':None,     'sz':2, 'ofsShape': None,            'prntCt':  self.headJnt[0] , 'xAim':None,            'zAim':self.headJnt[0]},



                        self.hipJnt: { 'type':'sphere',    'sz':1,  'ofsShape': None,   'prntCt': self.rootJnt,                             'xAim':self.upLegJnt, 'zAim':self.hipJnt },   #leg
                        self.upLegJnt: { 'type':'sphere',    'sz':1,  'ofsShape': None,   'prntCt': 'general_CT',                             'xAim':self.lowLegJnt, 'zAim':self.upLegJnt },   #leg
                        self.lowLegJnt:{ 'type':'sphere',    'sz':.5, 'ofsShape': None,   'prntCt': [(self.upLegJnt, .5), (self.footJnt, .5)],'xAim':self.footJnt, 'zAim':self.upLegJnt },
                        self.footJnt: {  'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                              'xAim':self.toeJnt[0], 'zAim':self.upLegJnt },
                        self.toeJnt[0]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                              'xAim':self.toeJnt[1], 'zAim':self.upLegJnt },
                        self.toeJnt[1]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                              'xAim':None,           'zAim':self.toeJnt[0]},


                        self.legRevers[0]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                           'xAim':self.legRevers[1], 'zAim':self.legRevers[0]},#legRevers
                        self.legRevers[1]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                           'xAim':self.legRevers[0], 'zAim':self.legRevers[1]},
                        self.legRevers[2]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                           'xAim':self.legRevers[3], 'zAim':self.legRevers[2]},
                        self.legRevers[3]: {'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': 'legIk_CT',                           'xAim':self.legRevers[4], 'zAim':self.legRevers[3]},
                        self.legRevers[4]: {'type':None,        'sz':.5,  'ofsShape': None,   'prntCt': self.toeJnt[1],                       'xAim':self.legRevers[2], 'zAim':self.legRevers[4]},
                        self.legRevers[5]: {'type':None,        'sz':.5,  'ofsShape': None,   'prntCt': self.toeJnt[0],                       'xAim':self.legRevers[6], 'zAim':self.legRevers[5]},
                        self.legRevers[6]: {'type':None,        'sz':.3,  'ofsShape': None,   'prntCt': self.footJnt,                         'xAim':None,              'zAim':self.legRevers[5]},

                        self.shoulderJnt: {'type':'sphere',     'sz':.5,  'ofsShape': None,   'prntCt': self.torsoJnt,                        'xAim':self.upArmJnt,    'zAim':self.shoulderJnt},   #arm
                        self.upArmJnt: {'type':'shoulder',      'sz':2,  'ofsShape': [0,0,0,180,0,90],  'prntCt': self.torsoJnt,                          'xAim':self.foreArmJnt,    'zAim':self.handJnt},
                        self.foreArmJnt: {'type':'sphere',      'sz':.5, 'ofsShape': None,   'prntCt':[(self.upArmJnt, .5), (self.handJnt, .5)],'xAim':self.handJnt,    'zAim':self.handJnt},
                        self.handJnt :{ 'type':'handIk',         'sz':2, 'ofsShape': [0,0,0,0,180,90], 'prntCt':  'general_CT' ,                 'xAim':self.handJnt,    'zAim':self.handJnt},

                        self.indexJnt[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.indexJnt[1], 'zAim':self.indexJnt[0]},
                        self.indexJnt[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.indexJnt[2], 'zAim':self.indexJnt[4]},
                        self.indexJnt[2]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.indexJnt[1], .66), (self.indexJnt[4], .33)],  'xAim':self.indexJnt[3], 'zAim':self.indexJnt[4]},
                        self.indexJnt[3]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.indexJnt[1], .33), (self.indexJnt[4], .66)], 'xAim':self.indexJnt[4], 'zAim':self.indexJnt[4]},
                        self.indexJnt[4]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                      'xAim':self.indexJnt[4], 'zAim':self.indexJnt[4]},

                        self.middleJnt[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.middleJnt[1], 'zAim':self.middleJnt[0]},
                        self.middleJnt[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.middleJnt[2], 'zAim':self.middleJnt[4]},
                        self.middleJnt[2]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.middleJnt[1], .66), (self.middleJnt[4], .33)], 'xAim':self.middleJnt[3], 'zAim':self.middleJnt[4]},
                        self.middleJnt[3]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.middleJnt[1], .33), (self.middleJnt[4], .66)], 'xAim':self.middleJnt[4], 'zAim':self.middleJnt[4]},
                        self.middleJnt[4]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                      'xAim':self.middleJnt[4], 'zAim':self.middleJnt[4]},

                        self.ringJnt[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.ringJnt[1], 'zAim':self.ringJnt[0]},
                        self.ringJnt[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.ringJnt[2], 'zAim':self.ringJnt[4]},
                        self.ringJnt[2]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.ringJnt[1], .66), (self.ringJnt[4], .33)], 'xAim':self.ringJnt[3], 'zAim':self.ringJnt[4]},
                        self.ringJnt[3]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.ringJnt[1], .33), (self.ringJnt[4], .66)], 'xAim':self.ringJnt[4], 'zAim':self.ringJnt[4]},
                        self.ringJnt[4]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                      'xAim':self.ringJnt[4], 'zAim':self.ringJnt[4]},

                        self.pinkyJnt[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.pinkyJnt[1], 'zAim':self.pinkyJnt[0]},
                        self.pinkyJnt[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.pinkyJnt[2], 'zAim':self.pinkyJnt[4]},
                        self.pinkyJnt[2]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.pinkyJnt[1], .66), (self.pinkyJnt[4], .33)], 'xAim':self.pinkyJnt[3], 'zAim':self.pinkyJnt[4]},
                        self.pinkyJnt[3]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.pinkyJnt[1], .33), (self.pinkyJnt[4], .66)], 'xAim':self.pinkyJnt[4], 'zAim':self.pinkyJnt[4]},
                        self.pinkyJnt[4]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                      'xAim':self.pinkyJnt[4], 'zAim':self.pinkyJnt[4]},

                        self.thumbJnt[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.thumbJnt[1], 'zAim':self.thumbJnt[0]},
                        self.thumbJnt[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.thumbJnt[2], 'zAim':self.thumbJnt[3]},
                        self.thumbJnt[2]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt':[(self.thumbJnt[1], .5), (self.thumbJnt[3], .5)], 'xAim':self.thumbJnt[3], 'zAim':self.thumbJnt[3]},
                        self.thumbJnt[3]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                    'xAim':self.thumbJnt[3], 'zAim':self.thumbJnt[3]},


                        self.armRevers[0]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.armRevers[1], 'zAim':self.armRevers[0]},
                        self.armRevers[1]:{'type':'sphere',    'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                     'xAim':self.armRevers[0], 'zAim':self.armRevers[1]},
                        self.armRevers[2]:{'type':None,        'sz':.5,  'ofsShape': None,   'prntCt':[(self.ringJnt[1], .5), (self.middleJnt[1], .5)], 'xAim':self.handJnt, 'zAim':self.armRevers[3]},
                        self.armRevers[3]:{'type':None,        'sz':.5,  'ofsShape': None,   'prntCt': self.handJnt,                                    'xAim':self.armRevers[3], 'zAim':self.armRevers[3]},

                        }



    def skeletFromTemplate(self):
        self.jntCurrentData = self.getSkelHi([jnt for jnt in self.jntData.keys()if not self.jntData[jnt]['parent']])
        cmds.delete ('general_CT')
        self.createSkeleton()

    def getJntInfo(self, jnt):
        poz = cmds.xform  (jnt, query=True,  worldSpace=True, translation=True)
        ori = cmds.xform  (jnt, query=True,  worldSpace=True, rotation=True)
        parType = True if cmds.nodeType( cmds.listRelatives(jnt, p=True)[0])=='joint' else False
        par = cmds.listRelatives(jnt, p=True)[0]   if cmds.listRelatives(jnt, p=True) and parType else None
        rotOrder = cmds.getAttr (jnt+".rotateOrder", asString=True )
        return   {'pos':poz, 'ori':ori, 'parent':par }    #   'oriSis':self.jntData[jnt]['oriSis']}

    def getSkelHi(self, jnt, level = 0, output=None):
        """
        @param[in] jnt    - you specify one or more rooot joints
        @param[in] level  -service attribute, do not tach it
        @param[in] output  - service attribute, do not tach it
        """
        if output is None: # in first iteration output=None
            output = {}
        if not type(jnt) == list:        #if you specify one bone
            output [jnt]= self.getJntInfo(jnt)  #get jnt info
            #print level*'    ', jnt, '  ', output [jnt]  # print it
            child =  cmds.listRelatives (jnt, c = True)
            #print child, type(jnt)
            if child:
                for each in filter(lambda x: cmds.nodeType(x) == 'joint', child):
                    self.getSkelHi (each, level+1, output )
            return output
        else:                                                         #if you specify list of bones
            for each in jnt : self.getSkelHi(each,  level = 0, output=output )
        self.jntCurrentData = output
        return output

    def templateCtrl(self, gScale=1):
        jenCT = ctrl('general_CT') #make general class object
        jenCT.makeController( 'general',  size = gScale*12, offset = [0, 0, gScale] )

        for attr, val in [('axisVisibility', [1, 0]), ('axesSize', [10, 1]), ('controllersVisibility', [1, 1]),  ('SpheresSize', [10, 1]), ('jointVisibility', [1, 0]), #add attr
                            ('handAxisVisibility', [1, 1]), ('handReversVisibility', [1, 0]), ('legAxisVisibility', [1, 1]), ('legReversVisibility', [1, 0]),]:
            cmds.addAttr(jenCT.name, longName=attr, defaultValue=val[1], minValue=0.0, maxValue=val[0], k=True)

        scaleGrp = cmds.group (em=True, n='ctScale_grp' )
        cmds.parent ( scaleGrp, jenCT.name )

        for dem in ('.sx', '.sy', '.sz',): cmds.connectAttr (jenCT.name+'.SpheresSize', scaleGrp+dem  )

        self.createSkeleton(sfx = "", gScale=gScale)
#"""

        for jnt in self.templateData.keys():    #for all root joints
            if not self.jntData[jnt]['parent']:
                cmds.parent (jnt, jenCT.name)
                cmds.connectAttr (jenCT.name+'.jointVisibility', jnt+'.v')

        legCT = ctrl('legIk_CT') #make legCT class object
        legCT.makeController( 'legIk',  size = gScale*4.5, offset = [0, -1*gScale, 0])
        legCT.gropeCT()
        legCT.placeCT (self.footJnt, 'point')
        cmds.parent ( legCT.oriGrp, jenCT.name )
        legCT.addColor ( jenCT.name, 'left')

        for jnt in self.templateData.keys():
            ctObj = ctrl(chn(jnt).divideName()[0]+chn(jnt).divideName()[1]+'_CT')  #________controller_______
            if self.templateData[jnt]['type']:    ctObj.makeController( self.templateData[jnt]["type"], self.templateData[jnt]["sz"]*gScale ) # make Controller
            else:  ctObj.makeController( 'fk', gScale )

            if self.templateData[jnt]["ofsShape"]:
                ctObj.moveCt ( self.templateData[jnt]["ofsShape"][:3])     # ofset Shape
                ctObj.rotateCt (self.templateData[jnt]["ofsShape"][3:])
            ctObj.gropeCT()                                                 # grope CT
            ctObj.placeCT (jnt, 'parent')                                   # place CT
            cmds.pointConstraint (ctObj.name, jnt)
            cmds.connectAttr (jenCT.name+'.controllersVisibility', ctObj.name+'.v'  )

            if self.templateData[jnt]['type']=='sphere':  # define scale
                cmds.scaleConstraint (scaleGrp, ctObj.name)
                ctObj.hideAttr(['sx', 'sy', 'sz', 'v'])
            else: ctObj.hideAttr(['v'])


            oriCT = ctrl(chn(jnt).divideName()[0]+chn(jnt).divideName()[1]+'Ori_CT')       #________ori controller_______
            oriCT.makeOrientAxis( .5)
            oriCT.gropeCT()
            oriCT.placeCT (jnt, 'parent')
            cmds.parentConstraint (ctObj.name, oriCT.oriGrp)
            cmds.parent ( oriCT.oriGrp, jenCT.name )
            cmds.orientConstraint (oriCT.name, jnt)
            cmds.connectAttr (jenCT.name+'.axisVisibility', oriCT.name+'.v'  )
            for dem in ('.sx', '.sy', '.sz',): cmds.connectAttr (jenCT.name+'.axesSize', oriCT.name+dem   )
            ctColor = 'left' if chn(ctObj.name).divideName()[0]=='l_' else 'cntrFk'
            ctObj.addColor ( jenCT.name, ctColor)

            if not self.templateData[jnt]['type']: cmds.delete (cmds.listRelatives (ctObj.name, s=True)[0]) #delete shape of end CT


            if jnt in ([self.handJnt] +  self.indexJnt + self.middleJnt + self.ringJnt + self.pinkyJnt + self.thumbJnt ):
                cmds.connectAttr (jenCT.name+'.handAxisVisibility', oriCT.oriGrp+'.v'  )
            if jnt in ([self.footJnt] + self.toeJnt  ): cmds.connectAttr (jenCT.name+'.legAxisVisibility', oriCT.oriGrp+'.v'  )
            if jnt in self.legRevers : cmds.connectAttr (jenCT.name+'.legReversVisibility', oriCT.oriGrp+'.v'  )
            if jnt in self.armRevers  : cmds.connectAttr (jenCT.name+'.handReversVisibility', oriCT.oriGrp+'.v'  )

        for jnt in self.templateData.keys():                                                         # _________make CT hierarhy_________
            ctObj = ctrl(chn(jnt).divideName()[0]+chn(jnt).divideName()[1]+'_CT')  #make class object
            parentJnt = self.templateData[jnt]["prntCt"]
            if type(parentJnt) is str:                           #if parent is string
                cmds.parent ( ctObj.name.replace('_CT','_ori'), chn(parentJnt).divideName()[0]+chn(parentJnt).divideName()[1]+'_CT')
            if type(parentJnt) is list:                         #if parent is list
                for eachJnt, weght in parentJnt:
                    pCT = chn(eachJnt).divideName()[0]+chn(eachJnt).divideName()[1]+'_CT'
                    cmds.pointConstraint (pCT, ctObj.name.replace('_CT','_ori'), w=weght, mo=False)
                cmds.parent ( ctObj.name.replace('_CT','_ori'), jenCT.name )

            oriCT = ctrl(chn(jnt).divideName()[0]+chn(jnt).divideName()[1]+'Ori_CT')      # ________orient joints system_________
            up = chn(self.templateData[jnt]['zAim']).divideName()[0]+chn(self.templateData[jnt]['zAim']).divideName()[1]+'_CT'
            if self.templateData[jnt]['xAim'] : # usual jnt
                aim = chn(self.templateData[jnt]['xAim']).divideName()[0]+chn(self.templateData[jnt]['xAim']).divideName()[1]+'_CT'
                cmds.aimConstraint (aim, oriCT.name.replace('_CT','_con'), wuo = up, wut = 'objectrotation',u=[0.0, 0.0, 1.0],wu=[0.0, 0.0, 1.0])
            else:  #end jnt
                up = chn(self.templateData[jnt]['zAim']).divideName()[0]+chn(self.templateData[jnt]['zAim']).divideName()[1]+'Ori_CT'
                cmds.orientConstraint (up, oriCT.name.replace('_CT','_con'))
                                                                                    # line
        bLine = [self.toeJnt[1], self.toeJnt[0], self.footJnt, self.lowLegJnt, self.upLegJnt, self.hipJnt, self.rootJnt, self.spinJnt[0], self.spinJnt[1], self.spinJnt[2], self.torsoJnt, self.neckJnt, self.headJnt[0], self.headJnt[1]]
        aLine = [self.torsoJnt, self.shoulderJnt, self.upArmJnt, self.foreArmJnt, self.handJnt]
        for lst in (bLine, aLine, [self.handJnt]+self.indexJnt, [self.handJnt]+self.middleJnt, [self.handJnt]+self.ringJnt, [self.handJnt]+self.pinkyJnt , [self.handJnt]+self.thumbJnt ):
            cmds.parent ( an_helpLine(lst, name="line01_crv"), jenCT.name)
        cmds.delete('spine04_CT_scaleConstraint1')# fix litle error
#"""
#An_Skeleton().templateCtrl()
