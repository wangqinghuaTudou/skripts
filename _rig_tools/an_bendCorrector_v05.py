import maya.cmds as cmds
from An_Controllers import An_Controllers  as ctrl
from  anProcedures import  *
# UI
def an_bendCorrector_v05():
    win = "makeScelUI2"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Bend correction system v5.01", width=420,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout ('columnLayoutName', adjustableColumn=True)
    #step 1
    cmds.frameLayout (label="Step 1", cll=0, w=424, bgc=[0,0,0], borderVisible=True)
    cmds.columnLayout
    cmds.separator  (  style="none")
    cmds.text (l="         Creating a system for calculating the direction and degree of bend", al="left", font= "boldLabelFont")
    cmds.text (l="     - select joint, then up joint.", al="left")
    cmds.text (l="     - to delete a rig, select the group with the system and press \"Delete\"", al="left")
    cmds.text (l="     - to mirror a system, select the group with the system and press \"Delete\"", al="left")

    cmds.floatSliderGrp('ISG_gScaleCSys', label='Global scale:', field=True, min=0.1, max=10,  v=1 , cw = [(1, 124), (2, 50) ], enable= True )
    cmds.textFieldGrp ('TFBG_pfx', l='Prefix :',    cw = [(1, 124), (2, 191)]  )

    cmds.rowColumnLayout (nc=3, cw=[(1, 140), (2, 140), (3, 140)], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2)])
    cmds.button   (l="Mirror selected system",  c='an_mirrorSys()')
    cmds.button   (l="Delete correction system",c="an_delSys (cmds.ls(sl=True)[0])")
    cmds.button   (l="Add  correction system",   c="an_correctionSystem()" )
    #cmds.setParent ('..')
    cmds.text ('')
    #cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210) ], columnSpacing=[(2,2), ] )
    cmds.button   (l='Constraint system to joint',c='an_connectSys(disconnect=False)')
    cmds.button   (l='Unconstraint system',   c='an_connectSys(disconnect=True)' )

    cmds.setParent ('columnLayoutName')
    #step 2
    cmds.frameLayout (label="Step 2", cll=0, w=424, bgc=[0,0,0], borderVisible=True)
    cmds.columnLayout
    cmds.separator  (  style="none")
    cmds.text (l='         Creating a "direction" for calculating degree of bend', al="left", font= "boldLabelFont")
    cmds.text (l='     - create template, then input options and press Create "direction".', al="left")
    cmds.text (l="     - to delete a direction, select the controller and press \"Delete\"", al="left")
    cmds.text (l="     - to mirror a direction, select controller and press \"Mirror\"", al="left")

    bc = "cmds.textFieldButtonGrp ('TFBG_solver', e=True, tx=  cmds.ls (sl=True)[0]);"
    bc1 = "cmds.textFieldGrp ('TFBG_pfx', e=True, tx=  cmds.ls (sl=True)[0][:-16])"
    cmds.textFieldButtonGrp ('TFBG_solver', l='System name :',  bl="Assign",  cw = [(1, 124), (2, 191)],  bc = bc+bc1 )
    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 210) ], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2) ])
    cmds.button   (l='Delete "direction"',c='an_delSys(cmds.listRelatives (cmds.ls (sl=True)[0], p=True)[0])')
    cmds.button   (l='Create template',   c="an_addTemplateDirection()" )
    cmds.button   (l='Mirror "direction"',  c='an_mirrorDir()')
    cmds.button   (l='Create "direction"',   c="an_addDirection()" )
    cmds.setParent ('columnLayoutName')
    #step 3
    cmds.frameLayout (label="Step 3", cll=0, w=424, bgc=[0,0,0], borderVisible=True)
    cmds.columnLayout
    cmds.separator  (  style="none")
    cmds.text (l='         Add joint and directional dependence', al="left", font= "boldLabelFont")

    cmds.text (l="     - to add a joint, select direction controller and press \"Add joint\"", al="left")

    cmds.text (l="     - to mirror a joint, select root joint and press \"Mirror\"", al="left")

    cmds.radioButtonGrp ('RBG_orient', l="Parent to  :     ", nrb=2, la2=["Bendable joint","Up joint"],  sl=1 )
    cmds.rowColumnLayout (nc=2, cw=[(1, 419), (2, 210)])
    cmds.button   (l="Add joint",   c="an_addJnt()" )
    cmds.setParent ('..')

    comand = 'cmds.textFieldGrp ("TFBG_dir", e=True, tx = cmds.ls (sl=True)[0])'
    cmds.textFieldButtonGrp ('TFBG_dir', l='Controller name :',  bl="Assign",  cw = [(1, 124), (2, 191)],  bc = comand)
    cmds.rowColumnLayout (nc=3, cw=[(1, 140), (2, 140), (3, 140)], columnSpacing=[(2,2),(3,2)])
    cmds.button   (l='Mirror joint',c= 'an_mirrorJnt()')
    cmds.button   (l='Delete joint',c= 'cmds.delete(cmds.ls(sl=True))')
    cmds.button   (l="Connect to channel",   c="an_connectChannel()" )

    cmds.showWindow (win)


