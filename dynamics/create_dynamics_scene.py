import re

IGNOR_LIST = "general_CT", "pivotOffset_CT", "switch_CT"
CHAR_URL = [
    u'//renderServer/Project/SOBAKI_3d/assets/chars/liza/maya/work/rig/liza_rig.mb',
    u'C:/Users/belyaev_a/Desktop/anim_for_cloth/liza_v041.mb'
]
INPUT_OFFSET = -20
#RELACS

def set_t_pos(reference, ct_pattern="[\w:_]+_CT$"):
    """
    The function puts character in a t pose.
    """

    space_attribute_list = ["space", "rSpace"]

    ct_pattern = re.compile(ct_pattern)
    node_list = [x for x in cmds.referenceQuery(reference, nodes=True) if ct_pattern.search(x)]

    # remove ignor controllers
    node_list = [ct for ct in node_list if not ct.split(":")[-1] in IGNOR_LIST]

    # set in t-pos
    space_current_attributes = {}
    for ctrl in node_list:
        attributes = [x.split("_default")[0] for x in cmds.listAttr(ctrl) if "_default" in x]

        for attr in attributes:
            if attr in space_attribute_list:
                val = cmds.getAttr(ctrl + "." + attr)
                space_current_attributes[ctrl + "." + attr] = val

            default_val = cmds.getAttr(ctrl + "." + attr + "_default")
            try:
                cmds.setAttr(ctrl + "." + attr, default_val)
            except Exception as exception_data:
                print(exception_data)

    # create locators in control position
    locatots = []
    for ctrl in node_list:
        pos_loc = cmds.spaceLocator(name=ctrl + "_loc")[0]
        cmds.matchTransform(pos_loc, ctrl)
        try:
            cmds.pointConstraint(pos_loc, ctrl, name=ctrl + "_const")
        except:
            pass
        try:
            cmds.orientConstraint(pos_loc, ctrl, name=ctrl + "_const")
        except:
            pass
        locatots.append(pos_loc)

    # turn spaces attributes in necessary values
    for attr in space_current_attributes:
        try:
            cmds.setAttr(attr, space_current_attributes[attr])
        except Exception as exception_data:
            print(exception_data)

    # get final attributes values
    final_values = []
    for ctrl in node_list:
        attributes = [x.split("_default")[0] for x in cmds.listAttr(ctrl) if "_default" in x]
        for attr in attributes:
            try:
                val = cmds.getAttr(ctrl + "." + attr)
                final_values.append([ctrl, attr, val])
            except Exception as exception_data:
                print(exception_data)

    cmds.delete(locatots)

    # set final attributes values
    for ctrl, attr, val in final_values:
        try:
            cmds.setAttr(ctrl + "." + attr, val)
            cmds.setKeyframe(ctrl, attribute=attr, value=val)
        except Exception as exception_data:
            print(exception_data)


def get_all_controls(ctrl, sfx="_CT"):
    try:
        name_space = cmds.referenceQuery(ctrl, namespace=True, shortName=True) + ":"
    except RuntimeError:
        name_space = ""

    formula = re.compile(name_space + "\w+_CT$")
    return [x for x in cmds.ls() if formula.match(x)]


def create_dynamics_scene(CHAR_URL):
    reference_list = cmds.file(query=True, reference=True)
    characters_list = [cmds.referenceQuery(x, namespace=True, shortName=True) for x in reference_list if x in CHAR_URL]
    all_controls = []
    for char in characters_list:
        char_ignor_list = [char + ":" + ct for ct in IGNOR_LIST]
        ctrl = [ct for ct in get_all_controls(char + ":" + IGNOR_LIST[0]) if ct not in char_ignor_list]
        all_controls += ctrl

    start_time = int(cmds.playbackOptions(q=True, min=True))
    end_time = int(cmds.playbackOptions(q=True, max=True))
    cmds.bakeResults(all_controls,
                     simulation=True,
                     time=(start_time, end_time),
                     sampleBy=1,
                     oversamplingRate=1,
                     disableImplicitControl=True,
                     preserveOutsideKeys=True,
                     sparseAnimCurveBake=False,
                     removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False,
                     bakeOnOverrideLayer=False,
                     minimizeRotation=True,
                     controlPoints=False,
                     shape=True)

    cmds.playbackOptions(min=start_time - 10)

    for ct in all_controls:
        try:
            cmds.copyKey(ct, time=(start_time, start_time))
            cmds.pasteKey(ct, time=(start_time - 10, start_time - 10))
        except Exception as exception_data:
            print (exception_data)

    cmds.playbackOptions(min=start_time + INPUT_OFFSET)
    cmds.currentTime(start_time + INPUT_OFFSET, edit=True)

    for ref in reference_list:
        reference = cmds.file(ref, query=True, referenceNode=True)
        print reference

        set_t_pos(reference)

    cmds.keyTangent(all_controls, itt="linear", ott="linear")


create_dynamics_scene(CHAR_URL)