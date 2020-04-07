import maya.cmds as cmds
from  an_Procedures.rivet import rivet
from an_Procedures.utilities import an_convertSliceToList
 
 
def getNum(comp): 
    return int(comp.split('[')[1][:-1])

def an_rivet( ):

    seurface =  cmds.ls(sl=1)[0].split('.')[0]
    sel = cmds.filterExpand (sm= 32)  #get edge
    
    if sel:  
        print seurface, getNum(sel[0]), getNum(sel[1])
        rivet(seurface, [getNum(sel[0]), getNum(sel[1])] )
    else: 
        sel = cmds.filterExpand (sm= 34)  #get face
        edges = an_convertSliceToList(cmds.polyListComponentConversion( sel, te=True )) #get edges
        data = dict()
        for edg in edges:
            pt = an_convertSliceToList(cmds.polyListComponentConversion( edg, tv=True ))
            data[edg] = [ getNum(x) for x in pt ]
        egesCapl = [x for x in edges[1:] if (data[edges[0]][0] not in data[x]) and  (data[edges[0]][1] not in data[x])]+[edges[0]]
        print seurface, getNum(egesCapl[0]), getNum(egesCapl[1])
        rivet(seurface, edges=[getNum(egesCapl[0]), getNum(egesCapl[1])])
 