def an_mirrorJnt():
    sJnt = cmds.ls (sl=True)[0]
    sParent = cmds.listRelatives (sJnt, p=True)[0]
    cmds.parent (sJnt, w=True)
    mirJnt = cmds.mirrorJoint (sJnt, mirrorYZ=True,  mirrorBehavior=True, sr= ['l_', 'r_'])[0]
    cmds.parent (sJnt, sParent)
    cmds.parent (mirJnt, sParent.replace('l_', 'r_'))
    return mirJnt


def an_mirrorSys():
    def mirrorObg(obj, srs):
        cmds.select (cl=True)
        jnt = cmds.joint()
        cmds.delete (cmds.parentConstraint (srs, jnt))
        mirJnt = cmds.mirrorJoint (jnt, mirrorYZ=True,  mirrorBehavior=True)[0]
        cmds.delete (cmds.parentConstraint (mirJnt, obj), jnt, mirJnt)

    sys = cmds.ls (sl=True)[0]
    oldPfx = sys.replace ('CorectionRig_grp', '')
    pfx = oldPfx.replace ('l_', 'r_')

    locator = ctrl(pfx+'Correctiv_ctrl')
    locator.makeController( "kross", 0.5 )
    upCorJntGrp = cmds.group(em=True, n=pfx+'UpCorJnt_grp')
    bendCorJntGrp = cmds.group(locator.name, n=pfx+'BendCorJnt_grp')
    solverGrp = cmds.group(em=True, n=pfx+'Solver_grp')

    corectionRigGrp = cmds.group(upCorJntGrp, bendCorJntGrp, solverGrp, locator.name, n=pfx+'CorectionRig_grp')
    for obj in  (upCorJntGrp, bendCorJntGrp, solverGrp, locator.name):
        mirrorObg( obj, 'l_'+ obj[2:])

        parObj = cmds.parentConstraint ('l_'+ obj[2:], q=True, targetList=True)[0]
        if 'l_' == parObj[:2]:
            parObj = 'r_' + cmds.parentConstraint ('l_'+ obj[2:], q=True, targetList=True)[0][2:]
        cmds.parentConstraint (parObj, obj, mo=True)




