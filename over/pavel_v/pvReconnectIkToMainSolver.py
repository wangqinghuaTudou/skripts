import re

def pvReconnectIkToMainSolver():

    #ik_list = cmds.ls(type='ikSolver')
    ik_list = cmds.ls(type='ikSCsolver')
    ikRp_list = cmds.ls(type='ikRPsolver')
    ikSc_list = list(set(ik_list).difference(ikRp_list))
    cmds.select(ikSc_list, replace=True)
    cmds.select(ikRp_list, replace=True)
    
    rex = re.compile(r'^[a-zA-Z]*$')

    if len(ikSc_list) < 2:
        print('Info: Scene hasn\'t any additional SC ik solvers.')
    else:
        for sc in ikSc_list:
            if rex.match(sc):
                main_sc = sc
                break
        sc_count = 0
        for sc in ikSc_list:
            if sc != main_sc:
                conn_list = cmds.listConnections(sc + '.message', source=False, plugs=True)
                if conn_list:
                    for cn in conn_list:
                        cmds.disconnectAttr(sc + '.message', cn)
                        cmds.connectAttr(main_sc + '.message', cn, force=True)
                try:
                    cmds.delete(sc)
                except:
                    pass
                sc_count += 1
        print('Info: Successfuly reconnected and deleted %s SC ik solvers.'%sc_count)

    if len(ikRp_list) < 2:
        print('Info: Scene hasn\'t any additional RP ik solvers.')
    else:
        for rp in ikRp_list:
            if rex.match(rp):
                main_rp = rp
                break
        rp_count = 0
        for rp in ikRp_list:
            if rp != main_rp:
                conn_list = cmds.listConnections(rp + '.message', source=False, plugs=True)
                if conn_list:
                    for cn in conn_list:
                        cmds.disconnectAttr(rp + '.message', cn)
                        cmds.connectAttr(main_rp + '.message', cn, force=True)
                try:
                    cmds.delete(rp)
                except:
                    pass
                rp_count += 1
        print('Info: Successfuly reconnected and deleted %s RP ik solvers.'%rp_count)

    return True

# pvReconnectIkToMainSolver()