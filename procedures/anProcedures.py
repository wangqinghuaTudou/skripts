
# 8. 01 2020  edit an_unicName
# 18 12 2019 add  getRivets()
# 5  12 2019  add aimConstraintUp ( )
# 2  12 2019  add an_isObjEqual() 
# 25 11 2019  add an_geoNormalSmooth
# 27 09 2019  add an_isPointPosEqual


import maya.mel as mm
import maya.cmds as cmds
from CharacterNames import CharacterNames as chn
#from An_Controllers import An_Controllers as ctrl
from an_classControllers import AnControllers as ctrl 
import math

""" 

anProcedures

an_childCapture()          -  returns a list  between two specified objects (list), or a list of child objects if  one object (string) specified in the input.
an_helpLine()              -  templated line for polyvector CT
an_distans ()              -  It creates a group of calculates the distance or return distans  between objects
an_jntOnCurv()             -  system for creating a chain of bones to the selected curve
an_delSys()

   -connections-
an_connectRigVis()         -  criete attr 'rigVis' , and connect all obj.v in objList
an_connectReversAttr()     -  connect Attributes via revers node
an_connectByMultiplier ()  - connect Attributes via multiplier node
an_connectAttrToAttrList(obgAttr, inAttrs)   - connectAttrToAttrList('general_CT.s', 's')
an_madeInfoConnection ()   - add connection to get list controllers or joints list

an_fkRig()                  - fk joint chain rig
an_mixViaConstraint ()      - creates a mixing position of specified objects
an_convertPointsNames()     - convert   "pointShape.vtx[0:3]"    to     [pointShape.vtx[0], pointShape.vtx[1],  pointShape.vtx[2], pointShape.vtx[3]] 
an_saveLoadData():          - save and load data to/from object and file 
an_makeDynamicsCurve ()     - make dinamics curve
an_unicName ( num=False)    - return unik name
an_turnBasedUi()            - steb by step uneversal UI
an_TFBGcomand ():           - add sel comand to TFBG
an_rivet()                  - rivet
getRivets()                 - get list rivet
an_mixedSpace()             - creates parentConstraint and mix its wheght to each over
an_isObjInFolder()          - test  "is Obj In nesesary Folder "         
an_isPointPosEqual          - if to points position equal return true
an_isObjEqual()             - test to objects whith eny methods
an_geoNormalSmooth()   
aimConstraintUp()           - aimConstraint and up vectors

"""

#' -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kc 0 -su 0 -du 3 -sv 0 -dv 3 -tol 0.01 -fr 0  -dir 0'.replace(  ' ', '=').replace(  '=-', ', ') # convert mel flags to python

def an_childCapture(objects):   
    currentJnt = objects[0] if  type(objects) == list else objects
    out=[currentJnt,]
    while cmds.listRelatives (currentJnt, children=True ):
        currentJnt = cmds.listRelatives (currentJnt, children=True)[0]
        out.append(currentJnt)
        if  type(objects) == list and objects[1] == currentJnt: return out
    return out

def an_helpLine(chainObj, name="line01_crv"):  # templated line for polyvector CT
    name=chn(chn(name).fixNonUniqueName()).divideName()  
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
        prefix  = chn(start).divideName()[0]+chn(start).divideName()[1]
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