def an_connectSys(disconnect=False):

    #sys = cmds.ls (sl=True)[0]
    for sys in cmds.ls (sl=True):

        pfx = sys[:-16]
        locator, upCorJntGrp, bendCorJntGrp, solverGrp = pfx+'Correctiv_ctrl', pfx+'UpCorJnt_grp', pfx+'BendCorJnt_grp', pfx+'Solver_grp'

        if disconnect:
            for obj in [locator, upCorJntGrp, bendCorJntGrp, solverGrp]:
                parObj =  cmds.parentConstraint ( obj, q=True, targetList=True)[0]

                pConstr = cmds.parentConstraint ( obj, q=True, n=True)

                targOfset = cmds.getAttr(pConstr +'.target[0].targetOffsetRotate')[0]
                an_saveLoadData(data=[parObj, targOfset], obgect=obj, delAttr =  False)#save and load data to/from object and file
                cmds.delete( cmds.parentConstraint ( obj, q=True, n=True))

        else:
            upJnt = an_saveLoadData(obgect=upCorJntGrp)[0]
            bendJnt = an_saveLoadData(obgect=bendCorJntGrp)[0]

            cmds.parent (locator, bendCorJntGrp)
            for obj in [ upCorJntGrp, bendCorJntGrp, solverGrp, locator]:
                if not obj==locator:
                    cmds.delete (cmds.parentConstraint (bendJnt, obj, mo=False))
                parentObj, targOfset = an_saveLoadData(obgect=obj)
                pConstr = cmds.parentConstraint (parentObj, obj, mo=True)[0]

                cmds.setAttr(pConstr +'.target[0].targetOffsetRotate', targOfset[0], targOfset[1], targOfset[2])

            cmds.parent (locator, sys)



def an_mirrorDir():

    # 1 get new names, info
    controllerOld = cmds.ls (sl=True)[0]
    oldPfx = controllerOld.split ('Dir')[0]
    pfx = oldPfx.replace ('l_', 'r_')
    oldDirName = controllerOld.replace ('_ctrl', '')+'_grp'
    locator = pfx+'Correctiv_ctrl'

    # 2  made new geo
    dirName  = cmds.group(em=True, n = oldDirName.replace ('l_', 'r_'))[:-4]

    tmp = cmds.curve(d=3, p=[[0, 0, x] for x in range(9)], n=dirName+'_ctrl'  ) #controller
    controllerName = cmds.curve(d=3, p=[[0, 0, x] for x in range(33)], n=dirName+'_ctrl'  ) #controller
    ctrl(controllerName).addShape( tmp)

    controllerName = cmds.rename (controllerName, dirName+'_ctrl')

    seursePlane = cmds.nurbsPlane (p= [0, 1, 0], ax= [0, -1, 0], w=2.5, lr=1, d=3, u=10, v=10, ch=0, n=dirName+'SeursePlane_geo')[0]
    cmds.setAttr (seursePlane+".v", 0)
    cmds.parent(seursePlane, controllerName, dirName+'_grp')
    cmds.parent(dirName+'_grp', pfx+'Solver_grp')
    for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']: cmds.setAttr (dirName+'_grp.'+attr, 0)

        # 3  mirrow shape
    ctrl(controllerOld).mirrorShape( controllerName)
    ctrl(controllerName).addColor ( switch=None, color=17)# addColor

    sourse, target = seursePlane.replace ('r_', 'l_'), seursePlane
    sourseShape = cmds.listRelatives(sourse, s=True)[0]
    targShape = cmds.listRelatives(target, s=True)[0]
    for upn in xrange(13):
        for vpn in xrange(13):
            pos =cmds.xform(sourseShape+'.cv['+str(upn)+']['+str(vpn)+']',  q=True, t=True, ws=True )
            cmds.xform(targShape+'.cv['+str(upn)+']['+str(vpn)+']', t=[pos[0]*-1, pos[1], pos[2] ], ws=True )

    # 4  connect to nodes
    cmds.connectAttr  (controllerName+".rotate",  seursePlane+".rotate")

    for attr in ( 'val',  'multiplier',  'resultVal'  ):
        cmds.addAttr  (controllerName,  ln=attr, dv=-10, keyable=True)
    ctrl(controllerName).hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])

    vPointOnSurface = cmds.createNode ("closestPointOnSurface", n=pfx+"PointOnSurface")
    cmds.connectAttr  (locator+'.translate',  vPointOnSurface+".inPosition")

    v_nurbShape = cmds.listRelatives ( seursePlane, s=True )[0]
    cmds.connectAttr  (v_nurbShape+".worldSpace[0]",  vPointOnSurface+".inputSurface")

    setRange = cmds.createNode ("setRange", n=pfx+"SetRange")
    cmds.connectAttr  (vPointOnSurface+".parameterV",  setRange+".valueX")

    cmds.setAttr (setRange+".minX", -1)
    cmds.setAttr (setRange+".maxX", 1)
    cmds.setAttr (setRange+".oldMaxX", 1)

    multiplyDivide = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide" )

    cmds.setAttr (multiplyDivide+".operation", 3)
    cmds.setAttr (multiplyDivide+".input2X", 2)
    cmds.connectAttr  (setRange+".outValueX",  multiplyDivide+".input1X")

    revers = cmds.createNode ("reverse", n=pfx+"Revers")
    cmds.connectAttr (multiplyDivide+'.outputX', revers+'.inputX')

    multiplyDivide2 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide2" )
    cmds.connectAttr ( revers+'.outputX',  multiplyDivide2+'.input1X')
    cmds.connectAttr ( vPointOnSurface+'.parameterU',  multiplyDivide2+'.input2X')
    cmds.connectAttr (  multiplyDivide2+'.outputX', controllerName+'.val')

    multiplyDivide3 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide3" )

    cmds.connectAttr ( multiplyDivide2+'.outputX',  multiplyDivide3+'.input1X')
    cmds.connectAttr ( controllerName+'.multiplier',  multiplyDivide3+'.input2X')
    cmds.connectAttr (  multiplyDivide3+'.outputX', controllerName+'.resultVal')

    an_delSys(dirName+'_grp', [vPointOnSurface, setRange, multiplyDivide, revers, multiplyDivide2, multiplyDivide3])
    cmds.select ( controllerName, r=True)
    cmds.textFieldGrp ("TFBG_dir", e=True, tx = controllerName)
    return controllerName



