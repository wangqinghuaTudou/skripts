import maya.cmds as cmds
from An_Controllers import An_Controllers as ctrl
from anProcedures import *
from an_twistSegment import * 


def an_ropeRivetRig_v1():
    v_win = "SplineFkIKRigUi"
    if cmds.window (v_win, exists=True):
        cmds.deleteUI (v_win)
    cmds.window(v_win, t="Ik/fk rope rig tools v.1", w=450, h=100)
    cmds.columnLayout(adj=1)
    cmds.separator(st="none", h=10)
    cmds.text("    Creates a chain of bones that stretches along the curve. Please select curve!", align="left")
    cmds.separator(st="none", h=10)
    cmds.textFieldButtonGrp('TFBG_Prefix', label="Prefix: ", bl="Assign", bc="cmds.textFieldButtonGrp ('TFBG_Prefix', e=True, tx= cmds.ls(sl=True)[0])")
    cmds.textFieldButtonGrp('TFBG_General_CT', label="General_CT: ", bl="Assign", bc="cmds.textFieldButtonGrp ('TFBG_General_CT', e=True, tx= cmds.ls(sl=True)[0])")
    cmds.intSliderGrp('ISG_1', field=1, minValue=3, maxValue=500, value=20, label=" Joints number: ")
    cmds.intSliderGrp('ISG_2', field=1, minValue=2, maxValue=40, value=5, label=" Controllers number: ")
    cmds.separator(st="none", h=3)
    cmds.checkBoxGrp('inputPosCHB', columnWidth2=[141, 165], numberOfCheckBoxes=1, label='Input CT pos: ', v1=False, changeCommand1='an_change()')    
    cmds.separator(st="none", h=3) 
    cmds.textFieldGrp('TFBG_posList', label="Pos list: ", tx= '0,  0.1,  0.5,  0.92,  1', enable=False)
    cmds.showWindow(v_win)
    cmds.separator(st="none", h=10)
    cmds.button(l="Make rope rig", c="an_ropeRig()")

def an_change():
    state = cmds.checkBoxGrp('inputPosCHB', q=True,  v1=True) 
    if state: 
        cmds.intSliderGrp('ISG_2', e=True,  enable=False)
        cmds.textFieldGrp('TFBG_posList', e=True,  enable=True)
    else: 
        cmds.intSliderGrp('ISG_2', e=True,  enable=True) 
        cmds.textFieldGrp('TFBG_posList', e=True,  enable=False)
    
def an_rivetJnt(nameObject, e1, e2):  # e1, e2 - nambers of edges

    '''
    list = cmds.filterExpand (sm= 32)
    nameObject =  list[0].split('.')[0]
    e1 =  list[0].split('[')[1].split(']')[0]
    e2 =  list[1].split('[')[1].split(']')[0]
    an_rivet(nameObject, e1, e2)
    '''
    v_prefix = cmds.textFieldButtonGrp('TFBG_Prefix', q=True, tx=True)+'_'
    
    nameCFME1 = cmds.createNode ( 'curveFromMeshEdge', n=v_prefix+"rivetCurveFromMeshEdge1")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e1))
    
    nameCFME2 = cmds.createNode ( 'curveFromMeshEdge', n=v_prefix+"rivetCurveFromMeshEdge2")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e2))
    
    nameLoft = cmds.createNode ( 'loft' , n=v_prefix+"rivetLoft1")
    cmds.setAttr (nameLoft+ ".ic", s=2)
    cmds.setAttr (nameLoft+  ".u", True)
    cmds.setAttr (nameLoft+  ".rsn", True)
    
    namePOSI = cmds.createNode ( 'pointOnSurfaceInfo' , n= v_prefix+"rivetPointOnSurfaceInfo1")
    cmds.setAttr ( ".turnOnPercentage", 1)
    cmds.setAttr ( ".parameterU", 0.5)
    cmds.setAttr ( ".parameterV", 0.5)
    
    cmds.connectAttr ( nameLoft + ".os",  namePOSI + ".is", f=True)
    cmds.connectAttr ( nameCFME1 + ".oc",  nameLoft + ".ic[0]")
    cmds.connectAttr ( nameCFME2 + ".oc",  nameLoft + ".ic[1]")
    cmds.connectAttr ( nameObject + ".w",  nameCFME1 + ".im")
    cmds.connectAttr ( nameObject + ".w",  nameCFME2 + ".im")
  
    nameLocator = cmds.createNode ( 'joint' , n=v_prefix+"rivet1")
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

