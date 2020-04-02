import maya.cmds as cmds 
from CharacterNames import CharacterNames as chn
from An_Skeleton import An_Skeleton as skel
#from An_Controllers import An_Controllers  as ctrl 
from anProcedures import *
from an_classControllers import AnControllers as ctrl 

'''
def fingersScaleRig(info):
#turn Of 
    clinch_ct = chn('').getFingers( side=info['side'])[0]
    cmds.addAttr (clinch_ct, ln='handSize', keyable=True, dv=1)
    fingersRigJnt_grp =  info ['side']+'fingersJnt_grp' 
    fingersIk_grp =  info ['side']+'fingersIk_grp' 
    
    
    for dr in ['.sx', '.sy', '.sz']:
        cmds.connectAttr (clinch_ct+'.handSize',  fingersRigJnt_grp+dr)
        cmds.connectAttr (clinch_ct+'.handSize',  fingersIk_grp+dr)  
    info['fingersJnt']
    
'''


def an_07_fingersRig(action = 'rig', limb=''):    #'delRig', 

    if action =='rig':          ######### if rig mod  
        fingersRig(limb)
    
    elif action =='delRig':     ######### if delete mod:                                                                         
        if not limb:
            if not cmds.ls(sl=True): cmds.error ('Select joint!')
            limb = cmds.ls(sl=True)[0]  
        info = getInfo(limb)
        an_delSys( info ['side']+'fingersRig_grp')
       

def getInfo(limb): 
    info = {'side':chn(limb).divideName()[0], }   #get s  ide  
    info['pfx'] =  info['side']+'fingers' 
    info['handJnt'] = info['side']+''.join(chn(skel().handJnt).divideName()[1:]) 
    info['handCt'] = chn('').getArm(info['side'])[1]
    info['fingersJnt'] = [ x for x in (skel().indexJnt[0], skel().middleJnt[0], skel().ringJnt[0], skel().pinkyJnt[0],  skel().thumbJnt[0]) if cmds.objExists(x)]
    info['fingersJnt'] = [ x.replace('l_', info['side']) for x in (skel().indexJnt[0], skel().middleJnt[0], skel().ringJnt[0], skel().pinkyJnt[0],  skel().thumbJnt[0]) if cmds.objExists(x)]
    info['clinch'] = [ x.replace('l_', info['side']) for x in (skel().indexJnt[0], skel().middleJnt[0], skel().ringJnt[0], skel().pinkyJnt[0] ) if cmds.objExists(x)]
    info["color"] = ('left' if info['side']=='l_' else 'right')
    info['generalCt']= chn().general 
    return info

def fingersRig(limb=''): ####################################################################################

    if not limb:
        if not cmds.ls(sl=True): cmds.error ('Select joint!')
        limb = cmds.ls(sl=True)[0] 
    info = getInfo(limb)

    # 1. Made group
    fingersRigJnt_grp = cmds.group(em=True, n=info ['side']+'fingersJnt_grp')
    cmds.parentConstraint(info['handJnt'], fingersRigJnt_grp)
    fingersRigIk_grp =  cmds.group(em=True, n=info ['side']+'fingersIk_grp')
    
    objects = chn('').getArm(info['side'])[1], chn('').getArm(info['side'])[4], fingersRigIk_grp
    
    
    deleteObjectList = [an_mixViaConstraint (objects, type='parent', mixAttr = info['generalCt'][0]+'.'+ info['side']+'armIkFkSwitch')[2],]
    
    rigGrp= cmds.group(fingersRigJnt_grp, fingersRigIk_grp, n=info ['side']+'fingersRig_grp')
    
    # 2. Made Clinch system
    clinchCtObj=ctrl(chn('').getFingers( side=info['side'])[0])
    clinchCtObj.makeController('curvedArrow', 2)
    #clinchCtObj.gropeCT()
    clinchCtObj.rotateCt([0, -90, 0]) 
    clinchCtObj.placeCT ( info['fingersJnt'][1]  , 'parent')   # place CT 
    clinchCtObj.addColor ( info['generalCt'][0], info['color'])
    clinchCtObj.hideAttr(['sx', 'sy', 'sz', 'v']) 
    cmds.parent(clinchCtObj.oriGrp, fingersRigJnt_grp)
    
    oppozitCt = 'l_'+''.join(chn(clinchCtObj.name).divideName()[1:])  
    if info['side']=='r_' and cmds.objExists(oppozitCt) :
        ctrl(oppozitCt).mirrorShape(clinchCtObj.name) # correct semetry of rigth controllers
    
    clinchJnt = bildJntChain (info['clinch'], 'Clinch')
    cmds.parent(clinchJnt[0],  fingersRigJnt_grp )
    for index, cJnt in enumerate (clinchJnt[1:]):
        cmds.connectAttr (clinchCtObj.name+".r", cJnt +".r" )
        vPMA = cmds.createNode ('plusMinusAverage',  n = info['pfx']+'PMA')
        cmds.select (cJnt)
        oriVal = cmds.getAttr(cJnt+'.t')[0]
        cmds.connectAttr (clinchCtObj.name+".translate", vPMA +".input3D[0]")
        cmds.setAttr(vPMA +".input3D[1]", oriVal[0], oriVal[1], oriVal[2])
        cmds.connectAttr (vPMA +".output3D", cJnt +".translate")
        
        deleteObjectList.append(vPMA)
        
        #an_delSys(rigGrp, objList =[vPMA,])
        
    clinchJntCopy = cmds.duplicate( clinchJnt[0], inputConnections=True, renameChildren=True)
    cmds.parent(clinchJntCopy[0],  fingersRigIk_grp )
     
    # 3. Made revers ik and fk system for fingers
    bendJnt =[]
    allCtObjects =[]
    for i, sJnt in enumerate(info['fingersJnt']):  # revers
        jnts = an_childCapture(sJnt)
        if 'thumb' in sJnt: 
            jntRev =  bildJntChain ([jnts[0], jnts[-1]], 'Rev')
            cmds.parent(jntRev[0],  fingersRigJnt_grp )
        else: 
            jntRev = bildJntChain ([jnts[0], jnts[1], jnts[-1]], 'Rev')
            cmds.parent(jntRev[0],  clinchJnt[i] )
        
        ik = cmds.ikHandle( sj=jntRev[-2], ee=jntRev[-1], solver='ikSCsolver'  )[0]
        if 'thumb' in sJnt: cmds.parent(ik,  fingersRigIk_grp )
        else: 
            cmds.parent(ik, clinchJntCopy[i])
            cmds.orientConstraint  ( clinchJnt[i], ik, mo=True)
       
        bendJnt.append(jntRev)
        pfx=''.join(chn(sJnt).divideName()[:2])[:-1] #fk rig
        ctObjects, fkRigGrp = an_fkRig( jnts, pfx=pfx, ctSize=0.5)
        cmds.parent(fkRigGrp,  fingersRigJnt_grp )
        allCtObjects.append(ctObjects) 
        
        cmds.connectAttr (jntRev[-2]+'.rotate', ctObjects[-3].conGrp+'.rotate')
        
        for fkCt in ctObjects: fkCt.addColor ( info['generalCt'][0], info['color'])
        if not 'thumb' in sJnt:  cmds.parentConstraint  ( clinchJnt[i], ctObjects[0].conGrp )
        deleteObjectList.append(fkRigGrp)
    
    an_connectRigVis (rigGrp, [fingersRigIk_grp, clinchJnt[0], bendJnt[-1][0]])
    
    cmds.parent(rigGrp,  info['generalCt'][2] )
    cmds.connectAttr (info['generalCt'][0]+'.fingersCtrls', rigGrp+'.v')
    
