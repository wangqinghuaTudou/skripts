import maya.cmds as cmds      
#from An_Controllers import An_Controllers  as ctrl 
from An_Skeleton import  An_Skeleton as An_Skeleton
from an_classNames import AnNames as CharacterNames 
from  anProcedures import *
from an_classControllers import AnControllers as ctrl 

def an_01_foldersHierarhy(action = 'rig'): 

    jnts =[An_Skeleton().rootJnt,  An_Skeleton().legRevers[0].replace('l_', 'r_'), An_Skeleton().armRevers[0].replace('l_', 'r_'), An_Skeleton().legRevers[0] ,  An_Skeleton().armRevers[0]]
    if action == 'rig':  
    #############################   
        CharacterNames().rigStructure(make=True) # made folders
        
        normFolder = 'geo_normal'
        midFolder =  'geo_middle'
        proxyBody_grp = 'proxyBody_grp'
        proxyHead_grp = 'proxyHead_grp'
        lowFolder =  'geo_low'
        sProxyBody_grp = 'sProxyBody_grp'
        sProxyHead_grp = 'sProxyHead_grp'
        loClothProxyGeo_grp ='loClothProxyGeo_grp' 
        upClothProxyGeo_grp ='upClothProxyGeo_grp'
        accessoriesProxyGeo_grp = 'accessoriesProxyGeo_grp'
        
        ctData = {  'switch_CT':['switch',2, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'] ], 
                    'general_CT':['general',16,['v']    ], 
                    'pivotOffset_CT':['general',12,['sx', 'sy', 'sz', 'v']    ] }
        
        switchObj, generalObj, pivotOffsetObj   = [ctrl(x)for x in ctData.keys()] # made CT
        
        for CT in [switchObj, generalObj, pivotOffsetObj]:
            CT.makeController( ctData[CT.name][0],  size =  ctData[CT.name][1]*cmds.floatSliderGrp('ISG_gScale', q=True, v= True )) 
            CT.addColor ( 'switch_CT', 'cntrFk')
            if CT.name == 'switch_CT':
                CT.moveCt ( [0,cmds.getAttr(An_Skeleton().headJnt[1]+'.tx') ,0 ]) 
                cmds.pointConstraint ( An_Skeleton().headJnt[1], CT.name, n= 'switchConstrant' )
                
                CT.addDevideAttr ('Ik_Fk') #add atributes to switch
                for attr in ["l_armIkFkSwitch", "r_armIkFkSwitch", "l_legIkFkSwitch", "r_legIkFkSwitch"]:  
                    cmds.addAttr (CT.name, ln=attr, dv=1, min=0, max=1, keyable=True )
                CT.addDevideAttr ('visCtrls')   
                for attr in ["l_armCtrls", "r_armCtrls", "l_legCtrls", "r_legCtrls", "bodyCtrls", "addCtrls", "fingersCtrls", 'faceTable', 'upCloth', 'loCloth', 'proxyBody', 'proxyHead', 'accessories' ]: 
                    cmds.addAttr (CT.name, ln=attr, dv=1, min=0, max=1, keyable=True, attributeType='long' )
                    cmds.setAttr ( CT.name+'.'+attr, keyable=False,  channelBox=True )
                CT.addDevideAttr ('otherSettings') 
            CT.hideAttr(ctData[CT.name][2]) 
        
        cmds.group (jnts, n='skeleton_grp') 
        
        for child, par in ([pivotOffsetObj.name, generalObj.name],
                             [switchObj.name,  pivotOffsetObj.name],
                             [generalObj.name,  CharacterNames().rigStructure(query=True, rigFold=True)['rigBody']],
                             ['skeleton_grp', pivotOffsetObj.name ]):
            cmds.parent ( child, par)
            
        cmds.addAttr (switchObj.name, ln='renderGeometry', min=0, dv=1, max=1 , keyable=False) 
        cmds.connectAttr (switchObj.name+'.renderGeometry', normFolder+'.v')
        revers = an_connectReversAttr (switchObj.name+'.renderGeometry', midFolder+'.v')
        cmds.connectAttr (revers+".outputX", lowFolder+'.v')
        
        cmds.connectAttr (switchObj.name+'.loCloth', loClothProxyGeo_grp+'.v')
        cmds.connectAttr (switchObj.name+'.upCloth', upClothProxyGeo_grp+'.v')
        
        cmds.connectAttr (switchObj.name+'.proxyBody', sProxyBody_grp+'.v')
        cmds.connectAttr (switchObj.name+'.proxyHead', sProxyHead_grp+'.v')
        revers1 = an_connectReversAttr (switchObj.name+'.proxyBody', proxyBody_grp+'.v')
        revers2 = an_connectReversAttr (switchObj.name+'.proxyHead', proxyHead_grp+'.v')
        
        cmds.connectAttr (switchObj.name+'.accessories', accessoriesProxyGeo_grp+'.v')      
    
    elif action =='delRig': 
        for each in jnts: 
            cmds.parent (each, w=True)
        cmds.delete(CharacterNames().rigStructure( query=True,   fold=True )[0]) 

 
 
 

   
            
            
            
            
            
            
            
            