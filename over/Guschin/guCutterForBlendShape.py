import maya.cmds as mc 
def guCutterForBlendShape():

    win = 'guCutterForBlendShape'
    if mc.window(win, exists=True):
        mc.deleteUI(win)
    win = mc.window(win, title='cutter for blendShape', \
                    width=500, \
                    height=100, \
                    sizeable=False)
    mc.columnLayout ('guLayoutCutterForBlendShape', \
                     width=200, \
                     height=100, \
                     adjustableColumn=True)

    mc.setParent( '..' )
    mc.setParent( '..' )
    
    mc.frameLayout( label='cut options',labelAlign='left' )
    mc.textFieldButtonGrp( 'guBshTxt',label='default object', text='', buttonLabel='add selected' ,bc='mc.textFieldButtonGrp(\'guBshTxt\', e=True, text=mc.ls(sl=True)[0])')
    mc.text ('then select faces or vertices or edges on BSH geometry for accept range cut ')
    bot1=mc.button( label='cut off' ,bgc=(.0,.270,0.009),command='guCutBsh()')
    mc.showWindow(win)
                       
def guReturnWeightsFromCompDist(selects=[]):
    if selects==[]:
        mc.optionVar (iv=('TrackSelectionOrder',1))
        selects=mc.ls(orderedSelection=True, fl=True)
    if selects==[]:
        mc.warning('plse select some one component on object')
        mc.error('don\'t have components selecteds')
    for i in selects:
        if not '.vtx[' in i:
            if not '.e[' in i: 
                if not '.f[' in i:
                    mc.warning('plse select some one component on object')
                    mc.error('don\'t have components selecteds')
    position=[mc.xform(x,q=True,ws=True,t=True) for x in selects]
    boudBox=mc.xform(selects[0].split('.')[0],q=True,ws=True,bb=True)
    plan=mc.polyPlane(n='tempPlan',ch=1,o=1,w=1,h=1,sw=len(selects)-1,sh=1,cuv=2)
    planVtxs=[int(x) for x in mc.getAttr(mc.listRelatives(plan[0],c=True)[0]+'.vt',mi=True)]
    for x,z in zip(planVtxs,position+position):
        if x >= len(planVtxs)/2:
            y=boudBox[1::3][1]
        else:
            y=boudBox[1::3][0]
        mc.xform(plan[0]+'.vtx['+str(x)+']',t=(z[0],y,z[2]),ws=True)
    mc.select(cl=True)
    jnts=[mc.joint(n='tempBind_'+str(a),p=(x[0],x[1],x[2])) for x,a in zip(position,xrange(len(position)+1))]
    skinClst = mc.skinCluster(plan, \
                              jnts, \
                              toSelectedBones=True, \
                              dropoffRate=4, \
                              polySmoothness=False, \
                              removeUnusedInfluence=False, \
                              maximumInfluences=5, \
                              obeyMaxInfluences=False, \
                              normalizeWeights=True)[0]
    skinClst2 = mc.skinCluster(selects[0].split('.')[0], \
                              jnts, \
                              toSelectedBones=True, \
                              dropoffRate=4, \
                              polySmoothness=False, \
                              removeUnusedInfluence=False, \
                              maximumInfluences=5, \
                              obeyMaxInfluences=False, \
                              normalizeWeights=True)[0]
    [mc.skinPercent(skinClst,plan[0]+'.vtx['+str(x)+']',transformValue=(a,1)) for x,a in zip(planVtxs,jnts+jnts)]
    mc.copySkinWeights( ss=skinClst, ds=skinClst2, noMirror=True,sm=True)
    targVtxs=[int(x) for x in mc.getAttr(selects[0].split('.')[0]+'.vt',mi=True)]
    getTargetWaights=[[mc.skinPercent(skinClst2,selects[0].split('.')[0]+'.vtx['+str(x)+']',transform=a,q=True,v=True) for x in xrange(0,1361)] for a in jnts]
    mc.delete(jnts,plan)
    print 'have waights'
    return getTargetWaights


def guCreateTempGeo(selects,weights):
    if selects==[]:
        mc.optionVar (iv=('TrackSelectionOrder',1))
        selects=mc.ls(orderedSelection=True, fl=True)
    if selects==[]:
        mc.warning('plse select some one component on object')
        mc.error('don\'t have components selecteds')
    for i in selects:
        if not '.vtx[' in i:
            if not '.e[' in i: 
                if not '.f[' in i:
                    mc.warning('plse select some one component on object')
                    mc.error('don\'t have components selecteds')
    sel=mc.textFieldButtonGrp( 'guBshTxt',q=True,text=True)
    new=[mc.duplicate(sel,n=selects[0].split('.')[0]+'_BSH'+str(x+1))[0] for x in xrange(len(selects))]
    [[mc.setAttr(x+a,e=True,l=False) for a in ('.tx','.tz','.ty','.rx','.ry','.rz','.sx','.sy','.sz')] for x in new]
    [mc.delete(mc.parentConstraint(selects[0].split('.')[0],x,mo=False)) for x in new]
    [mc.delete(mc.scaleConstraint(selects[0].split('.')[0],x,mo=False)) for x in new]
    bsh=[mc.blendShape(selects[0].split('.')[0],x)[0] for x in new]
    [mc.setAttr(x+'.'+selects[0].split('.')[0],1) for x in bsh]
    [[mc.setAttr (x+'.inputTarget[0].inputTargetGroup[0].targetWeights['+str(a)+']', y) for a,y in zip(xrange(len(z)),z)] for x,z in zip(bsh,weights)]
    [mc.delete(x,ch=True) for x in new]




def guCutBsh():
    mc.optionVar (iv=('TrackSelectionOrder',1))
    selects=mc.ls(orderedSelection=True, fl=True)
    weights=guReturnWeightsFromCompDist(selects)
    guCreateTempGeo(selects,weights)
    

#guCutterForBlendShape()