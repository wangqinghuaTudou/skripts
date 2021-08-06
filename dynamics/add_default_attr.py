# Write t-pose.
def add_default_attr():
    transform_list = [x for x in cmds.ls(type="transform") if "_CT" in x]
    while transform_list:
        transform = transform_list.pop()
        if cmds.referenceQuery(transform, isNodeReferenced=True):  # not referens
            continue

        if True in cmds.lockNode(transform, query=True, lock=True):
            continue

        user_attribute_list = cmds.listAttr(transform, userDefined=True)
        if not user_attribute_list:
            user_attribute_list = []

        for atttribute in ["rx", "ry", "rz", "tx", "ty", "tz", "sx", "sy", "sz"]:
            user_attribute_list.append(atttribute)

        while user_attribute_list:
            user_attribute = user_attribute_list.pop()
            if user_attribute.startswith("ml_") or user_attribute.endswith("_default"):
                continue

            if cmds.getAttr(transform + "." + user_attribute, lock=True):
                continue

            if not cmds.getAttr(transform + "." + user_attribute, keyable=True):
                continue

            if not cmds.getAttr(transform + "." + user_attribute, settable=True):
                continue

            try:
                attribute_type = cmds.attributeQuery(user_attribute, n=transform, attributeType=True)

            except Exception as exception_data:
                print(exception_data)
                attribute_type = None

            if not attribute_type or re.search("string|compound|array|vector|color|type|rgb", attribute_type, re.I):
                continue

            try:
                default_value = cmds.getAttr(transform + "." + user_attribute)
                if isinstance(default_value, (list, set, tuple, unicode, basestring)):
                    continue

                default_user_attribute = user_attribute + "_default"
                if not cmds.attributeQuery(default_user_attribute, n=transform, exists=True):
                    cmds.addAttr(transform, longName=default_user_attribute, hidden=True)
                    print(default_user_attribute)
                cmds.setAttr(transform + "." + default_user_attribute, default_value)

            except Exception as exception_data:
                print(exception_data)