#v_curve, obj, pos= 'fIk_crv', 'f0_ori', 0.5

def placeObjOnCurve(v_curve, obj, pos):
    upVector = [0,0,1]
    loc = cmds.spaceLocator()[0]
    poci = cmds.createNode('pointOnCurveInfo')
    cmds.connectAttr(v_curve + '.worldSpace[0]', poci + '.inputCurve', force=True)
    cmds.setAttr(poci + '.parameter', pos)
    cmds.setAttr(poci + '.turnOnPercentage', 1)
    cmds.connectAttr(poci + '.position', loc + '.translate', force=True)
    locPos = cmds.duplicate(loc)[0]
    cord = cmds.getAttr( loc+'.translate')[0] 
    cmds.setAttr(locPos+'.translate', cord[0], cord[1], cord[2])
    aimVec = 1 if not pos==1 else -1
    cmds.setAttr(poci + '.parameter', pos+(0.01*aimVec))
    cmds.delete(cmds.aimConstraint(loc, locPos,  aim = [aimVec, 0, 0], u=upVector, wu=upVector,   mo=False))     
    cmds.delete(cmds.parentConstraint( locPos, obj, mo=False))
    cmds.disconnectAttr(poci + '.position', loc + '.translate')
    cmds.delete(poci, loc, locPos)


