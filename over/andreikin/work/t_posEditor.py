
import maya.cmds as cmds

from an_Procedures.utilities import * 
from an_Procedures.dynamics import *

"""
    t_posEditor

-Поставить в т позу + время постановок
-Создать т позу
-Распечатать список т поз
-удалить т позу из списка
    
"""

PFX='an_tpos'
T_FILE = 'D:/work/Project/tChar.dat'
 
def t_posEditor():
    lay = an_turnBasedUi('', title ='T-pos editor',  
                                stepsLabel =['Time setting', 'Presets editor',],
                                stepNum=False)
    
    cmds.rowColumnLayout (nc=3, cw=[(1, 210), (2, 105), (3, 105)], cs=[(2,2),(3,2)], rs=[(2,2),(3,2)], p=lay[0])
    cmds.button(l='Set T-pos', c='keyCtTest(cmds.ls ("*_CT"))')
    cmds.textField(PFX+'f1', text='-20')
    cmds.textField(PFX+'f2', text='-10')
    
    cmds.rowColumnLayout (nc=3, cw=[(1, 140), (2, 140), (3, 140)], cs=[(2,2),(3,2)], rs=[(2,2),(3,2)], p=lay[1])
    cmds.button(l='Make preset', c='keyCtTest(cmds.ls ("*_CT"))')    
    cmds.button(l='Delete preset', c='keyCtTest(cmds.ls ("*_CT"))')  
    cmds.button(l='Print presets', c='keyCtTest(cmds.ls ("*_CT"))')  
t_posEditor()

def savePreset( ):  #сохраняет обьекты стоящий в т позе в набор 
    geometrys =   [x.split(':')[-1] for x  in cmds.ls(sl=True)]
    selLen = len(cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True ).split('.m')[0])+3
    ref = cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True )[:selLen]  
    name= os.path.basename(ref).split(".")[0]

    data ={} 
    if not os.path.exists(T_FILE): 
        r = open(T_FILE, 'r')
        data = cPickle.load(r)
        r.close()
    
    data[ref]={'name':name,  'tObjects':geometrys }
    
    f = open(T_FILE, 'w')
    cPickle.dump(data , f )
    f.close()



def newFile():
    global FILE, GLOB_DIC
    FILE = cmds.fileDialog2(fileFilter='*.dat', fileMode=0, caption="Save position" )[0]
    GLOB_DIC = {}
    f = open(T_FILE, 'w')
    cPickle.dump(TPOS_DIC , f )
    f.close()
    cmds.textFieldButtonGrp(SFX+"pathF", e=True, text=FILE)    
        
    



