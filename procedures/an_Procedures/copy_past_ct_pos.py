
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name:
    copy_past_ct_pos()

Creation Date:
    November 3, 2020

Authors:
    Belyaev Andrey
    andreikin@mail.ru
    
Description:
    Copying or pasting attributes values from scene to scene

Comments or suggestions? E-mail me!!!
Good luck!!!

*************************************************************************************************************************
 version History
*************************************************************************************************************************
	v2.0
-working with chars and props
-refactoring
*************************************************************************************************************************
 Modify at your own risk
"""

import maya.cmds as cmds
import maya.mel as mm
import cPickle, re


def an_chek_attr( obj, attr):
    attr_obg_existence = cmds.objExists(obj+'.'+attr)                                              # test attr and obg existence	
    is_attr_unlocked  =  attr in cmds.listAttr(obj, unlocked=True, visible=True, k=True ) # test is attr unlocked 	  
    is_not_connected  = not cmds.connectionInfo(obj+'.'+attr, isDestination=True)                  # test is attr connected 	
    is_not_connected  = True if cmds.keyframe( obj+'.'+attr, query=True, keyframeCount=True ) else is_not_connected # test is attr connected to anim curves
    return all([attr_obg_existence, is_attr_unlocked, is_not_connected])

def an_kill_ns(seursNane): 
    out = seursNane.split(":")[-1]  if ":" in seursNane else v_seursNane
    return out

def an_save_load_data(data = ""):
    file_name = mm.eval("getenv (\"HOME\")")+'/tmp.dat'
    if not data: #if not data in function load mode
        with open(file_name, 'r' ) as f: return cPickle.load(f)
    else: 
        with open(file_name, 'w' ) as f: return cPickle.dump(data, f)

def an_get_ct(ctrl=''):
    pfx = cmds.ls(sl=True)[0].split(':')[0] if not ctrl else ctrl.split(':')[0]
    ctrls = [x for x in cmds.ls() if re.findall('^'+pfx+':\S+_CT$', x) and cmds.nodeType(x)== 'transform'] # sort controls by name and type
    return ctrls   

def an_copyPos():
    result = []
    for obj in an_get_ct():
        vAttr = cmds.listAttr(obj, k=True, u=True, s=True, v=True)         
        try:
            vData = []
            for each in vAttr:     
                vData.append(cmds.getAttr(obj+"."+each))
            result.append( [an_kill_ns(obj), vAttr, vData] )
        except TypeError:  pass
    an_save_load_data(result)# save

def an_pastePos(toSel=False): # if  toSel==True copy values only to selected objects
    objcts = cmds.ls(sl=True) 
    pfx = re.findall('[^\s]+:', objcts[0])[0] 
    data = an_save_load_data() 
    data = [x for x in data if pfx+x[0] in objcts ] if toSel else data
    for each  in data:
            for attr, val in zip(each[1], each[2]):
                if an_chek_attr(pfx+each[0], attr) and cmds.nodeType(pfx+each[0]) == "transform":
                    cmds.setAttr (pfx+each[0]+"."+attr, val)


#an_pastePos(toSel=True) 

#an_pastePos(toSel=False)
 
#an_copyPos()
