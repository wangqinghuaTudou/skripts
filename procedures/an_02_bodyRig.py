
import maya.cmds as cmds
#from An_Controllers import An_Controllers  as ctrl
from An_Skeleton import An_Skeleton  as skel
from CharacterNames import CharacterNames as chn
from  anProcedures import *   
from an_twistSegment import *
from an_classControllers import AnControllers as ctrl 

def getInfo():
    info = {'pfx':'body', 'madeTw':True, 'jNum': 10, 'subdiv':12 }
    info['gScale']= cmds.floatSliderGrp('ISG_gScale', q=True, v= True )
    info['twSettings']=[ (skel().spinJnt[2], 'z'), (skel().hipsJnt, 'z')]
    if  cmds.window ("bodyRigOptionWin", exists=True ):
        info['subdiv'] = cmds.intSliderGrp('ISG_rSab', q=True, v=True )
        info['jNum'] = cmds.intSliderGrp('ISG_jNum', q=True, v=True )
        info['madeTw']=False if not cmds.checkBoxGrp( 'bridgCHB' , q=True, v1=True) else True   
    info['ctrl'] = chn().body
    info['delList'] = []
    info['visList'] = []
    return info

def an_02_bodyRig(action = 'rig'):    

    info = getInfo()
    
    if action =='delRig':                                                                              
        pfx  = 'body'
        swCT =   chn().general[0]
        cmds.setAttr (swCT+".waistCtNumber", 2)
        an_delSys(pfx+'Rig_grp', [])
        cmds.deleteAttr (swCT, attribute="waistCtNumber")

    elif action =='option':
        win = "bodyRigOptionWin"
        if  cmds.window (win, exists=True ): cmds.deleteUI (win)
        cmds.window (win, t="Body Rig Option", width=420,  height=390, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ( adjustableColumn=True)
        cmds.canvas( height=10 )
        cmds.checkBoxGrp( 'bridgCHB' ,  numberOfCheckBoxes=1, label='Made twist system :   ', cc= "cmds.columnLayout ('bridgLayout', e=True, en=cmds.checkBoxGrp( 'bridgCHB' , q=True, v1=True))", v1=True)
        cmds.columnLayout ('bridgLayout', adjustableColumn=True)
        cmds.intSliderGrp('ISG_rSab', label='Radius subdivisions:', field=True, min=1, max=30,  v=12 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.intSliderGrp('ISG_jNum', label='Twist joint :', field=True, min=2, max=30,  v=10 , cw = [(1, 124), (2, 50) ], enable= True )
        cmds.showWindow()

    elif action =='rig':
        pfx  = info['pfx']
        swCT, jenCT, jenOffsCT = [ ctrl(chn().general[x])  for x in  range(3)]
                     
        # 1  Made body controllers ______________________________________
        bodyCT = ctrl(info['ctrl'][0])  # make body Controller
        bodyCT.makeController( 'body', 7*info['gScale'])
        #bodyCT.gropeCT()
        bodyCT.placeCT (skel().rootJnt , 'point')
        rigGrp = cmds.group(bodyCT.oriGrp, n=pfx+'Rig_grp')
        cmds.parent (rigGrp, jenOffsCT.name)
        cmds.parentConstraint (bodyCT.name, skel( ).rootJnt, mo=True)
        bodyCT.addColor ( swCT.name, 'cntrFk')# add color to controls
        
        ctData =  {    #data base to   'hips_CT', 'dw_waist_CT', 'up_waist_CT', 'torso_CT', 'shoulders_CT'
                   info['ctrl'][1]:   { 'type':'fkBody', 'depend':skel( ).hipsJnt,  'sz':5, 'parent': info['ctrl'][0],  'ofsShape': [0,-.7,0,0,0,0] ,  'ofsPos': [0,0,0,-180, -90, 90]  }, #'hips_CT'
                   info['ctrl'][2]:   { 'type':'fkBody', 'depend':skel( ).spinJnt[0],  'sz':5, 'parent': info['ctrl'][0],  'ofsShape': [0,0,0,0,0,0] ,  'ofsPos': [0,0,0,-180, -90, 90]  }, #'dw_waist_CT'
                   info['ctrl'][3]:   { 'type':'fkBody', 'depend':skel( ).spinJnt[1],  'sz':5, 'parent': info['ctrl'][2],  'ofsShape': [0,0,0,0,0,0] ,  'ofsPos': [0,0,0,-180, -90, 90]  }, #'up_waist_CT'
                   info['ctrl'][4]:   { 'type':'torso', 'depend':skel( ).spinJnt[2],  'sz':5, 'parent': info['ctrl'][3],  'ofsShape': [0,2,0,0,0,0] ,  'ofsPos': [0,0,0,-180, -90, 90]  }, #'torso_CT'
                   info['ctrl'][5]:   { 'type':'torso', 'depend':skel( ).torsoJnt,  'sz':5, 'parent': info['ctrl'][4],  'ofsShape': [0,2,0,0,0,0] ,  'ofsPos': [0,0,0,-180, -90, 90]  }, #'torso_CT'
                   }
        hipsObj, dw_waistObj, up_waistObj, torsoObj, shouldersObj = [ctrl(info['ctrl'][x])for x in  range(1,6)]
        info['objlist']= [bodyCT.name, rigGrp,] + [x.name for x in [hipsObj, dw_waistObj, up_waistObj, torsoObj, shouldersObj]]
        
        for ctObj in [hipsObj, dw_waistObj, up_waistObj, torsoObj, shouldersObj]:
            ctObj.makeController( ctData[ctObj.name]["type"], ctData[ctObj.name]["sz"]*info['gScale'] ) # make all Controller
            #ctObj.gropeCT()
            ctObj.moveCt  (ctData[ctObj.name]["ofsShape"][:3])     # ofset Shape
            ctObj.rotateCt(ctData[ctObj.name]["ofsShape"][3:])
            ctObj.placeCT (ctData[ctObj.name]["depend"]  , 'point')   # place CT
            cmds.delete (cmds.orientConstraint(ctData[ctObj.name]["depend"],  ctObj.oriGrp, o=ctData[ctObj.name]["ofsPos"][3:]))
            ctObj.addColor ( swCT.name, 'cntrFk')
            ctObj.hideAttr(['sx', 'sy', 'sz', 'v'])
        
        for ct in ctData.keys(): cmds.parent ( ct.replace('_CT','_ori'), ctData[ct]["parent"])
        cmds.connectAttr ( swCT.name+'.'+"bodyCtrls", bodyCT.name+'.v' )
        swCT.hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        jenCT.hideAttr(['v'])
        jenOffsCT.hideAttr(['sx', 'sy', 'sz', 'v'])
        
                          # 2  Set switching  the number of controllers______________________________________
        
        cmds.addAttr (swCT.name, ln='waistCtNumber',  at="enum", en="0:1:2", keyable=True )
        cmds.setAttr ( swCT.name+'.'+'waistCtNumber', keyable=False,  channelBox=True )
        
        midloc = cmds.spaceLocator()[0]
        cmds.pointConstraint(dw_waistObj.name, up_waistObj.name, midloc)
        cmds.orientConstraint(dw_waistObj.name, up_waistObj.name, midloc)
        
        targDw = (bodyCT.name,  midloc,  dw_waistObj.name)
        targUp = (bodyCT.name,  midloc,  up_waistObj.name)
        targTor =(torsoObj.name, torsoObj.name, torsoObj.name)
        
        pos={}
        for ctObj, targets in [(dw_waistObj, targDw),   (up_waistObj, targUp),   (torsoObj, targTor)]:  #get val
            for switchVal in xrange(0,3):
                pos[targets[switchVal]+'t']= cmds.xform(targets[switchVal], q=True, worldSpace=True, t=True )
                pos[targets[switchVal]+'r']= cmds.xform(targets[switchVal], q=True, worldSpace=True, ro=True )
        cmds.delete ()
        for ctObj, targets in [(dw_waistObj, targDw), (up_waistObj, targUp), (torsoObj, targTor)]:  #set dvk
            for switchVal in xrange(0,3):
                cmds.setAttr(swCT.name+'.'+'waistCtNumber', switchVal)
                conGrp =  cmds.listRelatives(ctObj.name, p=True)[0]
                cmds.xform(conGrp, worldSpace=True, t=pos[targets[switchVal]+'t'] )
                cmds.xform(conGrp, worldSpace=True, ro=pos[targets[switchVal]+'r'])
                for dem in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    val = cmds.getAttr(conGrp+'.'+dem)
                    cmds.setDrivenKeyframe (conGrp+'.'+dem,   cd= swCT.name+'.waistCtNumber',   dv = switchVal, v= val)
                if not ctObj.name == torsoObj.name:                                  #hide nessesery controllers
                    for eachCurve in cmds.listRelatives(ctObj.name, s=True):
                        val =  switchVal if ctObj.name == dw_waistObj.name else switchVal-1
                        if val>=0:   cmds.setDrivenKeyframe (eachCurve+'.v',   cd= swCT.name+'.waistCtNumber',   dv = switchVal, v= val)
        
        for ctObj in [hipsObj, dw_waistObj, up_waistObj, torsoObj, shouldersObj]:   #connect jnt to controls
            cmds.parentConstraint (ctObj.name, ctData[ctObj.name ]["depend"], mo=True)
        
        # 3  Made joint and curve for brige______________________________________
        if info['madeTw']:        
            pointPoz, curveSysOriJnt, curveSysJnt = [], [], []
            for jnt in [skel( ).hipsJnt,]+skel( ).spinJnt:
                pos=cmds.xform(jnt, q=True, worldSpace=True, t=True )
                pointPoz.append(pos)
                cmds.select (cl=True)
                curveSysOriJnt.append(cmds.joint (p = pos, n=chn(jnt).divideName()[1]+'CurveSysOri_jnt'))
                cmds.select (cl=True)
                curveSysJnt.append(cmds.joint (p = pos, n=chn(jnt).divideName()[1]+'CurveSys_jnt'))
            pointPoz.reverse()
            vCurve = cmds.curve (p =pointPoz, d=3, n=pfx+'Spine_crv')
                  
            #made jnt hierarhy
            cmds.parent ( curveSysOriJnt[1], curveSysOriJnt[0])
            cmds.parent ( curveSysOriJnt[2], curveSysOriJnt[3])
            
            #orient jnt
            for jnt in (curveSysOriJnt[0], curveSysOriJnt[3]): cmds.joint  (jnt, e=True, oj='xzy',  secondaryAxisOrient='xup', zso=True)
            for jnt in (curveSysOriJnt[1], curveSysOriJnt[2]): cmds.setAttr (jnt+".jointOrient", 0, 0, 0)
            for i in xrange(4): cmds.parent ( curveSysJnt[i], curveSysOriJnt[i])
            cmds.skinCluster(curveSysJnt, vCurve, tsb=True) #new skin to static jnt
            for jnt in curveSysJnt:
                cmds.addAttr(rigGrp, ln=jnt+'Offset', keyable= True)
                cmds.connectAttr( rigGrp+'.'+jnt+'Offset', jnt+'.tx'    )
                
            jntGrp = cmds.group(curveSysOriJnt[0], curveSysOriJnt[3], n=pfx + 'CurveSys_grp')  #group for joints
            cmds.parent ( jntGrp, rigGrp)
            for jntSkel, jnt in [(skel( ).hipsJnt, curveSysOriJnt[0]),  (skel( ).spinJnt[2], curveSysOriJnt[3])]: #constreints
                cmds.parentConstraint(jntSkel, jnt, mo=True)
            
                    # 4  Made brige if it nessesery______________________________________
            twInfo= {'pfx':pfx+'Tw',  'curveName':vCurve, 'jntNum': info['jNum'], 'stretchable': True, 'twSettings':  info['twSettings'], 'geo':True , 'subAx':12}
            twInfo['scaleObj'] = chn().general[1]
            twData =  an_twistSegment( twInfo)
        
            an_connectRigVis(rigGrp, [twData['rigGrp'], vCurve, jntGrp ])       
            an_delSys(rigGrp , [twData['rigGrp'], jntGrp,   ]) # vCurve, ikHandl[0],  geo,
            
            cmds.parent ( twData['rigGrp'], vCurve, rigGrp)
            cmds.addAttr (bodyCT.name, ln="squashSwitch", min=0, max=5 , keyable=True)
            cmds.connectAttr(bodyCT.name+'.squashSwitch ',  twInfo['rigGrp']+'.sqSwitch')        
            cmds.setAttr (vCurve+".inheritsTransform", 0)

        bodyCT.hideAttr(['sx', 'sy', 'sz', 'v'])
        an_saveLoadData(data=info, obgect=rigGrp, delAttr = False)
        
        print "body ok"
        











