import maya.cmds as mc

def pvClearRefNs ():
#delete references
    for each in ls (type ='reference'):
        print ('Deleted reference node ' + each)
        lockNode (each, l = 0)
        delete (each)

#delete namespaces
    for each in namespaceInfo (lon=True):
        if ('UI' in each) == 0:
            if ('shared' in each) == 0:
                namespace (each, mnr = True, rm = True)
                print ('Deleted namespaces ' + count)