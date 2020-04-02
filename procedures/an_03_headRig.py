from An_Skeleton import An_Skeleton  as Skel
from CharacterNames import CharacterNames as Name
from An_Space import An_Space as An_Space  
#from An_Controllers import An_Controllers  as ctrl 
from an_classControllers import AnControllers as ctrl 
import maya.cmds as cmds

def an_03_headRig(action = 'rig'):
    headJnt, Neck, Torso, Body_CT, Switch_CT, Parent_CT = Skel().headJnt, Skel().neckJnt, Skel().torsoJnt, Name().body[0], Name().general[0], Name().general[2]     
    if action =='rig': 
    
        headCT = ctrl(Name().head[0])  # make head Controller  
        headCT.makeController( 'head', 4*cmds.floatSliderGrp('ISG_gScale', q=True, v= True ) ) 
        #headCT.gropeCT()                                                
        headCT.placeCT (headJnt[0] , 'parent')
        cmds.delete (cmds.orientConstraint(headJnt[0], headCT.oriGrp, o=[-180, -90, 90] ))
        headCT.addColor ( Switch_CT, 'cntrFk')# add color to controls
        cmds.connectAttr (Switch_CT+".bodyCtrls", headCT.name + '.v' )
        headCT.hideAttr(['sx', 'sy', 'sz', 'v']) 
         
        
        headAimCT = ctrl(Name().head[1])  # make head aim Controller  
        headAimCT.makeController( 'headAim', 2*cmds.floatSliderGrp('ISG_gScale', q=True, v= True ) ) 
        #headAimCT.gropeCT()                                                
        headAimCT.placeCT (headJnt[0] , 'parent')
        cmds.delete (cmds.orientConstraint(headJnt[0], headAimCT.oriGrp, o=[-180, -90, 90] ))
        headAimCT.addColor ( Switch_CT, 'add')# add color to controls
        
        cmds.addAttr (headCT.name,  ln="aim_visibility", dv=0, min=0,  max=1, keyable=True)
        cmds.connectAttr (headCT.name +".aim_visibility",  headAimCT.name+".v")
        headAimCT.hideAttr(['sx', 'sy', 'sz', 'v']) 
        
        cmds.parent(headAimCT.oriGrp, headJnt[0] ) 
        cmds.setAttr (headAimCT.oriGrp+'.ty' ,cmds.getAttr(headJnt[0]+'.tx')*5 )
        cmds.parent(headAimCT.oriGrp, w=True) 
        
        targetAim = cmds.group (em=True,  n= Name(headAimCT.name).divideName()[1]) 
        targetAimGrp = cmds.group (targetAim, n= Name(headAimCT.name).divideName()[1]+"Offset") 
        
        cmds.delete (cmds.pointConstraint(headJnt[0], targetAimGrp ))
        
        cmds.aimConstraint (headAimCT.name, targetAim, upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=headAimCT.name)      
        
        #rotate space
        targetList =  [(Parent_CT, "general"), (Body_CT, "body"), (Torso, "torso"),  (Neck, "neck"), (targetAim, "aim")] 
        classObj = An_Space( headCT.name, headCT.conGrp, targetList,  spaceType='orient')
        classObj.rebildSpaceObj()
        #translate space
        targetList =  [(Parent_CT, "general"), (Body_CT, "body"), (Torso, "torso"),  (Neck, "neck")] 
        classObj = An_Space( headCT.name, headCT.conGrp, targetList,  spaceType='point')
        classObj.rebildSpaceObj()
        
        for attr in  ['.rSpace', '.tSpace']:  cmds.setAttr (headCT.name+attr, 3) 
         
        cmds.parentConstraint(headCT.name, headJnt[0], mo=True )
        cmds.parentConstraint(Neck, targetAimGrp, mo=True )
        rigGrp = cmds.group ( headCT.oriGrp, headAimCT.oriGrp, targetAimGrp , n= Name(headCT.name).divideName()[1]+'Rig_grp') 
        cmds.parent(rigGrp, Name().general[2])

    elif action =='delRig':  
        cmds.delete (Name(Name().head[0]).divideName()[1]+'Rig_grp')


 


















