

'''
Цели:
1 Создаем парент лист и скин лист.
2 группы ап и даун поинт констрейнятся и ориентируются через аим.
3 Система делится на простую, сложную ( 4 дирекшена), и дополнительную слложную (Настроенные в ручную косточи)
4 Возможность создания управляющей группы для пальцев и пр.
5 Возможность удаления с сохранением настроек

План:
1 Создание системы имен
1 Создание системы и групп внутри неё, ориентация групп
2 Создание солвера

# Naming convention
# ____________l_index2StYnRv_jnt___________  
# l_index2 (parent jnt name),      St (St and End - placing on parent jnt)       Yn or Yp (y negativ or positiv direction),   Rv 
'''





#________________________________________________________________________




skinJnrList = ['l_foreArm_jnt', 'l_upArm_jnt']
parentJntList = 'l_armBendDw0_jnt', 'l_armBendUp7_jnt'

def createCSSys(skinJnrList, parentJntList, type = 'simple',  driveGrp=''):
    pfx = chn(skinJnrList[0]).divideName()[0]+chn(skinJnrList[0]).divideName()[1]+'CS'
    upPfx = chn(skinJnrList[1]).divideName()[0]+chn(skinJnrList[1]).divideName()[1]+'CSEnd'
    rigGrp = cmds.group (em=True, n=pfx +'_grp')
    
    upGrp, bendGrp, solvGrp =  upPfx+'Jnt_grp', pfx+'StJnt_grp', pfx+'Solver_grp'
    for grp in [upGrp, bendGrp, solvGrp]:
        cmds.group (em=True, n=grp)
        cmds.parent(grp, rigGrp)
    for grp in [upGrp, bendGrp]:
        cmds.delete(cmds.parentConstraint(skinJnrList[0], grp))
    cmds.delete(cmds.aimConstraint(skinJnrList[1], upGrp, aimVector=[1,0,0], upVector=[0,0,1], worldUpType="objectrotation", worldUpVector=[0,0,1], worldUpObject=bendGrp ))
    for grp, jnt in zip([ bendGrp, upGrp], parentJntList): cmds.parentConstraint(jnt, grp, mo=True)

    if type == 'simple':
        for attr, rt in zip (['.zVal', '.yVal'] , ['.rz', '.ry']):
            cmds.addAttr(solvGrp, longName = attr[1:], k=True, dv = 0.0)  
            cmds.connectAttr  (skinJnrList[0]+ rt,  solvGrp+ attr,)
    else: 
        for attr  in ['zPoz', 'zNeg', 'zVal', 'yPoz', 'yNeg', 'yVal']:
            cmds.addAttr(solvGrp, longName = attr, k=True, dv = 0.0)
            addSolver(pfx)



def addSolver(pfx, upGrp, bendGrp, solvGrp): 
    print pfx


    dirs = {'yPos':[1,0,2,3,0,1,1,2], 'yPos':[1,0,2,3,0,1,1,2]}
    
    nurbsSphere = cmds.sphere (ax=[-1, 0, 0], s=1,  ch=0)[0]
    locator = cmds.spaceLocator (p=[0, 0, 0])[0]
    
    cmds.setAttr (locator+".translateX", 1)
    #cmds.parentConstraint('joint2', locator, mo=True)
    
    vPointOnSurface = cmds.createNode ("closestPointOnSurface", n=pfx+"PointOnSurface")
    cmds.connectAttr  (locator+'.translate',  vPointOnSurface+".inPosition")
    
    v_nurbShape = cmds.listRelatives ( nurbsSphere, s=True )[0]
    cmds.connectAttr  (v_nurbShape+".worldSpace[0]",  vPointOnSurface+".inputSurface")
    
    cmds.rebuildSurface  (nurbsSphere,  ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=0, du=3, sv=0, dv=3, tol=0.01, fr=0, dir=0)
    
    cmds.parent(locator, nurbsSphere) # position of loc and sphere
    cmds.delete(cmds.parentConstraint(bendGrp, nurbsSphere ))
    cmds.parent(locator, nurbsSphere, solvGrp) 
    cmds.parentConstraint(bendGrp, locator, mo=True)    
    cmds.parentConstraint(upGrp, nurbsSphere, mo=True)   
    
    
    for dir in dirs.keys(): 
        
        set_range = cmds.createNode ('setRange', n=pfx+dir+'SR') 
    
        for x in ['X', 'Y' ]:
            cmds.connectAttr ( vPointOnSurface+'.parameterV',  set_range+'.value'+x)
    
    
        for attr, val in zip(["minX", "maxX",  "oldMinX",  "oldMaxX",   "minY",   "maxY",  "oldMinY",  "oldMaxY"], dirs[dir],):
            cmds.setAttr (set_range+"."+attr, val)





    seursePlane = cmds.nurbsPlane (p= [0, 1, 0], ax= [0, -1, 0], w=2.5, lr=1, d=3, u=10, v=10, ch=0, n='SeursePlane_geo')
    
    



    for attr in [".translate", ".scale"]: cmds.connectAttr  (controllerName+attr,  seursePlane[0]+attr)
    cmds.setAttr ( seursePlane[0] +".rotate", 0, 180, 00)
    cmds.makeIdentity( seursePlane[0], apply=True, rotate=True )

    bendDefA = cmds.nonLinear ( tmpPlane[0] , controllerName, seursePlane, type='bend', highBound=1.57, lowBound=-1.57, curvature=1)







 