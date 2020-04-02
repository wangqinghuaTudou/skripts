


def an_childCaptureBetween(v_kurJnt, v_end):
    v_jnts = [];  i=0
    while not v_kurJnt == v_end:
        v_jnts.append(v_kurJnt)
        v_kurJnt = cmds.listRelatives (v_kurJnt, c=True)[0]
        i+=1
        if i==30: break
    v_jnts.append(v_kurJnt)
    return v_jnts

def an_distans (v_Start, v_End, v_Prefix ):
    v_distansName = cmds.group (em=True,  n=v_Prefix+"_distans#")
    v_distansOfsName = cmds.group ( n=v_Prefix+"_distansAim#")
    cmds.pointConstraint  (v_Start, v_distansOfsName)
    cmds.aimConstraint    ( v_End, v_distansOfsName, aim=[1, 0, 0])
    cmds.pointConstraint   ( v_End, v_distansName)
    return  v_distansName+".tx", v_distansOfsName


import maya.cmds as cmds
def an_stretchableIk():

    v_Start, v_End = cmds.ls (sl=True )

    result = cmds.promptDialog( title='FK rig system', message='Select start and end jnt, enter prefix:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':

    	v_Prefix = cmds.promptDialog(query=True, text=True)
    	v_jnts = an_childCaptureBetween(v_Start, v_End) #get jnt names
        v_ikHandle = cmds.ikHandle( sj=v_jnts[0], ee=v_jnts[-1], n=v_Prefix+"_ikHandle")[0] #make ik handle
        cmds.setAttr ( v_ikHandle+".snapEnable", 0 )

        v_distansSys = an_distans (v_Start, v_ikHandle, v_Prefix ) #make distanse solver
        v_allJntsLength = 0.0                                      #get all jnts length
        for v_jnt in v_jnts [1:]: v_allJntsLength = v_allJntsLength + cmds.getAttr (v_jnt+'.tx')

        v_condition = cmds.createNode( 'condition', n=v_Prefix+'_condition')
        cmds.setAttr ( v_condition+".secondTerm", v_allJntsLength )
        cmds.connectAttr (v_distansSys[0], v_condition+".firstTerm")
        cmds.setAttr ( v_condition+".operation", 2 )

        v_mdv = cmds.createNode( 'multiplyDivide', n=v_Prefix+'_multiplyDivide')

        cmds.setAttr ( v_mdv+".operation", 2 )
        cmds.setAttr ( v_mdv+".input2X", v_allJntsLength )
        cmds.connectAttr (v_distansSys[0], v_mdv+".input1X")
        cmds.connectAttr ( v_mdv+".outputX", v_condition+".colorIfTrueR")

        for v_jnt in v_jnts [:-1]: cmds.connectAttr ( v_condition+".outColorR", v_jnt+".sx")
        v_grp = cmds.group (v_ikHandle, v_distansSys[1], n=v_Prefix+'StretchableIk_grp' )

    else: pass