def an_jntOnCurv(curveName, jntNum = 10, stretchable=True, pfx=''):
    pfx = curveName+'ChSys' if not pfx else pfx
    cmds.select (cl=True,  sym =True)
    if stretchable: #If the joints should be stretched.
        curvLength  = cmds.arclen(curveName, constructionHistory = stretchable )
        if not cmds.objExists(curveName+'.scaleCompensator'): cmds.addAttr (curveName, ln='scaleCompensator', k=True, dv=1)

        jntPosMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'jPosMDV',  asUtility=True)
        cmds.connectAttr (curvLength+'.arcLength',  jntPosMDVnod+'.input1X')
        cmds.setAttr (jntPosMDVnod+".input2X", jntNum)
        cmds.setAttr (jntPosMDVnod+".operation", 2)

        scaleMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'scaleMDV',  asUtility=True)
        cmds.connectAttr (jntPosMDVnod+'.outputX',  scaleMDVnod+'.input1X')
        cmds.connectAttr (curveName+'.scaleCompensator',  scaleMDVnod+'.input2X')
        cmds.setAttr (scaleMDVnod+".operation", 2)
    jointName = range(jntNum+1)
    for index, string in enumerate(range(jntNum+1)):
    		 jointName[index]= cmds.joint (r=True , n=pfx+str(index)+'_jnt', p= [cmds.arclen(curveName)/jntNum, 0, 0])
    		 if stretchable: cmds.connectAttr (scaleMDVnod+'.outputX',  jointName[index]+'.tx')
    ikHandl = cmds.ikHandle  (n=pfx+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=jointName[0], ee= jointName[-1], c=curveName)
    cmds.parent (jointName[0], curveName)
    if stretchable: an_delSys(ikHandl[0], objList =[jointName[0], jntPosMDVnod, scaleMDVnod, curvLength])
    else: an_delSys(ikHandl[0], objList =[jointName[0], ])
    return jointName, ikHandl

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
        
def an_connectRigVis (ctrlObject, objList):
    if not cmds.objExists(ctrlObject+'.rigVis'):  cmds.addAttr (ctrlObject, ln="rigVis", at="enum", en="off:on", keyable=True)       #  cmds.addAttr  (info['grp'][0],  ln='rigVis',  keyable=True, dv=0, min=0, max=5, at="enum", en="off:on")                           #if attr Exists - create it
    for each in objList: 
    
	    if not cmds.connectionInfo (each+".v", id=True) and not cmds.objExists(each+'.rigVis'):   
	        cmds.connectAttr ( ctrlObject+'.rigVis',  each+".v") 
	    if cmds.objExists(each+'.rigVis'):  
	        cmds.connectAttr ( ctrlObject+'.rigVis',  each+'.rigVis') 

  
def an_connectReversAttr (input, output):
    prefix = chn(input.split('.')[0]).divideName()[0]+chn(input.split('.')[0]).divideName()[1]  
    revers =cmds.createNode ('reverse',  n = prefix+'Revers')
    cmds.connectAttr(input , revers+".inputX")
    cmds.connectAttr(  revers+".outputX", output)
    return revers
    
def an_connectByMultiplier (inputAttr, outputAttr, val ):
        unConvers = cmds.createNode ('unitConversion')
        cmds.setAttr (unConvers+".conversionFactor", val)
        cmds.connectAttr( inputAttr , unConvers+'.input')
        cmds.connectAttr( unConvers+'.output', outputAttr)
        return unConvers   
        
def an_connectAttrToAttrList(obgAttr, inAttrs): #  connectAttrToAttrList('general_CT.s', 's')
    sl = cmds.ls(sl=True)
    for each in sl:
        cmds.connectAttr(obgAttr, each +'.'+inAttrs)

def an_madeInfoConnection (storObject, dict): #add connection to get list controllers or joints list
    if cmds.objExists(storObject+'.'+dict.keys()[0]): cmds.deleteAttr( storObject+'.'+dict.keys()[0]) #if attr Exists - create it
    cmds.addAttr (storObject, ln=dict.keys()[0], at="message", multi=True, keyable=False )
    for i, ct in enumerate(dict[dict.keys()[0]]):
        cmds.connectAttr (ct+'.message',  storObject+'.'+ dict.keys()[0]+'['+str( i )+']')    