def an_addJnt():  #select controller

    sel = cmds.ls (sl=True)[0] if cmds.ls (sl=True) else cmds.textFieldGrp ('TFBG_dir', q=True, tx=True )
    pfx = sel[:-10] if sel else cmds.textFieldGrp ('TFBG_dir', q=True, tx=True )[:12]

    gScale = float(cmds.getAttr (pfx+"CorectionRig_grp.gScale"))


    controllerName = cmds.textFieldGrp ('TFBG_dir', q=True, tx=True  )
    solverGrp = pfx+'Solver_grp'

    cmds.select (cl=True)
    rtJnt = cmds.joint (n = an_unicName( pfx+'RtDir', '_jnt', num=True)[0], p=[0,0,0])
    jnt = cmds.joint (n = rtJnt.replace('RtDir', 'Dir'), p=[0,0,0])
    parentGrp = pfx+'UpCorJnt_grp' if cmds.radioButtonGrp ('RBG_orient', q=True, sl=True) == 2 else pfx+'BendCorJnt_grp'
    cmds.parent (rtJnt, parentGrp, relative=True)
    cmds.setAttr (jnt+".translateY", 1*gScale)
    if sel: cmds.select ( sel)

    return jnt, rtJnt

def an_connectChannel():
    jnt = cmds.ls (sl=True)[0]+'.'+cmds.channelBox  ('mainChannelBox', q = True, selectedMainAttributes = True )[0]
    controllerName = cmds.textFieldButtonGrp ('TFBG_dir', q=True, tx=True)
    cmds.connectAttr  (controllerName+".resultVal",  jnt)

