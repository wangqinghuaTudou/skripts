import maya.cmds as mc

def pvDelMuteAnim():
    bwList = []
    for each in mc.ls(sl=True):
        attrs = mc.listAttr(each, k=True)
        print attrs
        for att in attrs:
            connList = mc.listConnections('%s.%s'%(each,att), source=True, destination=False)
            if connList:
                for conn in connList:
                    if nodeType(conn)=='mute':
                        bwList.append(conn)
                        connListBW = mc.listConnections('%s.input'%conn, source=True, destination=False)
                        connListBW.append(mc.listConnections('%s.mute'%conn, source=True, destination=False)[0])
                        for connBW in connListBW:
                            if 'mute' in connBW:
                                mc.delete(connBW)
                            else:
                                mc.connectAttr('%s.output'%connBW, '%s.%s'%(each,att), force=True)
    if bwList:
        mc.delete(bwList)