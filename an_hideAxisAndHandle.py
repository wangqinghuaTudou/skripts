import maya.cmds as cmds
 

def an_hideAxisAndHandle():
    ATTR =['displayScalePivot', 'displayRotatePivot', 'displayHandle', 'displayLocalAxis']
    cmds.select (hierarchy=True)
    sel  = cmds.ls (sl=True)
    for each in sel:
        for attr in ATTR:
            if cmds.objExists(each+"."+attr):
                cmds.setAttr(each+"."+attr, 0)
    	 
     
	 

 
 
 