def an_correctionSystem (): ###########################################
    bendJnt, upJnt = cmds.ls (sl=True)
    pfx = cmds.textFieldGrp ('TFBG_pfx', q=True, tx=True  )
    gScale = cmds.floatSliderGrp('ISG_gScaleCSys', q=True, v=True  )
    locator = ctrl(pfx+'Correctiv_ctrl')
    locator.makeController( "kross", 0.5 )
    upCorJntGrp = cmds.group(em=True, n=pfx+'UpCorJnt_grp')
    bendCorJntGrp = cmds.group(locator.name, n=pfx+'BendCorJnt_grp')
    solverGrp = cmds.group(em=True, n=pfx+'Solver_grp')

    for grp in  [upCorJntGrp, bendCorJntGrp, solverGrp]: cmds.delete (cmds.parentConstraint (bendJnt, grp, mo=False))
    cmds.setAttr (locator.name+".translateX", 1*gScale)
    corectionRigGrp = cmds.group(upCorJntGrp, bendCorJntGrp, solverGrp, locator.name, n=pfx+'CorectionRig_grp')
    cmds.xform (corectionRigGrp, os=True, piv=[0, 0, 0])
    for grp in  [upCorJntGrp, solverGrp]: cmds.parentConstraint (upJnt, grp, mo=True)
    for grp in  [locator.name, bendCorJntGrp]: cmds.parentConstraint (bendJnt, grp, mo=True)
    cmds.textFieldButtonGrp ('TFBG_solver', e=True, tx= corectionRigGrp)
    cmds.addAttr   (corectionRigGrp, ln='gScale', dv=gScale,  keyable = False)
    return corectionRigGrp



def an_addTemplateDirection ():
    pfx = cmds.textFieldGrp ('TFBG_pfx', q=True, tx=True  )
    dirName  = cmds.group(em=True, n = an_unicName (pfx+'Dir', '_grp',  num=True)[0])[:-4]
    gScale = float(cmds.getAttr (cmds.textFieldButtonGrp ('TFBG_solver', q=True, tx=True )+".gScale"))

        # controller
    p = [[-1.25, 1, 0], [-1.25, 1, -0.375], [-1.25, 1, -0.75], [-1.25, 1, -1], [-1.25, 1, -1.25], [-1, 1, -1.25],
        [-0.75, 1, -1.25], [-0.375, 1, -1.25], [0, 1, -1.25], [0.375, 1, -1.25], [0.75, 1, -1.25], [1, 1, -1.25],
        [1.25, 1, -1.25], [1.25, 1, -1], [1.25, 1, -0.75], [1.25, 1, -0.375], [1.25, 1, 0], [1.25, 1, 0.375],
        [1.25, 1, 0.75], [1.25, 1, 1], [1.25, 1, 1.25], [1, 1, 1.25], [0.75, 1, 1.25], [0.375, 1, 1.25], [0, 1, 1.25],
        [-0.375, 1, 1.25], [-0.75, 1, 1.25], [-1, 1, 1.25], [-1.25, 1, 1.25], [-1.25, 1, 1], [-1.25, 1, 0.75], [-1.25, 1, 0.375], [-1.25, 1, 0]]
    p2 = [[-1.25, 1, 0],  [-1, 1, 0], [-0.75, 1, 0], [-0.375, 1, 0], [0, 1, 0], [0.375, 1, 0],  [0.75, 1, 0], [1, 1, 0], [1.25, 1, 0] ]

    curv2 = cmds.curve(d=3, p=[[x[0]*gScale, x[1]*gScale, x[2]*gScale] for x in p2], n=dirName+'tmp'  ) #controller
    controllerName  = cmds.curve(d=3, p=[[x[0]*gScale, x[1]*gScale, x[2]*gScale] for x in p], n=dirName+'_ctrl'  ) #controller
    ctrl(controllerName).addShape( curv2)
    ctrl(controllerName).addColor ( switch=None, color=17)# addColor


    for attrS, attrT, val in ([ 'orbitPoz', 'tz', 0], ['width', 'sz', 1], ['lengthOffset', 'tx', 0], ['lengthSize', 'sx', 1]):
        cmds.addAttr   (controllerName, ln=attrS, dv=val,  keyable = True)
        cmds.connectAttr  (controllerName+'.'+attrS,  controllerName+'.'+attrT)
    ctrl(controllerName).hideAttr(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])

    cmds.xform (controllerName, os=True, piv=[0, 1*gScale, 0])
    tmpPlane = cmds.nurbsPlane (p= [0, 1*gScale, 0], ax= [0, -1, 0], w=3.14*gScale, lr=2, d=3, u=6, v=10, ch=0, n=dirName+'Nurbs_geo')
    cmds.setAttr (tmpPlane[0]+".template", 1)

    seursePlane = cmds.nurbsPlane (p= [0, 1*gScale, 0], ax= [0, -1, 0], w=2.5*gScale, lr=1, d=3, u=10, v=10, ch=0, n=dirName+'SeursePlane_geo')
    for attr in [".translate", ".scale"]: cmds.connectAttr  (controllerName+attr,  seursePlane[0]+attr)
    cmds.setAttr ( seursePlane[0] +".rotate", 0, 180, 00)
    cmds.makeIdentity( seursePlane[0], apply=True, rotate=True )

    bendDefA = cmds.nonLinear ( tmpPlane[0] , controllerName, seursePlane, type='bend', highBound=1.57, lowBound=-1.57, curvature=1)
    bendDefA[1] = cmds.rename(bendDefA[1], dirName+'BendA_def')
    cmds.setAttr ( bendDefA[1] +".rotate", 0, 0, -90)
    cmds.setAttr ( bendDefA[1] +".scale", 1*gScale, 1*gScale, 1*gScale)