def an_fkRig( jnts, pfx='', ctSize=0.5):
    if not pfx: pfx = ''.join(chn(jnts[0]).divideName()[:2]) # if not  defined pfx define it from jnt name
    def addLength (ct, grp  ):                            #proc for add  length setup  
        cmds.addAttr (ct, longName='length', dv=1,  keyable=True) 
        MtDv =cmds.createNode ( 'multiplyDivide' ) 
        cmds.connectAttr (ct+".length", MtDv+".input1X") 
        cmds.setAttr (MtDv+".input2X",  cmds.getAttr (grp+".tx"))
        cmds.connectAttr (MtDv+".outputX", grp+".tx")
        return MtDv
    ctObjects = []
    for i in xrange(len(jnts)-1): 
        ctObj=ctrl(pfx+str(i)+chn('').suffixes[0]) #define ct name
        ctObjects.append(ctObj)
        ctObj.makeController( 'fk', ctSize) 
        #ctObj.gropeCT()
        ctObj.rotateCt([0, -90, 90])           
        ctObj.placeCT ( jnts[i]  , 'parent')   # place CT
        cmds.parentConstraint( ctObj.name, jnts[i]) 
        ctObj.hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        if i: cmds.parent(ctObj.oriGrp, ctObjects[i-1].name)
        if i: addLength (ctObjects[i-1].name, ctObjects[i].oriGrp )
    MtDv = addLength (ctObjects[-1].name, jnts[-1])
    for i in xrange(len(jnts)-1):  cmds.connectAttr (ctObjects[i].name+".length", jnts[i]+".sx") 
    rigGrp = cmds.group (ctObjects[0].oriGrp, n=pfx+'FkRig_grp')
    an_delSys(rigGrp, objList =[MtDv, ctObjects[0].oriGrp])        
    return ctObjects, rigGrp


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

def an_convertPointsNames(pList): #convert   "pointShape.vtx[0:3]"    to     [pointShape.vtx[0], pointShape.vtx[1],  pointShape.vtx[2], pointShape.vtx[3]] 
    output=[]
    for pName in pList:
        iRenge = pName.split(']')[0].split('[')[1] 
        if ':' in iRenge:
            for i in range ( int(iRenge.split(':')[0]), int(iRenge.split(':')[1])+1): output.append(pList[0].split('[')[0]+'['+str(i)+']' )
        else:  output.append(pName)     
    return output
    
def an_saveLoadData(data=[], obgect='', delAttr = False, vDir=''): #save and load data to/from object and file 
    import cPickle
    import maya.mel as mm
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

def an_makeDynamicsCurve (vCurve): 
    cmds.select (vCurve)
    mm.eval("makeCurvesDynamicHairs 0 0 0;")
    crvShape= cmds.listRelatives (vCurve, s=True)[0]
    folicle = cmds.listConnections (crvShape+".local") [0]
    folShape = cmds.listRelatives (folicle, s=True)[0]
    dynCurveShape = cmds.connectionInfo (folShape+".outCurve", destinationFromSource=True)[0].split('.')[0]   
    dynCurve = cmds.listRelatives (dynCurveShape, p=True)[0]		 
    hairSysShape = cmds.connectionInfo (folShape+".outHair", destinationFromSource=True)[0].split('.')[0] 
    hairSys = cmds.listRelatives (hairSysShape, p=True)[0] 
    return dynCurve, folicle, hairSysShape


def an_unicName (name, sfx , num=False, char=False):  #return unik name
    if char:
        print 42424
        for i in range(65, 91):
            if not cmds.objExists(name+chr(i)+sfx): return name+chr(i)+sfx, chr(i)
    elif num:
        for i in xrange(1,100): 
                num = '0'+ str(i) if len(str(i))==1 else str(i)
                if not cmds.objExists(name+num+sfx): return name+num+sfx, num
    else:# ecli nomer ne nuzhen
        if not cmds.objExists(name+sfx): #esli imya v scene otcutstvuet, to mozhno ispol`zovat` ishodnoe
            return name+sfx, '00'
        else: return an_unicName ( name, sfx , num=True)
    


def an_turnBasedUi(sfx, title ='',  stepsLabel =[]):
    win = sfx+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t=title, width=420,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout (sfx+"ColumnL", adjustableColumn=True)
    out =[]    
    for idx, step in enumerate(stepsLabel):
        cmds.frameLayout (sfx+"FL"+str(idx+1), label="Step "+str(idx+1)+': '+step  , cll=0, w=424, bgc=[0,0,0], borderVisible=True)
        out.append(sfx+"FL"+str(idx+1))
        cmds.setParent (sfx+"ColumnL")  
    cmds.showWindow (win)
    return out

