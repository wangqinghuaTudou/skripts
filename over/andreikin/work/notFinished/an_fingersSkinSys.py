import maya.cmds as cmds 
from  anProcedures import *
from CharacterNames import CharacterNames as chn



def an_fingersSkinSys():   
    fingersList = ['thumb', 'index', 'ring', 'middle',  'pinky']
    limb = cmds.ls(sl=True)[0]
    info = getInfo(limb, fingersList)
    
def getInfo(limb, fingersList): 
    info = {'side':chn(limb).divideName()[0], }   #get side     
    info['fingersJnt'] = [an_childCapture(info ['side']+x+'1_bind') for x in fingersList if cmds.objExists(info ['side']+x+'1_bind') ]
    return info