#######
    bendDefB = cmds.nonLinear ( tmpPlane[0], controllerName, seursePlane,  type='bend', highBound=20, lowBound=-20, curvature=1)
    bendDefB[1] = cmds.rename(bendDefB[1], dirName+'BendB_def')
    cmds.setAttr ( bendDefB[1] +".rotate", -90, 0, -90)
    cmds.setAttr ( bendDefB[1] +".translate", 0, 1*gScale, 0)
    cmds.setAttr ( bendDefB[1] +".scale", 1*gScale, 1*gScale, 1*gScale)

    if int(cmds.about (version=True)[:4])>= 2016 : #if maya 2016 or more:
        cmds.setAttr ( bendDefA[0] +".curvature",  57.3)
        cmds.setAttr ( bendDefB[0] +".curvature",  57.3)

    cmds.parent (bendDefB[1], bendDefA[1], tmpPlane[0], seursePlane, controllerName, dirName+'_grp')
    cmds.xform (os=True, piv=[0, 0, 0])
    for obj in [bendDefB[1], bendDefA[1], seursePlane[0]]: cmds.setAttr (obj+".v", 0)
    solverGrp = cmds.textFieldButtonGrp ('TFBG_solver', q=True, tx=True ).replace('CorectionRig_grp', 'Solver_grp')
    cmds.parent (dirName+'_grp', solverGrp)
    for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']: cmds.setAttr (dirName+'_grp.'+attr, 0)

    cmds.select ( controllerName, r=True)

    #an_connectRigVis (solverGrp, [controllerName,])

    return dirName, controllerName



