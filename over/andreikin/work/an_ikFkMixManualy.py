






# procedury dlya rigginga dlinnyh ruk ik fk mix, i bend sistemy

from an_twistSegment import *
from CharacterNames import CharacterNames as chn
from An_Controllers import An_Controllers  as ctrl 



def twArmSys():
    scaleObj = 'r_general_CT'
    ctSt, ctEnd = cmds.ls(sl=True)
    pfx  = chn(ctSt).divideName()[0]+chn(ctSt).divideName()[1] 
    
    rigGrp = cmds.group(em=True, n=pfx+'TwRig_grp')# rig grp
    coord =  [[0,0,0], [1,0,0], [2,0,0]]
    
    curv = cmds.curve(n=pfx+"_crv", p=coord, d=2)
    cmds.setAttr (curv+".inheritsTransform", 0)
    cmds.parent(curv, rigGrp)
    
    ctObj = ctrl(pfx+'Mid')     # controller
    ctObj.makeController('circle', 2)               
    ctObj.rotateCt([0, 90, 90]) 
    ctObj.gropeCT() 
    cmds.setAttr (ctObj.oriGrp+".translateX", coord[1][0])
    
    clList = [pfx+str(i)+'_clst' for i in xrange(3)]
    for  idx, clst in enumerate(clList):
        clst = cmds.cluster (curv+ '.cv['+str(idx)+']',  n = clst)[1]
        tmp = ctrl(clList [idx]+'Handle')
        tmp.gropeCT()
    
    cmds.parent(clList [1]+'Handle_ori', ctObj.name)
    cmds.parent(clList[0]+'Handle_ori', clList[2]+'Handle_ori',  ctObj.oriGrp , rigGrp,)
    cmds.parent(rigGrp, ctSt)
    
    cmds.pointConstraint( ctSt, clList[2]+'Handle' )   
    cmds.pointConstraint( ctEnd, clList[0]+'Handle' )   
    cmds.pointConstraint( ctSt, ctEnd, ctObj.oriGrp ) 
    
    cmds.delete(cmds.orientConstraint( ctSt, ctObj.oriGrp, mo=False ) )
    
    armMixSys(ctObj.name)
    
    info={}
    info['pfx']= pfx
    info['scaleObj'] = scaleObj
    info['curveName']=curv
    info['jntNum'] = 10
    info['stretchable']=True
    obj1 = ctEnd  
    ax1  = 'z' 
    obj2 = ctSt
    ax2  =  'z' 
    info['twSettings'] =[(obj1,  ax1), (obj2, ax2)] # define up vector
    info['geo']= False
    info['subAx'] = 12
        
    twRigGrp = an_twistSegment (info) ['rigGrp']
    
    cmds.parent(twRigGrp, ctSt)





def twArmSys2ct():
  
    scaleObj = 'r_general_CT'
    
    ctSt, ctEnd = cmds.ls(sl=True)
    pfx  = chn(ctSt).divideName()[0]+chn(ctSt).divideName()[1] 
    
    rigGrp = cmds.group(em=True, n=pfx+'TwRig_grp')# rig grp
    coord =  [[0,0,0], [1,0,0], [2,0,0], [3,0,0]]
    
    curv = cmds.curve(n=pfx+"_crv", p=coord, d=2)
    cmds.setAttr (curv+".inheritsTransform", 0)
    cmds.parent(curv, rigGrp)
    
    ctObj = ctrl(pfx+'Mid')     # controller
    ctObj.makeController('circle', 2)               
    ctObj.rotateCt([0, 90, 90]) 
    ctObj.gropeCT() 
    cmds.setAttr (ctObj.oriGrp+".translateX", coord[1][0])
    
    ctObjB = ctrl(pfx+'Mid2')     # controller
    ctObjB.makeController('circle', 2)               
    ctObjB.rotateCt([0, 90, 90]) 
    ctObjB.gropeCT() 
    cmds.setAttr (ctObjB.oriGrp+".translateX", coord[2][0])
    
    clList = [pfx+str(i)+'_clst' for i in xrange(4)]
    for  idx, clst in enumerate(clList):
        clst = cmds.cluster (curv+ '.cv['+str(idx)+']',  n = clst)[1]
        tmp = ctrl(clList [idx]+'Handle')
        tmp.gropeCT()
    
    cmds.parent(clList [1]+'Handle_ori', ctObj.name)
    cmds.parent(clList [2]+'Handle_ori', ctObjB.name)
    
    cmds.parent(clList[0]+'Handle_ori', clList[3]+'Handle_ori',  ctObj.oriGrp ,  ctObjB.oriGrp ,    rigGrp,)
    cmds.parent(rigGrp, ctSt)
    
    cmds.pointConstraint( ctSt, clList[3]+'Handle' )   
    cmds.pointConstraint( ctEnd, clList[0]+'Handle' )
       
    cmds.pointConstraint( ctSt, ctEnd, ctObj.oriGrp ) 
    cmds.pointConstraint( ctSt, ctEnd, ctObjB.oriGrp ) 
     
    cmds.delete(cmds.orientConstraint( ctSt, ctObj.oriGrp, mo=False ) )
    cmds.delete(cmds.orientConstraint( ctSt, ctObjB.oriGrp, mo=False ) )
    
    armMixSys(ctObj.name)
    armMixSys(ctObjB.name)
    
    info={}
    info['pfx']= pfx
    info['scaleObj'] = scaleObj
    info['curveName']=curv
    info['jntNum'] = 10
    info['stretchable']=True
    obj1 = ctEnd  
    ax1  = 'z' 
    obj2 = ctSt
    ax2  =  'z' 
    info['twSettings'] =[(obj1,  ax1), (obj2, ax2)] # define up vector
    info['geo']= False
    info['subAx'] = 12
        
    twRigGrp = an_twistSegment (info) ['rigGrp']
    cmds.parent(twRigGrp, ctSt)




