import maya.cmds as cmds
import maya.mel as mm
from an_classNames import AnNames 
from an_classControllers import AnControllers as ctrl 
import math, cPickle
 

'''
        utilities
     
    - an_convertSliceToList()   
    - an_childCapture()          -  returns a list  between two specified objects (list), or a list of child objects if  one object (string) specified in the input.
    - an_helpLine()              -  templated line for polyvector CT
    - an_distans ()              -  It creates a group of calculates the distance or return distans  between objects
    - an_delSys()
    - an_mixViaConstraint ()      - creates a mixing position of specified objects
    - an_saveLoadData():          - save and load data to/from object and file 
    - an_turnBasedUi()            - steb by step uneversal UI
    - an_mixedSpace()             - creates parentConstraint and mix its wheght to each over
    - an_isObjInFolder()          - test  "is Obj In nesesary Folder "         
    - an_isPointPosEqual          - if to points position equal return true
    - an_isObjEqual()             - test to objects whith eny methods
    - an_geoNormalSmooth()   
    - connectGeoToGeo()           - connect meshes whith many method
    - an_killReferenceNamespace ()
'''


def an_convertSliceToList(pList): #convert   "pShape.vtx[0:3]"       to     [pShape.vtx[0], pShape.vtx[1],  pShape.vtx[2], pShape.vtx[3]] 
    output=[]
    for pName in pList: 
        if '.'  in pName:
            iRenge = pName.split(']')[0].split('[')[1] 
            if ':' in iRenge:
                for i in range ( int(iRenge.split(':')[0]), int(iRenge.split(':')[1])+1): 
                    output.append(pName.split('[')[0]+'['+str(i)+']' )
            else:  output.append(pName)
        else:  output.append(pName)    
    return output

def an_delSys(ctrlObject, objList =[]):
    if objList: # If the list is not empty, the deleting system will create
        delObgList =[]
        if not cmds.objExists(ctrlObject+'.delList'): #if attr Exists - create it
            cmds.addAttr (ctrlObject, ln="delList", at="message", multi=True, keyable=False )
        else: delObgList = cmds.listConnections( ctrlObject+'.delList', s=True, d= False ) #else get list Connections for determin length  
        for index, obj in enumerate(objList):
            cmds.connectAttr (obj+'.message',  ctrlObject+'.delList['+str(index+len(delObgList))+']')
    else:  #If the list is empty the deleting system will started
        if cmds.objExists(ctrlObject+'.delList'): # if del obj has del attr list
            delObg = cmds.listConnections( ctrlObject+'.delList', s=True, d= False ) #get del attr list
            if ctrlObject in delObg: delObg.remove(ctrlObject)
            for obg in delObg:
                if cmds.objExists(obg+'.delList'): an_delSys(obg) #if del obj has del attr list start recursy
                else:
                    if cmds.objExists(obg): cmds.delete (obg) # if obj is cliar del it
            if cmds.objExists(ctrlObject): cmds.delete (ctrlObject)             
        else: 
            if cmds.objExists(ctrlObject): cmds.delete (ctrlObject)


""" 



"""

#' -ch 1 -rpo 1 -rt 0 -end 1 -kr 0  -dir 0'.replace(  ' ', '=').replace(  '=-', ', ') # convert mel flags to python

def an_childCapture(objects):   
    currentJnt = objects[0] if  type(objects) == list else objects
    out=[currentJnt,]
    while cmds.listRelatives (currentJnt, children=True ):
        currentJnt = cmds.listRelatives (currentJnt, children=True)[0]
        out.append(currentJnt)
        if  type(objects) == list and objects[1] == currentJnt: return out
    return out

def an_helpLine(chainObj, name="line01_crv"):  # templated line for polyvector CT
    name=AnNames(AnNames(name).fixNonUniqueName()).divideName()  
    v_curve = cmds.curve(n =name[0]+name[1]+"_crv",  p=[(0,0,x+1) for x in xrange(0, len(chainObj))], d=1 )
    cmds.setAttr (v_curve+".inheritsTransform", 0)
    v_grp = cmds.group( v_curve,  n=name[0]+name[1]+"_grp" )
    cmds.setAttr (v_curve +".overrideEnabled", 1)
    cmds.setAttr (v_curve +".overrideDisplayType", 2 )
    for index, obj in enumerate(chainObj):
        v_cluster =cmds.cluster(v_curve+'.cv['+str(index)+']')[1]
        cmds.pointConstraint(obj, v_cluster)
        cmds.setAttr (v_cluster+".visibility", 0)
        cmds.parent (v_cluster, v_grp)
    return v_grp

 

