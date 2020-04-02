import maya.cmds as cmds

def cleanTransferUV(source, target):
                # to skin geo
    if len (cmds.listRelatives (target,  s=True))>1:    
        targetOrig = cmds.listRelatives (target,  s=True)[1] #f=True,
                         #dummy check that this is orig object (is it intermediate? does it contain "orig"?)
        if cmds.getAttr (targetOrig+".intermediateObject") and  ("Orig" in targetOrig):
                        #turn off intermediate object setting on orig
            cmds.setAttr (targetOrig + ".intermediateObject", 0)
                        #transfer uv's to "orig" shape of target
            cmds.transferAttributes (source, targetOrig, pos=0, nml=0, uvs=2, col=2, spa=4, suv="map1", tuv="map1", sm=3, fuv=0, clb=1)
            cmds.select (cl=True)
                        #delete history on target orig then turn back on intermediate object attr
            cmds.delete (targetOrig, ch=True )
            cmds.setAttr (targetOrig + ".intermediateObject", 1)
        else :
            cmds.error( "couldn't find the orig shape of the target object. make sure it's a bound/deformed thing" )
    else:   # to not skin geo
        cmds.transferAttributes (source, target, pos=0, nml=0, uvs=2, col=2, spa=4, suv="map1", tuv="map1", sm=3, fuv=0, clb=1)
        cmds.delete (target, ch=True )


def posTest(objA, objB, bBox=True):
    out = False
    if bBox:
        objAShape = cmds.listRelatives(objA, s=True)[0] 
        objBShape = cmds.listRelatives(objB, s=True)[0] 
        objAbBox =  cmds.getAttr ( objAShape+'.boundingBoxMin')[0]+cmds.getAttr ( objAShape+'.boundingBoxMax')[0] 
        objBbBox =  cmds.getAttr ( objBShape+'.boundingBoxMin')[0]+cmds.getAttr ( objBShape+'.boundingBoxMax')[0] 
        if objAbBox == objBbBox: out = True 
    return out



def an_recombAndTransferUV(): # select seurc uv object 
    
    seurs, target = cmds.ls(sl=True)
    
    seursDup = cmds.duplicate (seurs)[0]
    targetDup = cmds.duplicate (target)[0]
    
    seursDupShape = cmds.listRelatives(seursDup, s=True)[0]
    targetDupShape = cmds.listRelatives(targetDup, s=True)[0]
    
    seursDupList = cmds.polySeparate  (seursDupShape, ch=0)
    targetDupList = cmds.polySeparate  (targetDupShape, ch=0)
    
    for geo in targetDupList: 
        for sGeo in seursDupList:
            if posTest(geo, sGeo):
                cmds.parent (sGeo, w=True)
                cmds.parent (sGeo, seursDup)
        
    sortDupList = cmds.listRelatives(seursDup, c=True) 
    cmds.delete(targetDup)
    cmds.select(sortDupList)
    newGeo = cmds.polyUnite (ch=0)[0]
    
    cleanTransferUV( newGeo, target) 
         
    cmds.delete(newGeo)  
        
 