def armMixSys(ct):

    #ct = cmds.ls(sl=True)[0]
    pfx  = chn(ct).divideName()[0]+chn(ct).divideName()[1]
    
    conGrp = cmds.listRelatives(ct, p=True)[0]
    rigGrp = ct #cmds.listRelatives( cmds.listRelatives(conGrp, p=True)[0], p=True)[0]
    
    transforms =[pfx+'pos', pfx+'stat']
    for tr in transforms:
        cmds.group(em=True, n=tr)
        cmds.delete(cmds.parentConstraint(conGrp, tr))
        constr =cmds.parentConstraint(tr, conGrp)[0]
        cmds.parent(tr, cmds.listRelatives(conGrp, p=True)[0])
    
    ctAttr = rigGrp+'.mix'    
    if not cmds.objExists( ctAttr): 
            cmds.addAttr (ctAttr.split('.')[0],    longName=ctAttr.split('.')[1],  minValue=0, maxValue=1, k=True )
             
    cmds.connectAttr(ctAttr, constr+'.'+transforms[0]+'W0')
    an_connectReversAttr(ctAttr, constr+'.'+transforms[1]+'W1')      



def jntIkFkMixSys(ct):

    ctAttr ='r_general_CT.ikFkMix'
    
    jntList = an_childCapture('r_arm01_jnt') [:10] 
    jntFkList = an_childCapture('r_armFk01_jnt') [:10] 
    jntIkList = an_childCapture('r_armIk01_jnt') [:10] 
    
    #jntFkList =  [ x.replace (   '_jnt', 'Fk_jnt',  )  for x in  jntList ] 
    #jntIkList =  [ x.replace (   '_jnt', 'Ik_jnt',  )  for x in  jntList ]
    
    
    if not cmds.objExists( ctAttr): 
            cmds.addAttr (ctAttr.split('.')[0],    longName=ctAttr.split('.')[1],  minValue=0, maxValue=1, k=True )
    
    for i, jnt in enumerate (jntList):
        objects = [jntIkList[i], jntFkList[i], jntList[i]]
        print  objects
        an_mixViaConstraint (objects, type='parent', mixAttr=ctAttr)


#an_distans ( cmds.ls (sl=True)[0], cmds.ls (sl=True)[1], act='createSys')

#ct = cmds.ls (sl=True)[0]
#________________________________________________

#jntList = an_childCapture('r_arm01_jnt') [:7] 


def addCtForTw(): 

    jntList = ['r_arm01_jnt', 'r_arm02_jnt', 'r_arm03_jnt', 'r_arm04_jnt', 'r_arm05_jnt', 'r_arm06_jnt']
    
    jntList = ['l_arm01_jnt', 'l_arm02_jnt', 'l_arm03_jnt', 'l_arm04_jnt', 'l_arm05_jnt', 'l_arm06_jnt'] 
    
    
    for i, jnt in enumerate (jntList): #print jnt
        
        
        pfx  = chn(jnt).divideName()[0]+chn(jnt).divideName()[1]
        
        
        ctObj = ctrl(pfx+'Bend')     # controller
        
        ctObj.makeController('circle', 2)               
        ctObj.rotateCt([0, 90, 90]) 
        ctObj.gropeCT() 
        
        cmds.parentConstraint (jnt, ctObj.oriGrp)