# 3. Made spread, fist   
    for attr in ['spread', 'fist']:  cmds.addAttr (clinchCtObj.name, ln=attr, keyable=True) 
    
    for i, ctObg in enumerate([x for x in  allCtObjects if not 'thumb' in x[1].name]):  #add ofs grp and connect it to 'spread'
        ofs_grp = cmds.group(ctObg[1].name, n=''.join(chn(ctObg[0].name).divideName()[:2])[:-1]+"_ofs")
        cmds.xform (ofs_grp, os=True, piv=[0, 0, 0])
        
        spreadMDV = cmds.shadingNode ('multiplyDivide', n=''.join(chn(ctObg[0].name).divideName()[:2])[:-1]+'spreadMDV',  asUtility=True)
        cmds.connectAttr (clinchCtObj.name+'.spread',  spreadMDV+'.input1X')
        cmds.setAttr (spreadMDV+'.input2X', range(1,-5,-1)[i])
        cmds.connectAttr (spreadMDV+'.outputX',  ofs_grp+'.ry')
        deleteObjectList.append(spreadMDV)
        
        #an_delSys (rigGrp, [spreadMDV,])
  
        
    for ctObgs in [x for x in  allCtObjects if not 'thumb' in x[1].name]:  #fist rig 
        for ctObg in ctObgs[1:]:
            parentGrp = cmds.listRelatives(ctObg.name, p=True)[0]
            cmds.connectAttr ( clinchCtObj.name+'.fist', parentGrp+'.rz')
            
    an_delSys(rigGrp, objList = deleteObjectList)

# 4. Scale hand
    
    clinch_ct = chn('').getFingers( side=info['side'])[0]
    cmds.addAttr (clinch_ct, ln='handSize', keyable=True, dv=1)
    fingersIk_grp =  info ['side']+'fingersIk_grp' 
    
    for dr in ['.sx', '.sy', '.sz']:
        cmds.connectAttr (clinch_ct+'.handSize',  fingersRigJnt_grp+dr)
        cmds.connectAttr (clinch_ct+'.handSize',  fingersIk_grp+dr) 
        cmds.connectAttr (clinch_ct+'.handSize',  info['handJnt']+dr)
        
    for jnt in  info['fingersJnt']:
        cmds.setAttr (jnt+".segmentScaleCompensate", 0)

    return allCtObjects
#allCtObjects = fingersRig(limb='l_handIk_CT')


def bildJntChain (targList, sfx): #bild copy of Jnt Chain list and orient it  ####################################################################################
    cmds.select (cl=True)
    newJnt =[]
    for i, jnt in enumerate (targList): 
        cJnt = cmds.joint (n=''.join(chn(jnt).divideName()[:2])+sfx+'_jnt')
        newJnt.append(cJnt)
        cmds.delete (cmds.parentConstraint (jnt, cJnt))
        oriVal = cmds.getAttr(cJnt+'.r'   )[0]
        cmds.setAttr(cJnt+'.jointOrient', oriVal[0], oriVal[1], oriVal[2])
        cmds.setAttr(cJnt+'.r', 0, 0, 0)
    return newJnt

 


 


 