def an_ropeRig():
    usList = cmds.checkBoxGrp('inputPosCHB', q=True,  v1=True)
    posList =[]
    v_ctNumber=[]
    
    if usList:
        textList = cmds.textFieldGrp('TFBG_posList', q=True,  tx=True)
        dev =[x.split(',') for x in textList.split('_') if x][0]
        posList = [float(x) for x in dev ]
        v_ctNumber = len(posList)
        
    else:
        v_ctNumber = cmds.intSliderGrp('ISG_2', q=True, v=True)
        posList = [ x*(1.0/v_ctNumber) for x in  range(v_ctNumber)]+[1.0,]
        
    v_jntNum = cmds.intSliderGrp('ISG_1', q=True, v=True)
    v_prefix = cmds.textFieldButtonGrp('TFBG_Prefix', q=True, tx=True )
    v_general_CT = cmds.textFieldButtonGrp('TFBG_General_CT', q=True, tx=True )
    # start
    v_curve = cmds.ls(selection=True)[0]
    v_curveShape = cmds.listRelatives(v_curve, shapes=True)[0]
    v_cvNumber = cmds.getAttr(v_curveShape + '.degree') + cmds.getAttr(v_curveShape + '.spans')
    cmds.setAttr(v_curve + ".v", 0)
    cmds.addAttr(v_general_CT, longName='ikFkMix', k=True, min = 0, max=1) 
    cutvLen = cmds.arclen (v_curve, ch=0)/30
    #ik jnt
    v_CT_jntsName, v_CT_orisName , profilsList= [], [], []
    for i in xrange(v_ctNumber):
        v_ct = ctrl(v_prefix + str(i) + '_CT')
        v_ct.makeController('sphere', size=1, offset=[0, 0, 0], orient="Y")
        v_ct.gropeCT()
        v_ctJnt= cmds.joint(r=True, n=v_prefix + 'Ctrl' + str(i) + "_jnt_")
        cmds.setAttr(v_ctJnt + ".v", 0)
        v_CT_jntsName.append(v_ctJnt)
        v_CT_orisName.append(v_ct.oriGrp)
        # replace v_curve by v_curveShape because of new procedure
        placeObjOnCurve(v_curveShape, v_ct.oriGrp, posList[i])
        cmds.connectAttr(v_general_CT+'.ikFkMix', v_ct.oriGrp+'.v' )
        #profils :
        profil = cmds.curve (d=1,  p=[(0, 0, -1.0*cutvLen),  (0, 0, cutvLen)] )
        placeObjOnCurve(v_curveShape, profil, posList[i])
        profilsList.append(profil)
    
    ikplane = cmds.loft( profilsList, n=v_prefix+'Ik_nrb', ch=True, rn=True, ar=True )[0]
    fkplane = cmds.loft( profilsList, n=v_prefix+'Fk_nrb', ch=False, rn=True, ar=True )[0]
    for nPlane in [ikplane, fkplane]: 
        cmds.setAttr(nPlane + ".v", 0)
        cmds.setAttr(nPlane + ".inheritsTransform", 0)
    
    cmds.delete(profilsList)
    cmds.skinCluster(ikplane, v_CT_jntsName, dr=4.5)
    
    v_fkGrp = cmds.group(v_CT_orisName, ikplane , n=v_prefix + "IkRigGrp" )
    
    #fk jnt
    fk_CT_jntsName, fk_CT_orisName = [], []
    for i in xrange(v_ctNumber):
        v_ct = ctrl(v_prefix + str(i) + 'Fk_CT')
        v_ct.makeController('circle', size=1.5, offset=[0, 0, 0], orient="X")
        v_ct.gropeCT()
        v_ctJnt= cmds.joint(r=True, n=v_prefix + 'Ctrl' + str(i) + "Fk_jnt_")
        cmds.setAttr(v_ctJnt + ".v", 0)
        fk_CT_jntsName.append(v_ctJnt)
        fk_CT_orisName.append(v_ct.oriGrp)
        placeObjOnCurve(v_curveShape, v_ct.oriGrp,  posList[i])
        if  i: 
            print fk_CT_orisName[i],    v_prefix + str(i-1) + 'Fk_CT'
            cmds.parent(fk_CT_orisName[i],    v_prefix + str(i-1) + 'Fk_CT')
        
    cmds.skinCluster(fkplane, fk_CT_jntsName, dr=4.5)
    v_Grp = cmds.group(fk_CT_orisName[0], fkplane , n=v_prefix + "Fk_RigGrp" )
    vBsh = cmds.blendShape ( ikplane, fkplane, w=[(0, 1)])
    
    cmds.connectAttr (v_general_CT+'.ikFkMix', vBsh[0]+'.'+ikplane)
    an_connectReversAttr (v_general_CT+'.ikFkMix', fk_CT_orisName[0]+'.v')
    
    #mixGrp = cmds.group( em=True, n=v_prefix + "MixGrp")
    #pConstr = cmds.parentConstraint( fk_CT_jntsName[-1], v_CT_jntsName[-1],  mixGrp, mo=False)[0]
    #an_connectReversAttr (v_general_CT+'.ikFkMix', pConstr+'.'+fk_CT_jntsName[-1]+"W0")
    #cmds.connectAttr (v_general_CT+'.ikFkMix', pConstr+'.'+v_CT_jntsName[-1]+"W1")
    
    v_Grp = cmds.group( v_fkGrp, v_Grp, n=v_prefix + "RigGrp" )
    cmds.parent(v_Grp, v_general_CT)
    
    poly = cmds.nurbsToPoly (fkplane,  mnd=1, ch=1, f=2, pt=1, pc=200, chr=0.9, ft=0.01, mel=0.001, d=0.1, ut=1, un=v_jntNum, vn=2, vt=1, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)
    cmds.setAttr(poly[0] + ".v", 0)
    
    polySkin = cmds.nurbsToPoly (fkplane,  mnd=1, ch=0, f=2, pt=1, pc=200, chr=0.9, ft=0.01, mel=0.001, d=0.1, ut=1, un=v_jntNum, vn=2, vt=1, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
    
    rivetJnt = []
    for i in range (0, v_jntNum-1): 
        adges = cmds.polyInfo(poly[0]+'.f['+str(i)+']', faceToEdge=True )[0].split(':')[1].split(' ')    
        edgeList = [x for x in  adges  if x and x != '\n']
        rivet = an_rivetJnt(poly[0], edgeList[1], edgeList[3])
        rivetJnt.append(rivet)
        cmds.connectAttr(v_general_CT+'.s', rivet+'.s' )
        
    cmds.skinCluster(polySkin, rivetJnt, dr=4.5)
        
    v_Grp = cmds.group( rivetJnt, poly, n=v_prefix + "RivGrp" )






