import maya.cmds as cmds

header = ['from maya import cmds',
          'from s3dCharBuilder.SetupRig import find_node',
          '',
          '',
          'def setup(namespace="", part=""):',
          '    find = lambda i, c=namespace, p=part: find_node(i, character=c, part=p)']


def chek_in_parent_constraint(jnt_name):
    out = []
    if cmds.connectionInfo(jnt_name + ".rotateX", isDestination=True):
        constraint_node = cmds.connectionInfo(jnt_name + ".rotateX", sourceFromDestination=True).split(".")[0]
        if cmds.nodeType(constraint_node) == 'parentConstraint':
            targets = cmds.parentConstraint(constraint_node, q=True, tl=True)
            for i, target in enumerate(targets):
                line = '    cmds.parentConstraint(find("$CHARACTER:$PART:' + target + '"), find("$CHARACTER:' + jnt_name + '"), mo=True)'
                out.append(line)
                attr_name = constraint_node + "." + target + "W" + str(i)
                driver_attr = cmds.connectionInfo(attr_name, sourceFromDestination=True)
                if driver_attr:
                    cmds.disconnectAttr(driver_attr, attr_name)
                    line = '    cmds.connectAttr(find("$CHARACTER:$PART:' + driver_attr + '"), find("' + attr_name + '"), force=True)'
                    out.append(line)
            cmds.delete(constraint_node)
    return out


def chek_out_parent_constraint(jnt_name):
    out = []
    if cmds.connectionInfo(jnt_name + ".parentMatrix[0]", isSource=True):
        destinations = cmds.connectionInfo(jnt_name + ".parentMatrix[0]", destinationFromSource=True)
        constraints = [x.split(".")[0] for x in destinations]
        for constraint_node in constraints:
            if cmds.nodeType(constraint_node) == 'parentConstraint':
                dependent_object = cmds.connectionInfo(constraint_node + ".constraintParentInverseMatrix",
                                                       sourceFromDestination=True)
                dependent_object = dependent_object.split(".")[0]
                line = '    cmds.parentConstraint(find("$CHARACTER:' + jnt_name + '"), find("$CHARACTER:$PART:' + dependent_object + '"), mo=True)'
                out.append(line)
                for i in range(10):
                    attr_name = constraint_node + "." + jnt_name + "W" + str(i)
                    if cmds.objExists(attr_name) and cmds.connectionInfo(attr_name, isDestination=True):
                        driver_attr = cmds.connectionInfo(attr_name, sourceFromDestination=True)
                        cmds.disconnectAttr(driver_attr, attr_name)
                        line = '    cmds.connectAttr(find("$CHARACTER:' + driver_attr + '"), find("' + attr_name + '"), force=True)'
                        out.append(line)
                cmds.delete(constraint_node)
    return out


def chek_in_transform(jnt_name):
    prohibited_list = ['parentConstraint', 'orientConstraint', 'pointConstraint', 'scaleConstraint', 'aimConstraint']
    out = []
    attributes = ("translate", "rotate", "scale", "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v")
    for attr in attributes:
        if cmds.connectionInfo(jnt_name + "." + attr, isDestination=True):
            print attr
            target = cmds.connectionInfo(jnt_name + "." + attr, sourceFromDestination=True)
            target_node = target.split(".")[0]
            if cmds.nodeType(target_node) == u"unitConversion":
                target = cmds.connectionInfo(target_node + ".input", sourceFromDestination=True)
            if not cmds.nodeType(target) in prohibited_list:
                cmds.disconnectAttr(target, jnt_name + "." + attr)
                line = '    cmds.connectAttr(find("$CHARACTER:$PART:' + target + '"), find("$CHARACTER:' + jnt_name + "." + attr + '"), force=True)'
                out.append(line)
    return out

# TODO: Create chek_out_transform.
# TODO: Create chek_in_orient_constraint.
# TODO: Create chek_in_aim_constraint.
# TODO: Create chek_in_point_constraint.
# TODO: Create chek_out_orient_constraint.
# TODO: Create chek_out_aim_constraint.
# TODO: Create chek_out_point_constraint.

def generate_connection():
    cmds.select('ROOT')
    out = []
    cmds.select(hi=True)
    all_jnt = cmds.ls(sl=True, type="joint")

    out.append("    # in parent constraint:")
    for joint in all_jnt:
        out += chek_in_parent_constraint(joint)

    out.append("    # out parent constraint:")
    for joint in all_jnt:
        out += chek_out_parent_constraint(joint)

    out.append("    # connection to transform attributes:")
    for joint in all_jnt:
        out += chek_in_transform(joint)

    file_path = cmds.fileDialog2(fileFilter='*.py', fileMode=0, caption="Save position", dir="")[0]
    file_obj = open(file_path, 'w+')
    for i in header + out:
        file_obj.write(i + "\n")
    file_obj.close()


if __name__ == '__main__':
    generate_connection()
