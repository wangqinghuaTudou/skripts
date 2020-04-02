from maya import cmds

def pvGetAllReferences():

    all_references_list = []
    references_list = cmds.file("", query=True, reference=True)
    for ref in references_list:
        children_references = pvGetReferencesChildren(ref)
        references_list += children_references

    return references_list


def pvGetReferencesChildren(ref):

    references_list = []
    children_references = cmds.file(ref, query=True, reference=True)
    if children_references:
        for ref in  children_references:
            children_references = pvGetReferencesChildren(ref)
            references_list += children_references

    return  references_list

if __name__ == '__main__':
    pvGetAllReferences()