def an_distans ( start, end, act=''):
    if act=='createSys':
        prefix  = AnNames(start).sfxMinus()
        distansName = cmds.group (em=True, n=prefix+"_distans#") 
        distansOfsName = cmds.group (n=prefix+"_distansAim#")   
        cmds.pointConstraint   (start, distansOfsName)
        cmds.aimConstraint    ( end, distansOfsName, aim=[1, 0, 0])
        cmds.pointConstraint   (end, distansName)
        return [distansName+".tx", distansOfsName]
    else :
        from math import  sqrt
        a = cmds.xform  (start, q=True, t=True, ws=True) if type(start)==str or type(start)==unicode else start
        b = cmds.xform  (end, q=True, t=True, ws=True)  if type(end)==str  or type(end)==unicode else end
        xy = sqrt ((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
        return  sqrt (xy*xy+(a[2]-b[2])*(a[2]-b[2])) 
 

        

def an_mixViaConstraint (objects, type='parent', mixAttr=''): # creates a mixing position of specified objects
    from  anProcedures import an_connectReversAttr  
    constraint =[]  
    if   type=='parent'  :   constraint = cmds.parentConstraint (objects)[0]
    if   type=='point'  :  constraint = cmds.pointConstraint (objects)[0]
    if   type=='orient'  :   
        constraint = cmds.orientConstraint (objects)[0]
        cmds.setAttr (constraint+'.interpType', 2)
    reversNod = an_connectReversAttr(constraint+'.'+objects[0]+'W0',  constraint+'.'+objects[1]+'W1')
    if mixAttr : cmds.connectAttr (mixAttr, constraint+'.'+objects[0]+'W0') 
    return constraint, objects[0]+'W0', reversNod


def an_saveLoadData(data=[], obgect='', delAttr = False, vDir=''): #save and load data to/from object and file 

    if not vDir: vDir = mm.eval("getenv (\"HOME\")")
    if data:             # if data exist - save mod 
            if obgect:                            # if  obgect exist - save on it
                    if not  cmds.objExists (obgect + '.data'):
                        cmds.addAttr   (obgect, ln="data", dt="string", keyable = False)  
                    cmds.setAttr ( obgect+".data", cPickle.dumps(data) , type="string" )  
            else :
                    vFileName = cmds.fileDialog2(fileFilter='*.dat', fileMode=0, caption="Save position", dir=vDir ) 
                    f = open(vFileName[0], 'w')
                    cPickle.dump(data , f )
                    f.close()

    else:            # if data absent - load mod 
            if obgect:                            # if  obgect exist - load from it
                    vString = cmds.getAttr  (obgect + '.data')
                    if delAttr: cmds.deleteAttr(obgect + '.data')
                    return cPickle.loads(str(vString))
            else :                                # if  obgect not exist - load from file
                    #vDir = mm.eval("getenv (\"HOME\")")
                    vFileName = cmds.fileDialog2( fileMode=1, caption="Load position", dir=vDir )
                    r = open(vFileName[0], 'r')
                    data = cPickle.load(r)
                    r.close()
                    return data



def an_turnBasedUi(sfx, title ='',  stepsLabel =[], stepNum=True):
    win = sfx+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t=title, width=420,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout (sfx+"ColumnL", adjustableColumn=True)
    out =[]    
    for idx, step in enumerate(stepsLabel):
        leble = "Step "+str(idx+1)+': '+step   if stepNum else step
        cmds.frameLayout (sfx+"FL"+str(idx+1), label=leble  , cll=0, w=424, bgc=[0,0,0], borderVisible=True)
        out.append(sfx+"FL"+str(idx+1))
        cmds.setParent (sfx+"ColumnL")  
    cmds.showWindow (win)
    return out


def an_mixedSpace(transforms, obj, type='parent', mo=True):
    vPMA, constr='', ''   
    for i in range(len(transforms)):
        if type=='orient': constr = cmds.orientConstraint (transforms[i], obj, mo=mo) 
        if type=='point' : constr = cmds.pointConstraint (transforms[i], obj, mo=mo)  
        if type=='parent': constr = cmds.parentConstraint (transforms[i], obj, mo=mo) 
        if i==0: 
            vPMA = cmds.createNode ('plusMinusAverage',  n =obj  +'PMA2') 
            cmds.setAttr (  vPMA+'.operation', 2)
            cmds.setAttr (  vPMA+'.input1D[0]', 1)
            CLM = cmds.createNode ('clamp',  n =obj  +'CLM') 
            cmds.connectAttr ( vPMA +'.output1D ', CLM+'.inputR')
            cmds.setAttr (  CLM+'.maxR', 1)
            cmds.connectAttr ( CLM +'.outputR ', constr[0]+'.'+ transforms[i]+'W'+str(i) ) 
        else: 
            cmds.connectAttr ( constr[0]+'.'+ transforms[i]+'W'+str(i), vPMA+'.input1D['+str(i)+ ']'  ) 
            val=0 if not i== len(transforms)-1 else 1
            cmds.setAttr ( constr[0]+'.'+ transforms[i]+'W'+str(i), val)
    return constr
            
def an_isObjInFolder(obg, fold):
    prnt = cmds.listRelatives(obg, p=True)
    if prnt:
        if prnt[0]==fold:  return True
        else:              return an_isObjInFolder( prnt[0], fold)
    else: return False   
    
def an_isPointPosEqual(p1, p2, accuracy = 6):
    pos1 = [round(x, accuracy)for x in cmds.pointPosition( p1 )]
    pos2 = [round(x, accuracy)for x in cmds.pointPosition( p2 )]
    return pos1==pos2
    
    
def an_isObjEqual(objA, objB, bBox=False, cv=False):
    objAShape = cmds.listRelatives(objA, s=True)[0] 
    objBShape = cmds.listRelatives(objB, s=True)[0]  
    if bBox:
        objAbBox =  cmds.getAttr ( objAShape+'.boundingBoxMin')[0]+cmds.getAttr ( objAShape+'.boundingBoxMax')[0] 
        objBbBox =  cmds.getAttr ( objBShape+'.boundingBoxMin')[0]+cmds.getAttr ( objBShape+'.boundingBoxMax')[0]  
        return objAbBox == objBbBox 
    if cv:
        vPNumA = cmds.getAttr(objAShape + '.spans') + cmds.getAttr( objAShape + '.degree')
        vPNumB = cmds.getAttr(objBShape + '.spans') + cmds.getAttr( objBShape + '.degree')
        if not vPNumA == vPNumB: return False 
        else:
            for i in range(vPNumA):
                if not an_isPointPosEqual( objA+'.cv['+str(i)+']',  objB+'.cv['+str(i)+']'):
                    return False   
            return True
            
def geoNormalSmooth(geo=''):
    if not geo: geo = cmds.ls(sl=True)
    else: geo = [geo,]
    for each in geo:
        cmds.polyNormalPerVertex (each, ufn=True)
        cmds.polySoftEdge (each, a=180, ch=0)
        cmds.bakePartialHistory( each, prePostDeformers=True )  


def connectGeoToGeo(sers, dest, conType='bsh'): # 'bsh',  'mesh', 'melnitsaWrap'
    if conType=='bsh':
        bl_shape = cmds.blendShape(sers, dest, o="world" )
    elif conType=='mesh':
        cmds.connectAttr (sers +'.outMesh', dest+'.inMesh', f=True )
    elif conType=='melnitsaWrap':
        sersShape = cmds.listRelatives( sers, s=True )[0]
        cmds.select(dest)
        deform = cmds. deformer (type='melnitsaWrap')[0]
        cmds.connectAttr (sersShape+'.worldMesh[0]', deform+'.obstacleMesh') 

def an_killReferenceNamespace ():
    sel = cmds.ls(typ="reference")
    for i in sel:
        cmds.lockNode (i, l=0 )
        cmds.delete (i)
    for i in [x for x in cmds.namespaceInfo (lon=True) if x not in ["UI", "shared"] ]:
        mm.eval('namespace -mnr -rm '+i)
       


















 