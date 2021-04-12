import re
import maya.cmds as cmds

def set_t_pos(reference , ct_pattern="[\w:_]+_CT$"):
    
    """
    The function puts character in a t pose.  
    """
    
    ignor_list = "general_CT", "pivotOffset_CT", "switch_CT"
    space_attribute_list = ["space", "rSpace"]
    
    ct_pattern = re.compile(ct_pattern)
    node_list = [x for x in cmds.referenceQuery(reference, nodes=True) if ct_pattern.search(x)]
    
    # remove ignor controllers
    node_list = [ct for ct in node_list if not ct.split(":")[-1] in ignor_list]
    
    # set in t-pos
    space_carrent_atributes = {}
    for ctrl in node_list: 
        attributes = [x.split("_default")[0] for x in cmds.listAttr(ctrl) if  "_default" in x]
        
        for attr in attributes:
            if attr in space_attribute_list:
                val = cmds.getAttr(ctrl+"."+attr)
                space_carrent_atributes[ctrl+"."+attr]=val
               
            default_val = cmds.getAttr(ctrl+"."+attr+"_default")
            cmds.setAttr(ctrl+"."+attr, default_val)
    
    # create locators in control position
    locatots = []
    for ctrl in node_list: 
        pos_loc = cmds.spaceLocator(name = ctrl+"_loc")[0]
        cmds.matchTransform (pos_loc, ctrl)
        try:
            cmds.pointConstraint(pos_loc, ctrl, name = ctrl+"_const")
        except:
            pass
        try:
            cmds.orientConstraint(pos_loc, ctrl, name = ctrl+"_const")
        except:
            pass   
        locatots.append(pos_loc)
    
    # turn spaces atributes in nessesary values
    for attr in space_carrent_atributes:
        cmds.setAttr(attr, space_carrent_atributes[attr])
    
    # get final atributes values
    final_values = []
    for ctrl in node_list: 
        attributes = [x.split("_default")[0] for x in cmds.listAttr(ctrl) if  "_default" in x]
        for attr in attributes:
            val = cmds.getAttr(ctrl+"."+attr)
            final_values.append([ctrl, attr, val])
    
    cmds.delete(locatots)
    
    # set final atributes values
    for ctrl, attr, val in final_values:
        cmds.setAttr(ctrl+"."+attr, val)
        cmds.setKeyframe(ctrl, attribute=attr, value=val )



def t_pos():
    reference=cmds.referenceQuery (cmds.ls(sl=True)[0], referenceNode=True)
    set_t_pos(reference , ct_pattern="[\w:_]+_CT$")


 




 