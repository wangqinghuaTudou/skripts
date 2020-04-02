import maya.cmds as mc


def pvMirrorXform(object, state):
    if 'l_' in object: opposite = object.replace('l_','r_')
    elif 'r_' in object: opposite = object.replace('r_','l_')
    if state[0]:
        tr = getAttr(object + '.translate')[0]
        setAttr(opposite + '.translateX', -tr[0])
        setAttr(opposite + '.translateY', tr[1])
        setAttr(opposite + '.translateZ', tr[2])
    if state[1]:
        rt = getAttr(object + '.rotate')[0]
        setAttr(opposite + '.rotateX', -rt[0])
        setAttr(opposite + '.rotateY', rt[1])
        setAttr(opposite + '.rotateZ', rt[2])
    if state[2]:
        sc = getAttr(object + '.scale')[0]
        setAttr(opposite + '.scaleX', sc[0])
        setAttr(opposite + '.scaleY', sc[1])
        setAttr(opposite + '.scaleZ', sc[2])