def an_addDirection ():

    pfx = cmds.textFieldGrp ('TFBG_pfx', q=True, tx=True  )
    controllerName = cmds.ls (sl=True)[0]
    seursePlane = controllerName.replace('_ctrl', 'SeursePlane_geo')
    tmpPlane    = controllerName.replace('_ctrl', 'Nurbs_geo')
    dirName = cmds.listRelatives (controllerName, p=True)[0]
    locator = pfx+'Correctiv_ctrl'

    for obj in [controllerName, seursePlane, tmpPlane]: cmds.delete(obj, ch=True )# del history
    cmds.delete(tmpPlane)
    ctrl(controllerName).showTransAttrs()

    for attr in ( 'orbitPoz',  'width',  'lengthOffset',  'lengthSize' ):
        cmds.deleteAttr( controllerName+'.'+attr )

    for attr in [".translate", ".scale"]: cmds.disconnectAttr  (controllerName+attr,  seursePlane+attr)

    cmds.connectAttr  (controllerName+".rotate",  seursePlane+".rotate")
    ctrl(controllerName).hideAttr(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])

    vPointOnSurface = cmds.createNode ("closestPointOnSurface", n=pfx+"PointOnSurface")
    cmds.connectAttr  (locator+'.translate',  vPointOnSurface+".inPosition")

    v_nurbShape = cmds.listRelatives ( seursePlane, s=True )[0]
    cmds.connectAttr  (v_nurbShape+".worldSpace[0]",  vPointOnSurface+".inputSurface")

    setRange = cmds.createNode ("setRange", n=pfx+"SetRange")
    cmds.connectAttr  (vPointOnSurface+".parameterV",  setRange+".valueX")

    cmds.setAttr (setRange+".minX", -1)
    cmds.setAttr (setRange+".maxX", 1)
    cmds.setAttr (setRange+".oldMaxX", 1)

    multiplyDivide = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide" )

    cmds.setAttr (multiplyDivide+".operation", 3)
    cmds.setAttr (multiplyDivide+".input2X", 2)
    cmds.connectAttr  (setRange+".outValueX",  multiplyDivide+".input1X")

    revers = cmds.createNode ("reverse", n=pfx+"Revers")
    cmds.connectAttr (multiplyDivide+'.outputX', revers+'.inputX')

    multiplyDivide2 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide2" )
    cmds.connectAttr ( revers+'.outputX',  multiplyDivide2+'.input1X')
    cmds.connectAttr ( vPointOnSurface+'.parameterU',  multiplyDivide2+'.input2X')

    for attr in ( 'val',  'multiplier',  'resultVal'  ):
        cmds.addAttr  (controllerName,  ln=attr, dv=10, keyable=True)

    cmds.connectAttr (  multiplyDivide2+'.outputX', controllerName+'.val')

    multiplyDivide3 = cmds.createNode ("multiplyDivide", n=pfx+"multiplyDivide3" )

    cmds.connectAttr ( multiplyDivide2+'.outputX',  multiplyDivide3+'.input1X')
    cmds.connectAttr ( controllerName+'.multiplier',  multiplyDivide3+'.input2X')
    cmds.connectAttr (  multiplyDivide3+'.outputX', controllerName+'.resultVal')

    pos = cmds.xform (dirName, q=True, t=True, ws=True)
    cmds.xform (controllerName, os=True, ws=True, piv=pos)
    cmds.xform (seursePlane, os=True, ws=True, piv=pos)

    an_delSys(dirName, [vPointOnSurface, setRange, multiplyDivide, revers, multiplyDivide2, multiplyDivide3])
    cmds.select ( controllerName, r=True)
    cmds.textFieldGrp ("TFBG_dir", e=True, tx = controllerName)




def corrctionGroups():
    lList= ([Skel().shoulderJnt, Skel().torsoJnt],
            [Skel().upArmJnt, Skel().shoulderJnt],
            [Skel().foreArmJnt, Skel().upArmJnt],
            [Skel().handJnt, Skel().foreArmJnt],
            [Skel().upLegJnt, Skel().hipJnt],
            [Skel().lowLegJnt, Skel().upLegJnt],
            [Skel().footJnt, Skel().lowLegJnt],
            [Skel().toeJnt[0], Skel().footJnt],)

    CSList=[]

    for bendJnt, upJnt in lList:

        pfx = chn(bendJnt).divideName()[0]+chn(bendJnt).divideName()[1]+'CS'
        cmds.textFieldGrp ('TFBG_pfx', e=True, tx=pfx  )
        cmds.select(bendJnt, upJnt)
        lSys = an_correctionSystem ()
        CSList.append(lSys)
        cmds.select(lSys)
        an_mirrorSys()
    return CSList



