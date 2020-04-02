import maya.cmds as cmds

def geoPointIdentity(geo1, geo2):
    out = True   
    pointNum = cmds.getAttr (geo1 + ".cp", size=True ) 
    for i in [0, pointNum-1]:
        pos1 = cmds.xform( geo1+'.vtx['+str(i)+']',  q=True,  t=True, os=True ) 
        pos2 = cmds.xform( geo2+'.vtx['+str(i)+']',  q=True,  t=True, os=True ) 
        if not pos1==pos2: out=False 
    return out

def an_hierarhyUVCopy ():
    objects = cmds.ls(sl=True)
    badGeo=[]
    for seurs in objects:   
   
        copyList = cmds.ls( seurs.split('|')[-1])
        if len (copyList)>1:
            target = copyList[1] if seurs == copyList[0] else copyList[0]
            #if geoPointIdentity(seurs, target):
            pvCopyUV(seurs, target) 
            #else: badGeo.append(seurs) 
    #cmds.select( badGeo)
    
    
def findPolyCopyObj (geo, accuracy=10):  
    #geo = cmds.ls(sl=True) [0]
    pointNum = cmds.getAttr (geo + ".cp", size=True )                         
    objects =  [cmds.listRelatives(x, p=1, fullPath=1)[0] for x in  cmds.ls(typ='mesh') if x!= cmds.listRelatives(geo, s=1)[0] and cmds.getAttr (x + ".cp", size=1)==pointNum  ]   
    # bBox test
    bBox, out= [],[]
    for d in xrange(3):
        bBox.append (round(max([cmds.xform( geo+'.vtx['+str(x)+']', q=1, t=1, ws=1 )[d] for x in xrange(pointNum)]), accuracy))
        bBox.append (round(min([cmds.xform( geo+'.vtx['+str(x)+']', q=1, t=1, ws=1 )[d] for x in xrange(pointNum)]), accuracy))
    for obj in objects:
        objBox= []
        for d in xrange(3):
            objBox.append (round(max([cmds.xform( obj+'.vtx['+str(x)+']', q=1, t=1, ws=1 )[d] for x in xrange(pointNum)]), accuracy))
            objBox.append (round(min([cmds.xform( obj+'.vtx['+str(x)+']', q=1, t=1, ws=1 )[d] for x in xrange(pointNum)]), accuracy))
        if objBox==bBox: out.append(obj)
    return out

########################################################################### inorodnoe telo ####################################
import maya.api.OpenMaya as om

def pvShowOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 1)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 0)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) shown successful.')

def pvHideOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 0)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 1)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) hided successful.')

def pvDeleteOrigShapes(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified some object(s).')
        return

    deleted_shapes_counter = 0
    deletedShapes = []

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            for shp in shapes:
                isOrig = cmds.getAttr (shp + '.intermediateObject')
                if isOrig:
                    isConnected = cmds.listConnections(shp, source=True, destination=True)
                    if not isConnected:
                        try:
                            deletedShapes.append(shp)
                            cmds.delete(shp)
                            deleted_shapes_counter += 1
                        except:
                            om.MGlobal.displayInfo('Can\'t delete "Orig" shape: ' + shp)

    if deletedShapes:
        om.MGlobal.displayInfo('-------------------------------------------------------------')
        om.MGlobal.displayInfo('Deleted %s shapes.'%deleted_shapes_counter)
        om.MGlobal.displayInfo('Deleted shapes:')
        om.MGlobal.displayInfo('%s'%deletedShapes)
    else:
        om.MGlobal.displayInfo('No "Orig" shapes deleted.')

    return deletedShapes

def pvCopyUV(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified two objects.')
        return
    if len(args) != 2:
        om.MGlobal.displayInfo('Must be specified only two objects.')
        return

    sample_space = pvCopyUVInterfaceRequest()
    source = args[0]
    dest = args[1]
    pvDeleteOrigShapes(source)
    pvDeleteOrigShapes(dest)
    pvShowOrigGeo(dest)

    cmds.transferAttributes(source, dest, \
                            transferPositions=0, \
                            transferNormals=0, \
                            transferUVs=2, \
                            transferColors=0, \
                            sampleSpace=sample_space, \
                            sourceUvSpace='map1', \
                            targetUvSpace='map1', \
                            searchMethod=3, \
                            flipUVs=0,
                            colorBorders=1)

    cmds.delete(dest, constructionHistory=True)
    pvHideOrigGeo(dest)
    cmds.select(dest, replace=True)
    om.MGlobal.displayInfo('Mapping replaced successfuly.')

