def an_TFBGcomand (TFBG):  return  "cmds.textFieldButtonGrp ('"+TFBG+"', e=True, tx= cmds.ls (sl=True)[0]);"

"""
def an_rivet(nameObject, e1, e2):  # e1, e2 - nambers of edges
    '''
    list = cmds.filterExpand (sm= 32)
    nameObject =  list[0].split('.')[0]
    e1 =  list[0].split('[')[1].split(']')[0]
    e2 =  list[1].split('[')[1].split(']')[0]
    an_rivet(nameObject, e1, e2)
    '''
    
    nameCFME1 = cmds.createNode ( 'curveFromMeshEdge', n= "rivetCurveFromMeshEdge1")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e1))
    
    nameCFME2 = cmds.createNode ( 'curveFromMeshEdge', n="rivetCurveFromMeshEdge2")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e2))
    
    nameLoft = cmds.createNode ( 'loft' , n="rivetLoft1")
    cmds.setAttr (  ".ic", s=2)
    cmds.setAttr ( ".u", True)
    cmds.setAttr ( ".rsn", True)
    
    namePOSI = cmds.createNode ( 'pointOnSurfaceInfo' , n= "rivetPointOnSurfaceInfo1")
    cmds.setAttr ( ".turnOnPercentage", 1)
    cmds.setAttr ( ".parameterU", 0.5)
    cmds.setAttr ( ".parameterV", 0.5)
    
    cmds.connectAttr ( nameLoft + ".os",  namePOSI + ".is", f=True)
    cmds.connectAttr ( nameCFME1 + ".oc",  nameLoft + ".ic[0]")
    cmds.connectAttr ( nameCFME2 + ".oc",  nameLoft + ".ic[1]")
    cmds.connectAttr ( nameObject + ".w",  nameCFME1 + ".im")
    cmds.connectAttr ( nameObject + ".w",  nameCFME2 + ".im")
    
    nameLocator = cmds.createNode ( 'transform' , n = an_unicName ('rivet','' )[0]  )
    cmds.createNode ( 'locator' , n= nameLocator + "Shape", p=nameLocator)
    
    nameAC = cmds.createNode ( 'aimConstraint', p= nameLocator , n=  nameLocator + "_rivetAimConstraint1")
    cmds.setAttr ( ".tg[0].tw", 1)
    cmds.setAttr ( ".a" , 0, 1, 0)
    cmds.setAttr ( ".u", 0, 0, 1)
    
    for attr in [".v", ".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]: cmds.setAttr ( attr, k=False)
    cmds.connectAttr ( namePOSI + ".position",   nameLocator + ".translate")
    cmds.connectAttr ( namePOSI + ".n",   nameAC + ".tg[0].tt")
    cmds.connectAttr ( namePOSI + ".tv",   nameAC + ".wu")
    for d in ('x', 'y', 'z'): cmds.connectAttr ( nameAC + ".cr"+d,   nameLocator + ".r"+d)
    return nameLocator
    
    
def getRivets():
    geo =  cmds.listRelatives( cmds.ls(sl=True)[0], s=True)[0]
    nods = [ x for x in cmds.listConnections(geo) if cmds.nodeType(x)=='curveFromMeshEdge']
    for tp in ( 'loft', 'pointOnSurfaceInfo', 'transform'):
        tmp =[]
        for y in nods: tmp.append( [ x for x in cmds.listConnections(y) if cmds.nodeType(x)== tp] [0]    )
        nods= list(set(tmp)) 
    return nods
"""    

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

def an_geoNormalSmooth(geo):
    if not geo: geo = ls(sl=True)[0]
    cmds.polyNormalPerVertex (geo, ufn=True)
    polySoftEdge (geo, a=180, ch=0)
    cmds.bakePartialHistory( geo,prePostDeformers=True )  

#target, obj, upObject = cmds.ls(sl=True)
def aimConstraintUp(target, obj, upObject):
    return cmds.aimConstraint( target, obj, mo=False, u=[0, 0, 1],  wuo = upObject, worldUpType='object')
    
    























