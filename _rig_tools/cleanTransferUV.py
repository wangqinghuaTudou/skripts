import maya.cmds as cmds

def cleanTransferUV():
    if not len(cmds.ls (l=True,  sl=True))==2: 
        cmds.error( "hey. 2 objects. Select source then target" )
    source, target = cmds.ls (  sl=True) #l=True,
                #try to do it by just reading SECOND shape node (first is shape, then ORIG, then other shape)

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