import maya.cmds as cmds
import random as rnd

print('---------------------------------------------------')
start_time = cmds.playbackOptions(query=True, minTime=True)
alembic_list = cmds.ls(type='AlembicNode')
if not alembic_list:
    print('Scene hasn\'t any "alembic" node.')
else:
    counter = 0
    for al in alembic_list:
        try:
            cmds.setAttr(al + '.offset', int(start_time + rnd.uniform(-300, 0)))
            counter += 1
        except Exception, err:
            print('Can\'t set "offset" to %s "alembic" node.'%al)
            print(err)
    if counter:
        print('"Offset" setted for %s "alembic" nodes.'%counter)
    else:
        print('Can\'t set "offset" to any "alembic" node.')
print('---------------------------------------------------')