import maya.cmds as cmds
import maya.OpenMaya as om
from pvCopyShape import *


controllers_list = ['l_hand_CT']
x_angles_list = [45, 90, 135]
y_angles_list = [30, 60, 90, 120]
z_angles_list = [30, 60, 90, 120]
geometry_corrective_joints = 'l_armCorrJoints_geo'
geometry_corrective_bs = 'l_armCorrBs_geo'
pose_interpolator = 'l_foreArm_jnt_poseInterpolator'
bs_node = 'l_armDeformer_bs'
i = 0.0
for ctrl in controllers_list:
    for i, x_angle in enumerate(x_angles_list):
        cmds.setAttr(ctrl + '.rotateX', x_angle)
        cmds.sculptTarget(bs_node, edit=True, target=-1)
        #cmds.blendShape(bs_node, e=True, topologyCheck=True, target=[|l_armCorrBs_geo|l_armCorrBs_geoShape 6 l_armCorrBs_geo2 1 -w 6 1)
        cmds.blendShape(bs_node, edit=True, target=[geometry_corrective_bs, 6 + i, geometry_corrective_bs, 0.0])
        cmds.aliasAttr('l_hand_bind_0_0_0', bs_node + '.w[6]')
        cmds.connectAttr(pose_interpolator + '.output[3]', bs_node + '.w[6]', force=True)
        pvCopyShape(geometry_corrective_joints, geometry_corrective_bs)
        i += 1
    cmds.setAttr(ctrl + '.rotateX', 0)
    for y_angle in y_angles_list:
        cmds.setAttr(ctrl + '.rotateY', y_angle)
        pvCopyShape(geometry_corrective_joints, geometry_corrective_bs)
    cmds.setAttr(ctrl + '.rotateY', 0)
    for z_angle in z_angles_list:
        cmds.setAttr(ctrl + '.rotateZ', z_angle)
        pvCopyShape(geometry_corrective_joints, geometry_corrective_bs)
    cmds.setAttr(ctrl + '.rotateZ', 0)